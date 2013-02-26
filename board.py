# Copyright (c) 2013, Robert Rueger <rueger@itp.uni-frankfurt.de>
#
# This file is part of RC4.
#
# RC4 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# RC4 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with RC4.  If not, see <http://www.gnu.org/licenses/>.

"""Class for a connect-4 board"""

from os import name as os_name


class Board:


    def __init__(self, cols = 7, lines = 6):
        """initializes a new board"""

        # initialize move history
        self.move_history = []

        # build a new board
        # can be accessed like this: board[line][col]
        # board[0][0] is in the upper left corner
        self.cols = cols
        self.lines = lines
        self.board = []
        for i in range(lines):
            self.board.append([])
            for j in range(cols):
                self.board[i].append(0)


    def __str__(self):
        """returns a pretty string, that is ready for printing"""

        output = []

        # set colors for the output
        if os_name == 'posix':
            red = "\033[31m"
            green = "\033[32m"
            gray = "\033[30m"
            black = "\033[0m"
        else:  # unfortunately no colors for windows shell
            red = ""
            green = ""
            gray = ""
            black = ""

        # column labels
        for i in range(0,self.cols):
            output.append(" " + str(i))
        output.append("\n")
        for i in range(0,self.cols):
            output.append(" -")
        output.append("\n")

        # print board line by line
        for i in range(0,self.lines):
            for j in range(0,self.cols):
                output.append(" ")
                if self.board[i][j] == 0:
                    output.append(gray + str(self.board[i][j]))
                elif self.board[i][j] == 1:
                    output.append(green + str(self.board[i][j]))
                elif self.board[i][j] == 2:
                    output.append(red + str(self.board[i][j]))
            output.append("\n")

        # tidy up and return output string
        #output.pop()
        output.append(black)
        return "".join(output)


    def dump(self):
        """returns the board as a 2dim list"""

        return self.board


    def move(self, move, player):
        """updates the board, when a player makes a valid move"""

        if self.move_is_valid(move):
            # look for the first free slot in column (bottom-up)
            i = self.lines - 1
            while i > 0 and self.board[i][move] != 0:
                i -= 1
            self.board[i][move] = player
            # update the history
            self.move_history.append((player, move))
            return True
        else:
            return False


    def move_is_valid(self, move):
        """checks if a move is possible on a board"""

        try:
            if self.board[0][move] == 0:
                return True
            else:
                return False
        except IndexError:
            return False


    def undo(self, n = 1):
        """undo the last n moves"""

        j = 0
        while j < n and self.move_history != []:
            j += 1

            move = self.move_history.pop()
            i = 0
            while self.board[i][move[1]] == 0: i += 1
            if self.board[i][move[1]] == move[0]:
                self.board[i][move[1]] = 0
            else:
                raise ValueError("board history is corrupted!")


    def dimensions(self):
        """returns the boards dimensions (lines, cols)"""

        return (self.lines, self.cols)


    def line_count(self):
        """returns the board number of lines"""

        return self.lines


    def col_count(self):
        """returns the board number of columns"""

        return self.cols


    def element(self, line, col):
        """returns the element at position [line][col] as string"""

        try: return str(self.board[line][col])
        except: return ""


    def line(self, n):
        """returns line n as a string"""

        if 0 <= n < self.lines:
            return "".join(str(element) for element in self.board[n])
        else:
            return ""


    def col(self, n):
        """returns col n as a string"""

        if 0 <= n < self.cols:
            result = []
            for i in range(0, self.lines):
                result.append(str(self.board[i][n]))
            return "".join(result)
        else:
            return ""


    def diagonal1(self, n):
        """returns bottom left to top right diagonals"""

        result = []
        if 0 <= n < self.lines:
            line, col = n, 0
        elif self.lines <= n <= self.lines + self.cols - 1:
            line, col = self.lines - 1, n - self.lines + 1
        else:
            return ""
        while line >= 0 and col < self.cols:
            result.append(str(self.board[line][col]))
            line -= 1
            col += 1
        return "".join(result)


    def diagonal2(self, n):
        """returns top left to bottom right diagonals"""

        result = []
        if 0 <= n < self.lines:
            line, col = n, self.cols - 1
        elif self.lines <= n <= self.lines + self.cols - 1:
            line, col = self.lines - 1, self.cols - (n - self.lines + 2)
        else:
            return []
        while line >= 0 and col < self.cols and col >= 0:
            result.append(str(self.board[line][col]))
            line -= 1
            col -= 1
        return "".join(result)


    def vincinity(self, line, col):
        """returns a list of the line, column and diagonals an element is in"""

        result = [self.line(line)]
        result.append(self.col(col))
        result.append(self.diagonal1(line + col))
        result.append(self.diagonal2(line + self.cols - 1 - col))

        return result


    def check_gameover(self):
        """checks if the game is over

        and returns either 0 if not finished, 3 if game draw or the winner(1/2)
        """

        # board is completely full? (draw)
        if 0 not in self.board[0]: return 3

        # horizontal
        for i in range(0, self.lines):
            line = self.line(i)
            if line.count("1111") > 0: return 1
            if line.count("2222") > 0: return 2

        # vertical
        for i in range(0, self.cols):
            col = self.col(i)
            if col.count("1111") > 0: return 1
            if col.count("2222") > 0: return 2

        # diagonal
        for i in range(3, self.lines + self.cols - 4):
            diag = self.diagonal1(i) + " " + self.diagonal2(i)
            if diag.count("1111") > 0: return 1
            if diag.count("2222") > 0: return 2

        # nothing found? game is not over then ...
        return 0


    def qcheck_gameover(self):
        """quickly checks if the last move has finished the game"""

        move = self.move_history[-1]
        line = 0
        while self.board[line][move[1]] == 0: line += 1
        for direction in self.vincinity(line, move[1]):
            if direction.count(4*str(move[0])) > 0: return move[0]
        return 0

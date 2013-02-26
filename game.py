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

"""Main module that manages the Connect Four game."""

from time import time, sleep
from copy import deepcopy as copy
from game_utils import ClearScreen
from board import Board
from ai2_player import ArtificialIntelligence


def Main(p1_is_ai, p2_is_ai, cols, lines):
    """main function, that manages the game"""

    # getting everything ready ...
    board = Board(cols, lines)
    if p1_is_ai: ai1 = ArtificialIntelligence(1)
    if p2_is_ai: ai2 = ArtificialIntelligence(2)
    turn = 0
    game_is_over = 0
    ai_msg = ""

    # execution of the game
    while board.check_gameover() == 0:
        turn += 1  # count the turns
        active_player = (turn + 1) % 2 + 1  # who is active?
        ClearScreen()
        if p1_is_ai or p2_is_ai:
            print(ai_msg); print("\n"),
        print(board)
        print(str(turn) + "th turn: It's player " \
              + str(active_player) + "'s turn!")
        while True:  # get a valid move from the player
            try:
                if (active_player == 1 and not p1_is_ai) or \
                   (active_player == 2 and not p2_is_ai):
                    # human player is active
                    move = input("Enter column: ")
                    if move == "b":
                        return
                    else:
                        move = int(move)
                else:
                    # ai player is active
                    print("AI is thinking ...")
                    ai_starttime = time()
                    if active_player == 1:
                        move = ai1.think(board)
                    if active_player == 2:
                        move = ai2.think(board)
                    ai_duration = time() - ai_starttime
                    ai_msg = "AI makes its move: col " + str(move) + " after " + \
                             str(round(ai_duration, 3)) + "s"

                if board.move_is_valid(move) == False:
                    raise ValueError
                break
            except ValueError:  # if move is not valid ...
                print("Not a valid move! Enter b to cancel the game ...")
        board.move(move, active_player)

    # end of the game, print the board and the results
    ClearScreen()
    print(board)
    if board.check_gameover() == 3:
        print("The game ends with a draw!")
    else:
        print("Player " + str(active_player) + " has won!")
    print("You'll be taken to the main menu soon ...")
    sleep(10)


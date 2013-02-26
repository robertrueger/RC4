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

"""Connect Four second generation artificial intelligence"""

from multiprocessing import Pool
from random import shuffle
from copy import deepcopy as copy
from board import Board


def think(board, player, depth = 3, multiprocessing = True):
    """main public function that figures out my best move"""

    if not isinstance(board, Board): raise TypeError
    enemy = player % 2 + 1

    # looking for simple solutions
    potential_move = simple_solution(board, player)
    if potential_move is not None: return potential_move

    if multiprocessing:
        # no simple solution found ... starting multiprocess recursion
        jobs = []
        for col in range(0, board.col_count()):
            temp_board = copy(board)
            if temp_board.move(col, player):
                jobs.append((copy(temp_board), enemy, depth - 1 ))
            else:
                jobs.append(None)
        workers = Pool()
        results = workers.map(rekthink, jobs)
        choices = []
        for result in results:
            if isinstance(result, Board):
                choices.append(situation_rating(result, player))
            else: choices.append(-32768)
        print(choices)
        move = 0
        for i in range(1, board.col_count()):
            if choices[i] > choices[move]:
                move = i
        return move
    else:
        # no simple solution found ... starting singleprocess recursion
        choices = []
        for col in range(0, board.col_count()):
            temp_board = copy(board)
            if temp_board.move(col, player):
                if depth > 0:
                    temp_board = rekthink((copy(temp_board), enemy, depth - 1))
                choices.append(situation_rating(temp_board, player))
            else: choices.append(-32768)
        print(choices)
        move = 0
        for i in range(1, board.col_count()):
            if choices[i] > choices[move]:
                move = i
        return move


def rekthink(job):
    """recursive thinking ...."""

    # move is not possible ... nothing to do ...
    if job is None: return None

    # expand data ...
    board = job[0]
    player = job[1]
    depth = job[2]
    enemy = player % 2 + 1

    # looking for simple solutions
    potential_move = simple_solution(board, player)
    if potential_move is not None:
        board.move(potential_move, player)
        return board

    # no simple solution found ... doing recursion ...
    choices = []
    for col in range(0, board.col_count()):
        tboard = copy(board)
        if tboard.move(col, player):
            if depth > 0:
                tboard = rekthink((copy(tboard), enemy, depth - 1))
            choices.append(situation_rating(tboard, player))
        else: choices.append(-32768)
    move = 0
    for i in range(1, board.col_count()):
        if choices[i] > choices[move]:
            move = i
    board.move(move, player)
    return board


def simple_solution(board, player):
    """tries to find a simple iv or db solution"""

    enemy = player % 2 + 1

    # can I win the game instantly?
    potential_move = instant_victory(board, player)
    if potential_move is not None: return potential_move

    # does the enemy force me to do a specific move?
    potential_move = instant_victory(board, enemy)
    if potential_move is not None: return potential_move

    # can I set up a double bind for the enemy?
    potential_move = double_bind_construction(board, player)
    if potential_move is not None: return potential_move

    # can the enemy set up a double bind for me?
    potential_move = double_bind_construction(board, enemy)
    if potential_move is not None: return potential_move

    return None


def instant_victory(board, player):
    """checks if it is possible for player to win instantly"""

    columns = list(range(0, board.col_count()))
    shuffle(columns)
    for col in columns:
        if board.move(col, player):
            result = board.qcheck_gameover()
            board.undo()
            if result == player:
                return col
    return None


def double_bind_construction(board, player):
    """checks if player can construct a double bind"""

    enemy = player % 2 + 1
    columns = list(range(0, board.col_count()))
    shuffle(columns)
    for col in columns:
        if board.move(col, player):
            # made the move to col ... checking the situation

            # did I help my enemy?
            if board.move(col, enemy):
                result = board.qcheck_gameover()
                board.undo()
                if result == enemy: board.undo(); break

            # counting the my enemy's binds
            binds = 0
            for col2 in columns:
                if board.move(col2, player):
                    result = board.qcheck_gameover()
                    board.undo()
                    if result == player:
                        binds += 1
                        if binds >= 2: board.undo(); return col

            # no db found with col ... tidying up
            board.undo()
    return None


def situation_rating(board, player):
    """calculates a rating for the players situation"""

    rating = 0
    enemy = player % 2 + 1

    for i in range(0, board.line_count()):
        rating += slice_rating(board.line(i), player)
        rating -= slice_rating(board.line(i), enemy)

    for i in range(0, board.col_count()):
        rating += slice_rating(board.col(i), player)
        rating -= slice_rating(board.col(i), enemy)

    for i in range(3, board.line_count() + board.col_count() - 4):
        rating += slice_rating(board.diagonal1(i), player)
        rating -= slice_rating(board.diagonal1(i), enemy)
        rating += slice_rating(board.diagonal2(i), player)
        rating -= slice_rating(board.diagonal2(i), enemy)

    return rating


def slice_rating(slc, player):
    """calculates the rating for a single slice of the board"""

    rating = 0
    p = str(player)

    # single token
    rating +=  1 * slc.count(p+"000")
    rating +=  2 * slc.count("0"+p+"00")
    rating +=  2 * slc.count("00"+p+"0")
    rating +=  1 * slc.count("000"+p)
    # double token
    rating +=  8 * slc.count(2*p+"00")
    rating +=  8 * slc.count(p+"0"+p+"0")
    rating +=  8 * slc.count(p+"00"+p)
    rating +=  8 * slc.count("0"+2*p+"0")
    rating +=  8 * slc.count("0"+p+"0"+p)
    rating +=  8 * slc.count("00"+2*p)
    rating += 16 * slc.count("0"+2*p+"00")
    rating += 16 * slc.count("00"+2*p+"0")
    rating += 16 * slc.count("0"+p+"0"+p+"0")
    # triple token
    rating += 128 * slc.count(3*p+"0")
    rating += 128 * slc.count(2*p+"0"+p)
    rating += 128 * slc.count(p+"0"+2*p)
    rating += 128 * slc.count("0"+3*p)
    rating += 512 * slc.count("0"+3*p+"0")
    # quad token = victory :)
    rating += 32768 * slc.count(4*p)

    return rating

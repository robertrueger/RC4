#!/usr/bin/env python2

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

"""Connect Four starting module and main menue."""

from game import Main
from game_utils import ClearScreen


exit = False
while exit != True:
    # print main menue
    ClearScreen()
    print("\n         ~~~Robert's Connect 4~~~")
    print("    (1) Multiplayer - play against each other")
    print("    (2) Singleplayer - play againt the AI")
    print("    (3) AI duel  - let two AIs battle each other")
    print("    (4) Quit")
    mode = 0
    while True:
        try:
            mode = int(input("    Selection: "))
            if mode < 1 or mode > 4:
                raise ValueError
            break
        except ValueError:
            print("    Not a valid selection!")
    ClearScreen()

    if mode == 1 or mode == 2 or mode == 3:  # do the configuration ...
        if mode == 1:
            print("   ~~~Multiplayer~~~")
            player1_is_ai, player2_is_ai = False, False
        elif mode == 2:
            print("   ~~~Singeplayer~~~")
            player1_is_ai, player2_is_ai = False, True
        elif mode == 3:
            print("   ~~~AI duel~~~")
            player1_is_ai, player2_is_ai = True, True
        print("How large would you like the board?")
        while True:
            try:
                cols = int(input("Columns: "))
                if cols < 4 or cols > 10:
                    raise ValueError
                break
            except ValueError:
                print("Number of columns must be between 4 and 10!")
        while True:
            try:
                lines = int(input("Rows: "))
                if lines < 4 or lines > 10:
                    raise ValueError
                break
            except ValueError:
                print("Number of rows must be between 4 and 10!")
        Main(player1_is_ai, player2_is_ai, cols, lines)  # start the game!

    else:  # user wants to quit
        exit = True
print("Bye!")

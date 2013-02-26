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

"""OOP interface for AI2 module"""

from copy import deepcopy as copy
from ai2 import think as inner_think


class ArtificialIntelligence:


    def __init__(self, player):
        """set me up as new AI player"""

        self.me = player
        self.enemy = self.me % 2 + 1


    def think(self, board, depth = 4):
        """generates a move for the player"""

        return inner_think(copy(board), self.me, depth)

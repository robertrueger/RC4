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

"""Collection of utilities."""

from os import system, name as os_name


def ClearScreen():
    """clears the screen"""
    if os_name == 'posix':
        system('clear')
    else:
        system('cls')

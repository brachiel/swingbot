#!/usr/bin/python
#python3

#    Copyright (c) 2016  Wanja Chresta
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import praw  # Python Reddit Api Wrapper, http://praw.readthedocs.io/en/stable/index.html, install using pip

passwd_file = './_passwd'


def get_login():
    fh = open(passwd_file, 'r')
    passwd_line = fh.readline().rtrim()  # First line without trailing \n
    fh.close()

    username, password = passwd_line.split(':')
    return username, password



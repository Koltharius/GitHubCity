"""Allows to get all data about a given GitHub City.

This module allow to developers to get all users of GitHub that have a
given city in their profile. For example, if I want getting all users
from London,. I will get all users that have London in their
profiles (they could live in London or not)

Author: Israel Blancas @iblancasa
Original idea: https://github.com/JJ/github-city-rankings
License:

The MIT License (MIT)
    Copyright (c) 2015-2017 Israel Blancas @iblancasa (http://iblancasa.com/)

    Permission is hereby granted, free of charge, to any person
    obtaining a copy of this software and associated documentation
    files (the Software), to deal in the Software
    without restriction, including without
    limitation the rights to use, copy, modify, merge,
    publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED AS IS, WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
    WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
    PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
    OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
    ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
    USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from __future__ import absolute_import
import json
import logging
import coloredlogs
import pystache

class GitHubRegion():
    def __init__(self):
        self.__users = []

    def addCity(self, fileName):
        with open(fileName) as data_file:
            data = json.load(data_file)
        self.__users.extend(data["users"])

    def export(self, template_file_name, output_file_name,
               sort="public", data=None, limit=0):
        """Export ranking to a file.

        Args:
            template_file_name (str): where is the template
                (moustache template)
            output_file_name (str): where create the file with the ranking
            sort (str): field to sort the users
        """
        exportedData = {}
        exportedUsers = self.getSortedUsers()

        if limit == 0:
            exportedData["users"] = exportedUsers
        else:
            exportedData["users"] = exportedUsers[:limit]
        exportedData["extraData"] = data

        with open(template_file_name) as template_file:
            template_raw = template_file.read()

        template = pystache.parse(template_raw)
        renderer = pystache.Renderer()

        output = renderer.render(template, exportedData)

        with open(output_file_name, "w") as text_file:
            text_file.write(output)

    def getSortedUsers(self, order="public"):
        """Return a list with sorted users.

        :param order: the field to sort the users.
            - contributions (total number of contributions)
            - public (public contributions)
            - private (private contributions)
            - name
            - followers
            - join
            - organizations
            - repositories
        :type order: str.
        :return: a list of the github users sorted by the selected field.
        :rtype: str.
        """
        if order == "contributions":
            self.__users.sort(key=lambda u: u["contributions"],
                              reverse=True)
        elif order == "public":
            self.__users.sort(key=lambda u: u["public"],
                              reverse=True)
        elif order == "private":
            self.__users.sort(key=lambda u: u["private"],
                              reverse=True)
        elif order == "name":
            self.__users.sort(key=lambda u: u["name"], reverse=True)
        elif order == "followers":
            self.__users.sort(key=lambda u: u["followers"], reverse=True)
        elif order == "join":
            self.__users.sort(key=lambda u: u["join"], reverse=True)
        elif order == "organizations":
            self.__users.sort(key=lambda u: u["organizations"],
                              reverse=True)
        elif order == "repositories":
            self.__users.sort(key=lambda u: u["repositories"],
                              reverse=True)
        return self.__users
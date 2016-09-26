#    This file is part of Foobar.
#
#    Foobar is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Foobar is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
#

import re
import urllib.request


class EndPatternNotFoundError(Exception):
    pass


def http_get(url):
    response = urllib.request.urlopen(url)
    encoding = response.headers.get_content_charset() or 'utf-8'
    return response.read().decode(encoding)


def pattern_parser(strings, start_pattern, search_pattern, end_pattern):
    r"""Search a list of strings for search_pattern between start_pattern and end_pattern and return all matched groups.

    Keyword arguments:
    start_pattern -- re.RegexObject - Start searching for search_pattern if this is found
    search_pattern -- re.RegexObject - A pattern containing named groups
    end_pattern -- re.RegexObject - Pattern which ends the matching

    Returns:
    [re.RegexObject] - List of dict of matched groups from search_pattern

    Exceptions raised:
    EndPatternNotFoundError -- end_pattern was not found

    Example:
        >>> pattern_parser(["Hello","This is the START","Some <Match>","<Another> match","THEEND","Good bye"],
        ...                 start_pattern=re.compile(r'\bSTART'),
        ...                 search_pattern=re.compile(r'<(?P<match>\w+)>'),
        ...                 end_pattern=re.compile(r'\bTHEEND\b'))
        [{'match': 'Match'}, {'match': 'Another'}]
    """

    matches = []
    is_matching = False

    for string in strings:
        if not is_matching and start_pattern.search(string):
            is_matching = True
            continue
        if is_matching and end_pattern.search(string):
            break

        if is_matching:
            m = search_pattern.search(string)
            if m:
                matches.append(m.groupdict())
    else:
        raise EndPatternNotFoundError(
            "Couldn't find end pattern after {} matches. Found start: {}".format(len(matches), is_matching))

    return matches

wcsvideos_start = re.compile(r'<h1>Latest West Coast Swing Pro Videos</h1>')
wcsvideos_search = re.compile(r'<a href="/video/(?P<videoid>\d+)/" data-toggle="modal" data-target="#videoModal" ' +
                              r'data-video_id="(?P<youtube_id>\w+)">(?P<title>[^<]+)</a></p>')
wcsvideos_end = re.compile(r'<nav class="text-center">')


def wcsvideos_list(url="http://www.wcsvideos.com/pros/all/"):
    html = http_get(url)

    video_matches = pattern_parser(html.split('\n'), wcsvideos_start, wcsvideos_search, wcsvideos_end)

    print(video_matches)


if __name__ == '__main__':
    import doctest
    doctest.testmod()


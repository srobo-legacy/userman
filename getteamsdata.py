#!/usr/bin/env python

import urllib

TEAMS_PAGE = 'https://www.studentrobotics.org/trac/wiki/2014/Teams?format=txt'

tmpfile, headers = urllib.urlretrieve(TEAMS_PAGE)

lines = []

with open(tmpfile) as f:
    for line in f:
        line = line.strip()

        if line == '= Registered Schools =':
            store_lines = True
            continue
        if line.startswith('='):
            store_lines = False
            continue

        if store_lines and len(line) > 0:
            lines.append(line)

team_map = {}

# ignore the header
for line in lines[1:]:
    if not line.startswith('||'):
        break
    parts = line.split('||', 4)
    x, tla, college_name, rest = [parts[i].strip() for i in xrange(4)]
    if not tla.startswith('\'\'\''):
        team_map[tla] = college_name

for tla, college_name in team_map.iteritems():
    print "{0},{1}".format(tla, college_name)

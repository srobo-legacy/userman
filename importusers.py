#!/usr/bin/python

import sys
import csv
import sr
import c_teams
import mailer

if len(sys.argv) != 2:
    print >>sys.stderr, "Usage: importusers.py users.csv"
    sys.exit(1)

for row in csv.reader(open(sys.argv[1], 'r')):
    print repr(row)
    newname = sr.new_username(row[2], row[3], row[4])
    u =sr.users.user(newname)
    if u.in_db:
        print >>sys.stderr, "User {0} already exists".format(newname)
        sys.exit(1)

    college = sr.group(row[2])
    if not college.in_db:
        print >>sys.stderr, "Group {0} doesn't exist".format(row[2])
        sys.exit(1)

    team = sr.group(row[6])
    if not team.in_db:
        print >>sys.stderr, "Group {0} doesn't exist".format(row[2])
        sys.exit(1)

    students = sr.group('students')
    if not students.in_db:
        print >>sys.stderr, "Group {0} doesn't exist".format('students')
        sys.exit(1)

    # NB: strange save order because I encountered some pyenv error without the
    # intervening u.save; didn't have time to investigate.
    u.cname = row[3]
    u.sname = row[4]
    u.email = row[5]
    u.save()
    u.set_lang('english')
    u.save()

    college.user_add(u)
    college.save()

    team.user_add(u)
    team.save()

    students.user_add(u)
    students.save()

    print "User {0} created".format(newname)

    mailer.send_template("welcome", u, { "PASSWORD": u.init_passwd } )
    print "User {0} mailed".format(newname)

#!/usr/bin/python
# By Alex Monk, based on importusers.py by Jeremy Morse

import sys, yaml, os
import sr, mailer, c_teams
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("teamsdir", help="Working dir for teams.git")
args = parser.parse_args()

TEAMS_DIR = args.teamsdir

# Test whether TEAMS_DIR exists
try:
    os.stat(TEAMS_DIR)
except OSError:
    print >>sys.stderr, "Couldn't stat \"{0}\"".format(TEAMS_DIR)
    sys.exit(1)

# Suck a list of teams out of TEAMS_DIR
team_yaml = []
def add_to_team_yaml(arg, dirname, fnames):
    if dirname == TEAMS_DIR:
        for fname in fnames:
            team_yaml.append(fname)

os.path.walk(TEAMS_DIR, add_to_team_yaml, None)

team_yaml = [x for x in team_yaml if ".yaml" in x]

# Filter team records for those who actually posess a team this year.
def is_taking_part_yaml(fname):
    with open(os.path.join(TEAMS_DIR, fname)) as file:
        data = yaml.safe_load(file)
        if not data["teams"]:
            return False

        return True
    # On failure
    print >>sys.stderr, "Couldn't open {0}".format(fname)
    sys.exit(1)

team_yaml = [x for x in team_yaml if is_taking_part_yaml(x)]

print >>sys.stderr, "EUNIMPLEMENTED"
sys.exit(1)

for college_id in set(teamTLAs): # Remove duplicates
	try:
		teamFile = open(TEAMS_DIR + '/' + college_id + '.yaml')
	except IOError:
		print("Error while trying to read file for college " + college_id + ", skipping...")
		continue

	collegeInfo = yaml.load(teamFile)
	if 'contacts' not in collegeInfo or len(collegeInfo['contacts']) == 0:
		print("College " + college_id + " have no contacts set, skipping...")
		continue

	contact = collegeInfo['contacts'][0] # Only the first contact gets an account
	print("Working on " + college_id)
	first_name, last_name = contact['name'].split(' ')

	newname = sr.new_username(college_id, first_name, last_name)
	u = sr.users.user(newname)
	if u.in_db:
		print >>sys.stderr, "User {0} already exists".format(newname)
		sys.exit(1)

	college = c_teams.get_college(college_id)
	if not college.in_db:
		print >>sys.stderr, "College group {0} doesn't exist".format(college.name)
		sys.exit(1)

	teams = collegeInfo['teams']
	teamGroups = []
	for team in teams:
		teamGroup = c_teams.get_team(team)
		teamGroups.append(teamGroup)
		if not teamGroup.in_db:
			print >>sys.stderr, "Group {0} doesn't exist".format(teamGroup.name)
			sys.exit(1)

	teachers = sr.group('teachers')
	if not teachers.in_db:
		print >>sys.stderr, "Group {0} doesn't exist".format('teachers')
		sys.exit(1)

	u.cname = first_name
	u.sname = last_name
	u.email = contact['email']
	u.save()
	u.set_lang('english')
	u.save()

	college.user_add(u)
	college.save()

	for team in teamGroups:
		team.user_add(u)
		team.save()

	teachers.user_add(u)
	teachers.save()

	print "User {0} created".format(newname)

	mailer.send_template("welcome", u, { "PASSWORD": u.init_passwd } )
	print "User {0} mailed".format(newname)

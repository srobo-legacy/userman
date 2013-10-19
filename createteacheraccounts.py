# By Alex Monk, based on importusers.py by Jeremy Morse
#!/usr/bin/python

import sys, csv, sr, mailer, yaml, os, c_teams

for filename in os.listdir('priv/teams'):
	data = yaml.load(open('priv/teams/' + filename))
	if not 'contacts' in data.keys():
		continue
	for contact in data['contacts']:
		college_id = data['teams'][0] # If there's multiple, just use the first.
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

		teams = data['teams']
		teamGroups = []
		for team in teams:
			teamGroup = c_teams.get_team(team)
			if not teamGroup.in_db:
				print >>sys.stderr, "Group {0} doesn't exist".format(team.name)
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

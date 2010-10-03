#!/bin/env python
import smtplib, getpass
import sr

fromaddr = "rspanton@studentrobotics.org"
#toaddr = "rspanton@gmail.com"
smtpserver = "smtp.ecs.soton.ac.uk"
username = "rds"
subject = "Welcome to Student Robotics" 

def def_psource():
    return getpass.getpass("SMTP Server password:")

psource = def_psource

def set_psource( fn ):
    global psource
    psource = fn

the_pass = None
def get_pass():
    global the_pass
    if the_pass == None:
        the_pass = psource()
    return the_pass

def email( fromaddr, toaddr, subject, msg, smtp_pass = None ):
    if smtp_pass == None:
        smtp_pass = get_pass()

    msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s" % (fromaddr, toaddr, subject, msg)

    server = smtplib.SMTP(smtpserver)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, smtp_pass)
    print server.sendmail(fromaddr, toaddr, msg)
    try:
        server.quit()
    except smtplib.sslerror:
        pass

def email_pass( user,p, smtp_pass = None ):
    msg = """Hello %s,

You now have a shiny new Student Robotics account.  This will let you
access the Student Robotics facilities, including the forums and the
software development environment for your robot.

Your username is: %s
Your password is: %s

Your registered email address is %s.

You can change your password at:

	https://www.studentrobotics.org/password

If you have any problems with your account then please get in touch by
emailing accounts@studentrobotics.org.

So go introduce yourself to everyone on the forums, and enjoy building
your robots.

Thanks,

The Student Robotics Team

""" % ( user.cname, user.username, p, user.email )

    email( fromaddr, user.email, subject, msg, smtp_pass )


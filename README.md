# Userman

This is Userman, a command line interface to the LDAP users database for
[Student Robotics](http://studentrobotics.org) (SR).

## Setting Up

In order for Userman to make any sense of the LDAP database you point it at,
the database needs to be structured as detailed on the [LDAP](https://www.studentrobotics.org/trac/wiki/LDAP)
page of SR's trac wiki. There's also a [guide](https://www.studentrobotics.org/trac/wiki/PrepareLDAP)
on how to do this on various systems, but by far the simplest way is to
grab a development copy of SR's server using [vagrant](http://github.com/samphippen/badger-vagrant).

Once the LDAP is valid, you'll need to set the connection details in your checkout,
which is done by creating a `local.ini` inside the `srusers` submodule
(checked out into the `sr` directory). This should be a modified copy of the
`config.ini` file in the same directory, see that file for details on what
to change.

## Basic Usage

Get help:

    ./userman

List all the users on the system:

    ./userman user list

Create a new group called `my-group`:

    ./userman group create my-group

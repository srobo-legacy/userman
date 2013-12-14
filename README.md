# Userman

This is Userman, a command line interface to the LDAP users database for
[Student Robotics](http://studentrobotics.org) (SR).

## Setting Up

In order for Userman to make any sense of the LDAP database you point it at,
the database needs to be structured as detailed on the [LDAP](https://www.studentrobotics.org/trac/wiki/LDAP)
page of SR's trac wiki. There's also a [guide](https://www.studentrobotics.org/trac/wiki/PrepareLDAP)
on how to do this on various systems, but by far the simplest way is to
grab a development copy of SR's server using [vagrant](http://github.com/samphippen/badger-vagrant).

By default it will connect to localhost, and prompt for the password of the
`Manager` account. If you want it to save the password, or connect to a
different host, this is configurable (see the Configuration section below).

## Basic Usage

Get help:

    ./userman

List all the users on the system:

    ./userman user list

Create a new group called `my-group`:

    ./userman group create my-group

## Configuration

Additional configuration can be achieved by adding `local.ini` files next to
the respective `config.ini` that they intend to override. There are two such
configs, one in the root of the project and one within the `srusers` submodule
(checked out into the `sr` directory). As it is the `srusers` submodule that
handles the actual connection to LDAP, it is there that any connection (ie,
host, username or password) related changes must be made.

In either case, the `local.ini` should be a modified copy of the `config.ini`
it will override, though any keys that are unchanged may be omitted. See the
details in each `config.ini` for which keys do what.

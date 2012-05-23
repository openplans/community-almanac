Community Almanac
====================

This is the source code that runs Community Almanac:
http://www.communityalmanac.org/

Installation and Setup
======================

First, install the software:
----------------------------

(You must have Python 2, at least version 2.5.
Note that python 3 is NOT supported!)

 virtualenv env
 mkdir -p env/src
 cd env
 source bin/activate
 pip install -r https://raw.github.com/openplans/community-almanac/master/almanac-requirements.txt

* Note that you can most likely get away with just checking
out the source and running `python setup.py develop`,
but the almanac-requirements.txt file
represents the known good set of packages that work with the almanac.

Next, set up the database.
--------------------------

The community almanac requires a postgres database to be set up with
postgis spatial extensions. (A typical way to do so would be with
commands like:

  createuser almanac
  createdb -O almanac -T template_postgis almanac

Assuming the database is set up already, there is a development.ini
config file provided for you as a starting point. In particular,
ensure that the database name and username/password are set correctly.
Then run this command:

  cd env/src/communityalmanac
  paster setup-app development.ini

Make note of the "initial admin account" username and password
that is printed at the end; you'll want that to log in to the admin UI.


Run it.
-------

  cd env/src/communityalmanac
  paster serve development.ini


Explore it
-----------

  Point your browser at http://127.0.0.1:4000

  For the admin UI, browse to http://127.0.0.1:4000/admin
  ... then at the login form, click "Existing user" and enter
  the admin username and password that was printed when you ran `paster setup-app` above


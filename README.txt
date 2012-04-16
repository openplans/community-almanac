Installation and Setup
======================

First, install the software:
----------------------------

(You must have Python 2, at least version 2.5.
Note that python 3 is NOT supported!)

python2 /path/to/virtualenv env
mkdir env/src
hg clone https://source.openplans.org/hg/communityalmanac env/src/communityalmanac
/path/to/pip install -r env/src/communityalmanac/almanac-requirements.txt -E env
cd env
source bin/activate

* Note that you can most likely get away with just running setup.py
develop on the source, but the almanac-requirements.txt file
represents the known good set of packages that work with the almanac.

Next, set up the database.
--------------------------

The community almanac requires a postgres database to be set up with
postgis spatial extensions. (A typical way to do so would be with
commands like `createuser almanac; createdb -O almanac -T
template_postgis almanac`).

Assuming the database is set up already, there is a development.ini
config file provided for you as a starting point. In particular,
ensure that the database name and username/password are set correctly.
Then run this command:

$ paster setup-app development.ini


Run it.
-------

paster serve development.ini

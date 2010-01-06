# Community Almanac - A place for your stories.
# Copyright (C) 2009  Douglas Mayle, Robert Marianski,
# Andy Cochran, Chris Patterson

# This file is part of Community Almanac.

# Community Almanac is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# Community Almanac is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with Community Almanac.  If not, see <http://www.gnu.org/licenses/>.
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

import sys
# We monkeypatch setuptools to perform script installs the way distutils does.
# Calling pkg_resources is too time intensive for a serious command line
# applications.
def install_script(self, dist, script_name, script_text, dev_path=None):
    self.write_script(script_name, script_text, 'b')

if sys.platform != 'win32' and 'setuptools' in sys.modules:
    # Someone used easy_install to run this.  I really want the correct
    # script installed.
    import setuptools.command.easy_install
    setuptools.command.easy_install.easy_install.install_script = install_script

# lxml has some problems intalling under OS X, so we force a static install of
# libxml to make things easier.
if sys.platform == 'darwin':
    import os
    os.environ['STATIC_DEPS'] = 'true'

setup(
    name='communityalmanac',
    version='0.1',
    description='A place for your stories.',
    long_description="""\
    Community Almanac is a way to capture and share the oral history of your
    town.
""",
    author='Douglas Mayle, Robert Marianski, Andy Cochran, Chris Patterson',
    author_email='',
    license='GNU Affero General Public License v3',
    url='http://source.openplans.org/hg/communityalmanac',
    install_requires=[
        "Pylons>=0.9.7",
        "SQLAlchemy>=0.5",
        "psycopg2>=2.0.10",
        "geopy==0.93dev-r84",
        "shapely>=1.0.14",
        "pyproj>=1.8.5",
        "formalchemy==1.2",
        "repoze.what>=1.0.8",
        "repoze.what-pylons>=1.0",
        "repoze.what.plugins.sql>=1.0rc1",
        "repoze.who>=1.0.14",
        "repoze.who.plugins.openid>=0.5",
        "repoze.who.plugins.sa>=1.0rc2",
        "lxml>=2.2",
        "mailer>=0.5",
        "PIL==1.1.6",
        "recaptcha-client>=1.0.3",
        "bcrypt>=0.1",
    ],
    dependency_links=[
        "https://source.openplans.org/eggs/geopy-0.93dev-r84.tar.gz",
        "http://dist.repoze.org/PIL-1.1.6.tar.gz",
        "https://source.openplans.org/eggs/FormAlchemy-1.2.tar.gz",
        "http://www.mindrot.org/files/py-bcrypt/py-bcrypt-0.1.tar.gz#egg=bcrypt-0.1",
    ],
    setup_requires=["PasteScript>=1.6.3"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'communityalmanac': ['i18n/*/LC_MESSAGES/*.mo']},
    #message_extractors={'communityalmanac': [
    #        ('**.py', 'python', None),
    #        ('templates/**.mako', 'mako', {'input_encoding': 'utf-8'}),
    #        ('public/**', 'ignore', None)]},
    zip_safe=False,
    paster_plugins=['PasteScript', 'Pylons'],
    entry_points="""
    [paste.app_factory]
    main = communityalmanac.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
    scripts=['scripts/ca'],
    classifiers=[
      'Development Status :: 1 - Planning',
      'Environment :: Web Environment',
      'Framework :: Pylons',
      'Intended Audience :: Other Audience',
      'License :: OSI Approved :: GNU Affero General Public License v3',
      'Operating System :: OS Independent',
      'Programming Language :: Python :: 2.5',
      'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary',
      'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
)

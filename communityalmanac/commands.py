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

# The minimum number of modules necessary for a reload monitor
import os
import sys
import signal

from optparse import OptionParser

def launch_and_watch_child(args):
    """if hasattr(os, 'fork'):
        # OS X Spits out ugly warnings if you import the webbrowser module
        # after forking.  Since we're going to fork, I'll preimport webbrowser.
        import webbrowser

        # Nice and easy...
        child = os.fork()
        if child == 0:
            return None, child
        childpid, exit_code = os.waitpid(child, 0)

        # Because of the way waitpid functions, we have to shift right by eight
        # to get the kind of exit code we expect.
        return exit_code >> 8, child"""

    from communityalmanac.lib import spatialite
    from subprocess import Popen
    child = Popen(args)
    exit_code = child.wait()
    return exit_code, child.pid

def _server_args(args, nolaunch=False):
    if hasattr(os, 'fork'):
        # We care about the in memory arguments
        args.fragile = True
        args.debug = False
        if nolaunch:
            args.nolaunch = True
        return

    # We have to much around with the actual arguments to pass down.
    import sys

    my_python = sys.executable
    # On windows, we may have to fix this up if there is a space somewhere
    # in the path.  I'm inclined to just escape the space, and hope that
    # works.  PasteScript command uses win32api.GetShortPathName to find
    # the FAT16 equivalent filename.  I hope we can avoid that mess.
    if sys.platform == 'win32' and ' ' in my_python:
        my_python = my_python.replace(' ', '\\ ')

    server_args = [my_python] + sys.argv

    # We don't want the server process to become a reload monitor.
    if '--debug' in server_args:
        server_args.remove('--debug')
    if '-d' in server_args:
        server_args.remove('-d')

    # Setup the server process to quit out on any changes.
    if '-f' not in server_args and '--fragile' not in server_args:
        server_args.append('--fragile')

    if nolaunch:
        if '-n' not in server_args and '--nolaunch' not in server_args:
            server_args.append('--nolaunch')
    return server_args

def main():
    parser = OptionParser(description="Community Almanac: A place to tell your stories.")

    parser.add_option(
        '-d', '--debug', action='store_true', default=False,
        help='Start community almanac in debugging mode.  This causes '
        'community almanac to monitor it\'s own source files and reload if '
        'they have changed.  Normally, only community almanac developers will '
        'ever have need of this functionality.')

    parser.add_option(
        '-f', '--fragile', action='store_true', default=False,
        help='INTERNAL USE ONLY.  When specified, start a thread that watches '
        'Community Almanac\'s source files.  If any change, then quit this '
        'process.')

    parser.add_option(
        '-n', '--nolaunch', action='store_true', default=False,
        help='Don\'t launch a web browser after starting the http server.')

    parser.add_option(
        '-p', '--port', type=int, default=4000,
        help='The port to serve on (by default: 4000).  If this port is in '
        'use, community almanac will try to randomly select an open port.')

    parser.add_option(
        '-i', '--ip', default='0.0.0.0',
        help='The IP address to listen on. Defaults to 0.0.0.0, which means '
        'all IPv4 addresses')

    parser.add_option(
        '-u', '--url', default='postgres://almanac:almanac@localhost/almanac',
        help='The DB url to pass to sqlalchemy. It defaults to '
        '"postgres://almanac:almanac@localhost/almanac"')

    parser.add_option(
        '-s', '--setup', action='store_true', default=False,
        help='Run the community almanac setup.  This creates any necessary models.')

    parser.add_option(
        '-m', '--map-key',
        default='ABQIAAAArBPF8riaRhqOCRInVOpLVhS7l0GBSa1x8uTWSQog_urT4TWq5xQAsIXoWoBjWzF7uvuoy8WT3pGQQA',
        help='The google maps api key to use')

    args = parser.parse_args()[0]

    config = {
        'use': 'egg:communityalmanac',
        'full_stack': 'true',
        'static_files': 'true',

        'cache_dir': os.path.join(os.getcwd(), 'data'),
        'beaker.session.key': 'almanac',
        'beaker.session.secret': 'somesecret',

        'sqlalchemy.url': args.url,
        'map_key': args.map_key,
    }

    if args.setup:
        conf = type('TempConfig', (object,), dict(global_conf=config, local_conf=config))
        from communityalmanac.websetup import setup_app
        setup_app(None, conf, {})
        sys.exit(0)
    # We're gonna implement magic reload functionality, as seen in paster
    # serve. (Thanks, Ian Bicking, for the code and the explanation of what to
    # do.)

    # When this command is called with --debug, it does no actual serving.  It
    # opens a new process with a special flag that will tell Community Almanac
    # to launch in 'fragile mode'.  This means that it will call
    # paste.reload.install(), which starts a thread that kills the process if
    # any of it's files change.

    # Meanwhile, back at the ranch (this process) we'll watch to see if our
    # subprocess dies and simply launch it again.  At the same time, we'll
    # watch for a Ctrl-C so that the user can interrupt us (and by extension,
    # the server.)

    if args.debug:

        nolaunch = args.nolaunch
        while True:
            child = None
            try:
                try:
                    print "Launching server process"
                    exit_code, child = launch_and_watch_child(_server_args(args, nolaunch))
                    if not child:
                        break

                    # We only let nolaunch be False on the first subprocess launch.
                    # After that, we never want to launch a webbrowser.
                    nolaunch = True
                except (SystemExit, KeyboardInterrupt):
                    "^C Pressed, shutting down server"
                    return
            finally:
                if child and hasattr(os, 'kill'):
                    # Apparantly, windows will litter processes in the case of
                    # catastrophic failure.
                    try:
                        os.kill(child, signal.SIGTERM)
                    except (OSError, IOError):
                        pass
            if exit_code != 3:
                # The child exited non-normally, so we will too.
                return exit_code


    if args.fragile:
        # This simple form does not work in jython, so I should fix that, since
        # the code is already written into paste.serve
        from paste import reloader
        # Do we need to allow a way to slow this down?  Defaults to checking
        # once per second.
        reloader.install()
        # If we ever add a config file, we need to add that to the watch list
        # like this:
        # reloader.watch_file(my_config_file)

    from communityalmanac.config.middleware import make_app
    app = make_app({'debug':(args.debug or args.fragile) and 'true' or 'false'}, **config)

    import webbrowser
    def webhelper(url):
        """\
        Curry the webbrowser.open method so that we can cancel it with a
        threaded timer."""
        def _launch_closure():
            webbrowser.open(url)
        return _launch_closure

    import socket
    from paste.httpserver import serve

    # Paste's httpserver doesn't return once it's started serving (which is
    # pretty normal).  The only problem is that we don't know if it
    # successfully captured the port unless it didn't return.  We don't want to
    # open the user's webbrowser unless we're successfully serving, so it's
    # sort of a chicken and egg problem.  We'll start a timer with a half
    # second delay (forever in computer time) in another thread.  If the server
    # returns, we'll cancel the timer, and try again.
    if not args.nolaunch:
        from threading import Timer
        safelaunch = Timer(0.5, webhelper('http://%s:%d/' % (args.ip, args.port)))
        safelaunch.start()

    try:
        serve(app, host=args.ip, port=args.port)
    except socket.error, e:
        safelaunch.cancel()
        print "Unable to serve on port %d : Error message was: %s" % (args.port, e[1])

if __name__ == '__main__':
    main()

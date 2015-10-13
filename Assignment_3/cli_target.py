#!/usr/bin/env python2

########################################################################
#                                                                      #
#  This code is part of Android Explorer                               #
#  Code written by Thuan Song Teoh except where noted.                 #
#                                                                      #
#  Permission is hereby granted, free of charge, to any person         #
#  obtaining a copy of this software and associated documentation      #
#  files (the "Software"), to deal in the Software without             #
#  restriction, including without limitation the rights to use,        #
#  copy, modify, merge, publish, distribute, sublicense, and/or sell   #
#  copies of the Software, and to permit persons to whom the           #
#  Software is furnished to do so.                                     #
#                                                                      #
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,     #
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES     #
#  OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND            #
#  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR        #
#  ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF      #
#  CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION  #
#  WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.     #
#                                                                      #
########################################################################

import cmd
from core.core_cli import *
from core.core_host import *
from core.core_target import *

def cli_deco(connected=True):
    """cli_deco(bool)
    Decorator for command line. Handles exception and prints in a
    fixed format.

    """
    def decorate(func):
        def wrapper(self,args):
            # Remind to connect if not logged in yet
            if connected and self._remote.connected is False:
                print '*** Error: Please connect first.'
                return

            try:
                return func(self,*args) 
            except Exception as e:
                print '*** Error: '+str(e)
        # Inherit all documentation strings
        wrapper.__doc__=func.__doc__
        return wrapper
    return decorate

class Cli_target(Cli):
    """Command line inteface for ADB sync."""
    def __init__(self):
        """Initialises command line interface.
        """
        cmd.Cmd.__init__(self)
        self.prompt='ADB > '
        self._remote=Core_target()
        if self._remote.connected == True:
            print '[Connected]'
        else:
            print '[Not connected]'
        self._local=Core_host()

    @cli_deco(connected=False)
    def do_connect(self):
        """Connect to a device.
        """
        self._remote.connect()
        if self._remote.connected == True:
            print '[Connected]'
        else:
            print '*** Error: Device not found.'

    @cli_deco()
    def do_status(self):
        """Get disk usage info of device.
        """
        data=self._remote.df()
        for i in data:
            print i
            print 'Size: '+data[i]['Size']
            print 'Used: '+data[i]['Used']
            print 'Free: '+data[i]['Free']

    @cli_deco()
    def do_ls(self,args=None):
        """Lists contents of device directory. If no arguments are given, \
uses current path instead.

        Examples:
        ADB > ls
        ADB > ls /Test
        """
        return Cli.do_ls(self,args)

    @cli_deco(connected=False)
    def do_lls(self,args=None):
        """Lists contents of local directory. If no arguments are given, \
uses current path instead.

        Examples:
        ADB > lls
        ADB > lls ~/foo
        """
        return Cli.do_lls(self,args)

    @cli_deco()
    def do_mkdir(self,args):
        """Creates a folder in device.

        Example:
        ADB > mkdir /foo
        """
        return Cli.do_mkdir(self,args)

    @cli_deco()
    def do_rm(self,args):
        """Deletes a file/folder from device.

        Examples:
        ADB > rm /foo
        ADB > rm /bar.txt
        """
        return Cli.do_rm(self,args)

    @cli_deco()
    def do_cp(self,_from,_to):
        """Copies a file/folder in device to another location in device.

        Examples:
        ADB > cp /foo /bar
        ADB > cp /foo.txt /bar
        """
        return Cli.do_cp(self,_from,_to)

    @cli_deco()
    def do_mv(self,_from,_to):
        """Moves a remote file/folder to another location in device. \
File/folder name must be included.

        Examples:
        ADB > mv /foo /bar
        ADB > cp /foo.txt /bar/foo.txt
        """
        return Cli.do_mv(self,_from,_to)

    @cli_deco()
    def do_pwd(self):
        # Shows current remote working directory
        return Cli.do_pwd(self)

    @cli_deco(connected=False)
    def do_lpwd(self):
        # Shows current local working directory
        return Cli.do_lpwd(self)

    @cli_deco()
    def do_cd(self,args=None):
        """Change current device working directory. If no arguments \
are given, changes to home directory.

        Examples:
        ADB > cd /foo
        ADB > cd ..
        """
        return Cli.do_cd(self,args)

    @cli_deco(connected=False)
    def do_lcd(self,args=None):
        """Change current local working directory. If no arguments \
are given, changes to home directory.

        Examples:
        ADB > lcd ~/foo
        ADB > lcd ..
        """
        return Cli.do_lcd(self,args)

    @cli_deco()
    def do_put(self,_from,_to):
        """Uploads file from local to device. File name must be included.

        Examples:
        ADB > put ~/foo.txt /bar.txt
        ADB > upload ~/foo.txt /bar.txt
        """
        return Cli.do_put(self,_from,_to)

    @cli_deco()
    def do_get(self,_from,_to):
        """Downloads file from device to local. File name must be included.

        Examples:
        ADB > get /foo.txt ~/bar.txt
        ADB > download /foo.txt ~/bar.txt
        """
        return Cli.do_get(self,_from,_to)

    @cli_deco(connected=False)
    def do_help(self,args=None):
        # List available commands and help text
        return Cli.do_help(self,args)

    def do_exit(self,args):
        """Terminates program.

        Examples:
        ADB > exit
        ADB > quit
        """
        print
        return True

    # For command line magic only)
    def do_EOF(self,args):
        """Hit Ctrl+D to exit program.
        """
        return self.do_exit(None)

    # Aliases
    do_quit=do_exit
    do_upload=do_put
    do_download=do_get

def main():
    term=Cli_target()
    term.cmdloop()

if __name__ == '__main__':
    main()

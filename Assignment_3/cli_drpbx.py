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

import os
import cmd
from core.core_cli import *
from core.core_host import *
from core.core_drpbx import *

def cli_deco(login=True):
    """cli_deco(bool)
    Decorator for command line. Handles exception and prints in a
    fixed format.

    """
    def decorate(func):
        def wrapper(self,args):
            # Remind to login if not logged in yet
            if login and self._remote.client is None:
                print '*** Error: Please login first.'
                return

            try:
                return func(self,*args) 
            except Exception as e:
                print '*** Error: '+str(e)
        # Inherit all documentation strings
        wrapper.__doc__=func.__doc__
        return wrapper
    return decorate

class Cli_drpbx(Cli):
    """Command line inteface for Dropbox sync."""
    def __init__(self):
        """Initialises command line interface.
        """
        cmd.Cmd.__init__(self)
        self.prompt='core_drpbx > '
        self._remote=Core_drpbx()
        self._local=Core_host()
        if self._remote.client != None:
            print '[Logged in]'
        else:
            print '[Not logged in]'

    @cli_deco(login=False)
    def do_login(self):
        """Login into a Dropbox account.
        """
        auth_url=self._remote.get_auth_url()
        print '1. Please go to: '+auth_url
        print '2. Click \"Allow\" (might have to login first).'
        print '3. Copy the authorisation code.'
        code=raw_input('Enter the authorisation code here: ').strip()
        self._remote.login(code)

    @cli_deco()
    def do_logout(self):
        """Logout from a Dropbox account.
        """
        self._remote.logout()

    @cli_deco()
    def do_status(self):
        """Get quota info of Dropbox account.
        """
        data=self._remote.acc_info()
        print 'Total: '+data[0]
        print 'Used: '+data[1]

    @cli_deco()
    def do_ls(self,args=None):
        """Lists contents of remote directory. If no arguments are given, \
uses current path instead.

        Examples:
        Drpbx > ls
        Drpbx > ls /Test
        """
        return Cli.do_ls(self,args)

    @cli_deco(login=False)
    def do_lls(self,args=None):
        """Lists contents of local directory. If no arguments are given, \
uses current path instead.

        Examples:
        Drpbx > lls
        Drpbx > lls ~/foo
        """
        return Cli.do_lls(self,args)

    @cli_deco()
    def do_mkdir(self,args):
        """Creates a folder in remote.

        Example:
        Drpbx > mkdir /foo
        """
        return Cli.do_mkdir(self,args)

    @cli_deco()
    def do_rm(self,args):
        """Deletes a file/folder from remote.

        Examples:
        Drpbx > rm /foo
        Drpbx > rm /bar.txt
        """
        return Cli.do_rm(self,args)

    @cli_deco()
    def do_cp(self,_from,_to):
        """Copies a remote file/folder to another remote location.

        Examples:
        Drpbx > cp /foo /bar
        Drpbx > cp /foo.txt /bar
        """
        return Cli.do_cp(self,_from,_to)

    @cli_deco()
    def do_mv(self,_from,_to):
        """Moves a remote file/folder to another remote location. File/folder \
name must be included.

        Examples:
        Drpbx > mv /foo /bar
        Drpbx > cp /foo.txt /bar/foo.txt
        """
        return Cli.do_mv(self,_from,_to)

    @cli_deco()
    def do_pwd(self):
        return Cli.do_pwd(self)

    @cli_deco(login=False)
    def do_lpwd(self):
        return Cli.do_lpwd(self)

    @cli_deco()
    def do_cd(self,args=None):
        """Change current remote working directory. If no arguments \
are given, changes to root directory.

        Examples:
        Drpbx > cd /foo
        Drpbx > cd ..
        """
        return Cli.do_cd(self,args)

    
    @cli_deco(login=False)
    def do_lcd(self,args=None):
        """Change current remote working directory. If no arguments \
are given, changes to root directory.

        Examples:
        Drpbx > cd /foo
        Drpbx > cd ..
        """
        return Cli.do_lcd(self,args)

    @cli_deco()
    def do_put(self,_from,_to):
        """Uploads file from local to remote. File name must be included.

        Examples:
        Drpbx > put ~/foo.txt /bar.txt
        Drpbx > upload ~/foo.txt /bar.txt
        """
        return Cli.do_put(self,_from,_to)

    @cli_deco()
    def do_get(self,_from,_to):
        """Downloads file from remote to local. File name must be included.

        Examples:
        Drpbx > get /foo.txt ~/bar.txt
        Drpbx > download /foo.txt ~/bar.txt
        """
        return Cli.do_get(self,_from,_to)

    @cli_deco(login=False)
    def do_help(self,args=None):
        return Cli.do_help(self,args)

    def do_exit(self,args):
        """Terminates program.

        Examples:
        Drpbx > exit
        Drpbx > quit
        """
        if self._remote.client != None:
            opt=raw_input('Do you want to logout? [Y] or N: ')
            print 
            if opt == 'Y':
                self._remote.logout()
                return True
            else:
                return True
        else:
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
    term=Cli_drpbx()
    term.cmdloop()

if __name__ == '__main__':
    main()

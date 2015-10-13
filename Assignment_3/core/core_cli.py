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
import shlex

class Cli(cmd.Cmd):
    # Main command line inteface (CLI) class. Other CLIs will inherit this.
    def do_ls(self,args=None):
        # Lists file in remote
        out=self._remote.ls(args)
        print '\n'.join(out)

    def do_lls(self,args=None):
        # Lists file in local
        out=self._local.ls(args)
        print '\n'.join(out)

    def do_mkdir(self,args):
        # Creates folder in remote
        self._remote.mkdir(args)

    def do_rm(self,args):
        # Deletes a file/folder in remote
        self._remote.rm(args)

    def do_cp(self,_from,_to):
        # Copies a remote file/folder to another remote location
        self._remote.cp(_from,_to)

    def do_mv(self,_from,_to):
        # Moves a remote file/folder to another remote location
        self._remote.mv(_from,_to)

    def do_pwd(self):
        """Shows current device working directory.
        """
        print self._remote.pwd()

    def do_lpwd(self):
        """Shows current local working directory.
        """
        print self._local.pwd()

    def do_cd(self,args=None):
        # Changes current remote working directory
        self._remote.cd(args)

    def do_lcd(self,args=None):
        # Changes current local working directory
        self._local.cd(args)

    def do_put(self,_from,_to):
        # Uploads a file from local to remote
        self._remote.upload(_from,_to)

    def do_get(self,_from,_to):
        # Downloads a file from remote to local
        self._remote.download(_from,_to)

    def do_help(self,args=None):
        """List available commands with "help" or detailed help with "help cmd".
        """
        all_names=dir(self)
        if args == None:
            cmd=[name[3:] for name in all_names if 'do_' in name]
            cmd.sort()

            print 'More detailed help with "help cmd"'
            print 'Available commands:'
            print '==================='
            print ' '.join(cmd)
        else:
            cmd=getattr(self,'do_'+args)
            print cmd.__doc__

    # Methods below are for command line magic only)
    def emptyline(self):
        # Default behaviour: Runs previous command if hit Enter with no
        # commands. Since we are dealing with files, disable to prevent
        # unintentional actions.
        pass

    def parseline(self,args):
        # Default parseline is not flexible enough, does not take account of
        # quotes, so use shlex instead
        parts=shlex.split(args)
        if len(args) == 0:
            return None,None,args
        else:
            return parts[0],parts[1:],args

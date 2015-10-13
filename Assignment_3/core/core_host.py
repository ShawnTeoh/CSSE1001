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
import shutil

class Core_host:
    """Core methods for PC."""
    def __init__(self):
        """Core_host.__init__()

        Initialises Core_host.
        """
        self._cur_path=os.path.expanduser('~')
        os.chdir(self._cur_path)

    def pwd(self):
        """Core_host.pwd() -> (string)

        Returns current path.
        """
        return self._cur_path

    def ls(self,folder=None):
        """Core_host.ls(string) -> (dict(dict))

        Lists files in current directory or specific directory (if given).
        Also checks file size and if file is directory.
        """
        out={}
        if folder == None:
            folder=self._cur_path
        names=os.listdir(folder)

        for name in names:
            is_dir=os.path.isdir(os.path.join(folder,name))
            size=self._convert(os.path.getsize(os.path.join(folder,name)))
            out[name]={'is_dir':is_dir,'size':size}
        return out

    def cd(self,path=None):
        """Core_host.cd(string)

        Switches to specified directory (home directory if not specified).
        """
        if path == None:
            path='~'

        self._cur_path=os.path.expanduser(path)

    def cp(self,_from,_to):
        """Core_host.cp(string,string)

        Copies file/folder into given path. File/folder name must be specified.
        """
        if os.path.isdir(_from):
            shutil.copytree(_from,_to)
        else:
            shutil.copy2(_from,_to)
    
    def mv(self,_from,_to):
        """Core_host.mv(string,string)

        Moves file/folder into given path. File/folder name must be specified.
        Can be used for renaming.
        """
        shutil.move(_from,_to)

    def rm(self,path):
        """Core_host.rm(string)

        Deletes specified file/folder.
        """
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

    def mkdir(self,path):
        """Core_host.mkdir(string)

        Creates a new folder.
        """
        os.makedirs(path)

    def _convert(self,num):
        """Core_host._convert(int) -> (string)

        Converts given number into bytes, KB, MB, GB or TB.
        """
        for x in ['bytes','K','M','G','T']:
            if num < 1024.0:
                return '%.2f %s'%(num, x)
            num/=1024.0

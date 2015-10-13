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
# Android uses Unix like path, use posixpath to make it OS dependent
import posixpath
import subprocess

class ADBError(Exception):
    """Exception for ADB action errors."""
    pass

class Core_target:
    """Core methods for ADB."""
    def __init__(self):
        """Core_target.__init__()

        Initialises Core_target.
        """
        self.connect()
        
    def _execute(self,cmd):
        """Core_target._execute(list or string) -> (list)

        Executes shell commands and returns the output as a list.
        """
        process=subprocess.Popen(cmd,shell=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT).stdout
        lines=[]     
        while True:
            line = process.readline()
            if not line:
                break
            lines.append(line.rstrip())
        return lines

    def check_connect(self):
        """Core_target.check_connect()

        Checks if device is connected.
        """
        self._execute('adb start-server')
        check=self._execute('adb devices')
        
        if len(check) < 3:
            self.connected=False
        else:
            self.connected=True

    def connect(self):
        """Core_target.connect()

        Connects to device.
        """
        self.check_connect()
        self.env()
    
    def pwd(self):
        """Core_target.pwd() -> (string)

        Returns current path.
        """
        return self._cur_path

    def ls(self,folder=None):
        """Core_target.ls(string) -> (dict(dict))

        Lists files in current directory or specific directory (if given).
        """
        out={}
        if folder == None:
            folder=self._cur_path
        data=self._execute('adb shell ls -al '+folder)
        self._check_error(data)
        for i in data:
            j=i.split()
            if j[0].startswith('d'):
                is_dir=True
                name=j[-1]
            elif j[0].startswith('l'):
                name=j[-3]
                try:
                    is_dir=self._check_is_dir(j[-1])
                except ADBError:
                    continue
            else:
                is_dir=False
                name=j[-1]
            
            if is_dir:
                size='0.0 bytes'
            else:
                size=self._convert(int(j[3])) 
            
            out[name]={'is_dir':is_dir,'size':size}
        return out    

    def cd(self,path):
        """Core_target.cd(string)

        Switches to specified directory (home directory if not specified).
        """
        if path == None or path == '~/':
            self._cur_path=self.storage['EXTERNAL_STORAGE']
        elif path.startswith('/'):
            self._cur_path=path
        else:
            self._cur_path=posixpath.abspath(posixpath.join(self._cur_path,
                                                            path))

    def cp(self,_from,_to):
        """Core_target.cp(string,string)

        Copies file/folder into given path. File/folder name must be specified.
        """
        if _from.startswith('/') and _to.startswith('/'):
            out=self._execute('adb shell cp '+_from+' '+_to)
        elif _from.startswith('/'):
            out=self._execute('adb shell cp '+_from+''+self._cur_path+'/'+_to)
        elif _to.startswith('/'):
            out=self._execute('adb','shell','cp',self._cur_path+'/'+_from,_to)
        else:
            out=self._execute('adb shell cp '+self._cur_path+'/'+_from+' '+
                               self._cur_path+'/'+_to)
        self._check_error(out)
    
    def mv(self,_from,_to):
        """Core_target.mv(string,string)

        Moves file/folder into given path. File/folder name must be specified.
        Can be used for renaming.
        """
        if _from.startswith('/') and _to.startswith('/'):
            out=self._execute('adb shell mv '+_from+' '+_to)
        elif _from.startswith('/'):
            out=self._execute('adb shell mv '+_from+' '+self._cur_path+'/'+_to)
        elif _to.startswith('/'):
            out=self._execute('adb shell mv ',self._cur_path+'/'+_from+' '+_to)
        else:
            out=self._execute('adb shell mv '+self._cur_path+'/'+_from+' '+
                               self._cur_path+'/'+_to)
        self._check_error(out)

    def rm(self,path):
        """Core_target.rm(string)

        Deletes specified file/folder.
        """
        if not path.startswith('/'):
            path=self._cur_path+'/'+path    
        out=self._execute('adb shell rm -r '+path)
        self._check_error(out)

    def upload(self,_from,_to):
        """Core_target.upload(string,string)

        Uploads file to given full path. File name must be specified.
        """
        out=self._execute('adb push '+_from+' '+_to)
        self._check_error(out)

    def download(self,_from,_to):
        """Core_target.download(string,string)

        Downloads file to given full path. File name must be specified.
        """
        out=self._execute('adb pull '+_from+' '+_to)
        self._check_error(out)

    def mkdir(self,path):
        """Core_target.mkdir(string)

        Creates a new folder.
        """
        if not path.startswith('/'):
            path=self._cur_path+'/'+path
        out=self._execute('adb shell mkdir '+path)
        self._check_error(out)

    def df(self):
        """Core_target.df() -> {dict{dict}}

        Displays disk usage.
        """
        data=self._execute('adb shell df')
        self._check_error(data)
        out={}
        for name in data:
            if self.storage['EXTERNAL_STORAGE'] in name or \
               self.storage['SECONDARY_STORAGE'] in name:
                i=name.split()
                out[i[0]]={'Size':i[1],'Used':i[2],'Free':i[3]}
        return out

    def env(self):
        """Core_target.env()

        Get path of device storage.
        """
        if self.connected:
            data=self._execute('adb shell env')
            self.storage={}
            for name in data:
                if 'EXTERNAL_STORAGE' in name or 'SECONDARY_STORAGE' in name:
                    i=tuple(name.split('='))
                    self.storage[i[0]]=i[1]
            self._cur_path=self.storage['EXTERNAL_STORAGE']

    def _convert(self,num):
        """Core_target._convert(int) -> (string)

        Converts given number into bytes, KB, MB, GB or TB.
        """
        for x in ['bytes','K','M','G','T']:
            if num < 1024.0:
                return '%.2f %s'%(num,x)
            num/=1024.0

    def _check_error(self,out):
        """Core_target(list)

        Raises an exception if there is an error when executing shell commands.
        """
        if out:
            if 'error' in out[0] or 'failed' in out[0] or 'cannot' in out[0] \
               or 'No such' in out[0]:
                raise ADBError(out[0])

    def _check_is_dir(self,path):
        """Core_target(string) -> (bool)

        Checks if the given path is a folder or not (targeted at symlinks).
        """
        return self.ls(os.path.dirname(path))[os.path.basename(path)]['is_dir']

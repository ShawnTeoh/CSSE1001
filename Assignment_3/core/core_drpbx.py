########################################################################
#                                                                      #
#  This code is part of Android Explorer.                              #
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
# Dropbox uses Unix like path, use posixpath to make it OS dependent
import posixpath
import ConfigParser
try:
    import dropbox
except ImportError:
    print 'The dropbox modules is not installed'
    exit(1)

APP_KEY='s8xmcugdebrhtg2'
APP_SECRET='5pnm0cqb2lqbkxe'
CFG_FILE='configs/drpbx.cfg'
CFG_PATH=os.path.abspath(os.path.join(os.path.dirname(__file__),'..',CFG_FILE))

class Core_drpbx:
    """Core methods for Dropbox sync."""
    def __init__(self):
        """Core_drpbx.__init__()

        Initialises core_drpbx.
        """
        self.client=None
        self._cur_path='/'
        self._config=ConfigParser.SafeConfigParser()
        self._flow=dropbox.client.DropboxOAuth2FlowNoRedirect(APP_KEY,
                                                              APP_SECRET)
        try:
            self._config.read(CFG_PATH)
            token=self._config.get('Dropbox','token')
            self.client=dropbox.client.DropboxClient(token)
        except ConfigParser.NoSectionError:
            pass # Don't care if not logged in yet

    def get_auth_url(self):
        """Core_drpbx.get_auth_url() -> (string)

        Gets authorisation URL.
        """
        return self._flow.start()

    def login(self,code):
        """Core_drpbx.login(string)

        Login using authorisation code.
        """
        token,user_id=self._flow.finish(code)
        
        if self._config.has_section('Dropbox'):
            self._config.remove_section('Dropbox')
        self._config.add_section('Dropbox')
        self._config.set('Dropbox','token',token)

        with open(CFG_PATH,'w') as f:
            self._config.write(f)
        
        self.client=dropbox.client.DropboxClient(token)

    def logout(self):
        """Core_drpbx.logout()

        Logout from account.
        """
        if self.client != None:
            self.client=None
            self._current_path='/'
            os.unlink(CFG_PATH)
    
    def pwd(self):
        """Core_drpbx.pwd() -> (string)

        Returns current path.
        """
        return self._cur_path

    def ls(self,folder=None):
        """Core_drpbx.ls(string) -> (dict(dict))

        Lists files in current directory or specific directory (if given).
        Also checks file size and if file is directory.
        """
        out={}
        if folder != None:
            data=self.client.metadata(folder)
        else:
            data=self.client.metadata(self._cur_path)

        if 'contents' in data:
            for f in data['contents']:
                out[os.path.basename(f['path'])]={'is_dir':f['is_dir'],
                                                       'size':str(f['size'])}
        return out       

    def cd(self,path):
        """Core_drpbx.cd(string)

        Switches to specified directory (root directory if not specified).
        """
        if path == None or path == '~/':
            self._cur_path='/'
        elif path.startswith('/'):
            self._cur_path=path
        else:
            self._cur_path=posixpath.abspath(posixpath.join(self._cur_path,
                                                            path))

    def cp(self,_from,_to):
        """Core_drpbx.cp(string,string)

        Copies file/folder into given path. File/folder name must be specified.
        """
        if _from.startswith('/') and _to.startswith('/'):
            self.client.file_copy(_from,_to)
        elif _from.startswith('/'):
            self.client.file_copy(_from,self._cur_path+'/'+_to)
        elif _to.startswith('/'):
            self.client.file_copy(self._cur_path+'/'+_from,_to)
        else:
            self.client.file_copy(self._cur_path+'/'+_from,
                                  self._cur_path+'/'+_to)
    
    def mv(self,_from,_to):
        """Core_drpbx.mv(string,string)

        Moves file/folder into given path. File/folder name must be specified.
        Can be used for renaming.
        """
        if _from.startswith('/') and _to.startswith('/'):
            self.client.file_move(_from,_to)
        elif _from.startswith('/'):
            self.client.file_move(_from,self._cur_path+'/'+_to)
        elif _to.startswith('/'):
            self.client.file_move(self._cur_path+'/'+_from,_to)
        else:
            self.client.file_move(self._cur_path+'/'+_from,
                                  self._cur_path+'/'+_to)

    def rm(self,path):
        """Core_drpbx.rm(string)

        Deletes specified file/folder.
        """
        if not path.startswith('/'):    
            self.client.file_delete(path)
        else:
            self.client.file_delete(self._cur_path+'/'+path)

    def upload(self,_from,_to):
        """Core_drpbx.upload(string,string)

        Uploads file to given full path. File name must be specified.
        """
        with open(os.path.expanduser(_from),'rb') as f:
            self.client.put_file(_to,f)

    def download(self,_from,_to):
        """Core_drpbx.download(string,string)

        Downloads file to given full path. File name must be specified.
        """
        with open(os.path.expanduser(_to),'wb') as f:
            f.write(self.client.get_file(self._cur_path+'/'+_from).read())

    def mkdir(self,path):
        """Core_drpbx.mkdir(string)

        Creates a new folder.
        """
        if not path.startswith('/'):
            self.client.file_create_folder(path)
        else:
            self.client.file_create_folder(self._cur_path+'/'+path)

    def acc_info(self):
        """Core_drpbx.acc_info() -> [string,string]

        Displays quota info.
        """
        data=self.client.account_info()['quota_info']
        out=[self._convert(data['quota'])]
        out.append(self._convert(data['normal']+data['shared']))
        return out
    
    def _convert(self,num):
        """Core_drpbx._convert(int) -> (string)

        Converts given number into bytes, KB, MB, GB or TB.
        """
        for x in ['bytes','K','M','G','T']:
            if num < 1024.0:
                return '%.2f %s'%(num, x)
            num/=1024.0

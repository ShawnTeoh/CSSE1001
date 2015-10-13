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
import subprocess
from Tkinter import *
import tkMessageBox
from PIL import Image, ImageTk
if os.name == 'nt':
    import SendKeys

TREE_COL=('name','size','type')
HELP_FILE='README.txt'

class UIFunc:
    """Main functions of main UI components."""
    def __init__(self,master,remote=None,tree=None):
        """UIFunc.__init__(instance,instance,instance)

        Initialises UIFunc.
        """
        self._master=master
        self._remote=remote
        self._tree=tree
        self._path=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))

    def _execute(self,cmd):
        """UIFunc._execute(string/list)

        Carries out a command without showing a shell.
        """
        subprocess.Popen(cmd,shell=True)

    def new_fol(self):
        """UIFunc.new_fol()

        Creates a new folder (called from context menu).
        """
        def ok():
            try:
                self._remote.mkdir(entry.get())
                self.refresh()
                win.destroy()
            except Exception as e:
                tkMessageBox.showerror(title='ERROR',message=e)
        
        entry,win=self.create_new_dialog('New Folder',
                                         'Enter folder name',20,ok)

    def rename(self):
        """UIFunc.rename()

        Renames files/folder (called from context menu).
        """
        def ok():
            try:
                self._remote.mv(path,entry.get())
                self.refresh()
                win.destroy()
            except Exception as e:
                tkMessageBox.showerror(title='ERROR',message=e)
        
        if self._tree.selection():
            item=self._tree.selection()[0]
            path=self._tree.set(item,TREE_COL[0])
            entry,win=self.create_new_dialog('Rename',
                                             'Enter new name',20,ok)

    def delete(self):
        """UIFunc.delete()

        Deletes files/folder (called from context menu).
        """
        path=self._tree.selection()
        reply = tkMessageBox.askquestion(type=tkMessageBox.YESNO,
                                         title="Deleting Files",
                                         message="Are you sure?")
        if reply == tkMessageBox.YES:
            try:
                for i in path:
                    self._remote.rm(self._tree.set(i,TREE_COL[0]))
                self.refresh()
            except Exception as e:
                tkMessageBox.showerror(title='ERROR',message=e)
    
    def refresh(self):
        """UIFunc.refresh()

        Refreshes tree view (called from context menu).
        """
        # Dirty hack: simulates F5 keypress
        if os.name == 'nt':
            SendKeys.SendKeys("""{F5}""")
        else:
            self._execute('xdotool key F5')

    def close(self):
        """UIFunc.close()

        Closes window (called from menu bar).
        """
        self._master.destroy()

    def single(self):
        """UIFunc.single()

        Opens a single panel file manager.
        """
        cmd='python '+os.path.join(self._path,'file_man.py')
        self._execute(cmd)

    def dual(self):
        """UIFunc.dual()

        Opens a dual panel file manager.
        """
        cmd='python '+os.path.join(self._path,'file_man.py')
        self._execute(cmd)

    def drpbx(self):
        """UIFunc.drpbx()

        Opens Dropbox sync.
        """
        cmd='python '+os.path.join(self._path,'drpbx_ui.py')
        self._execute(cmd)

    def cli_target(self):
        """UIFunc.cli_target()

        Launches ADB CLI in another shell.
        """
        if os.name == 'nt':
            cmd=['start','python',os.path.join(self._path,'cli_target.py')]
            self._execute(cmd)
        else:
            cmd=['xterm','-e','python '+os.path.join(self._path,'cli_target.py')]
            subprocess.call(cmd)

    def cli_drpbx(self):
        """UIFunc.cli_drpbx()

        Launches Dropbox CLI in another shell.
        """
        if os.name == 'nt':
            cmd=['start','python',os.path.join(self._path,'cli_drpbx.py')]
            self._execute(cmd)
        else:
            cmd=['xterm','-e','python '+os.path.join(self._path,'cli_drpbx.py')]
            subprocess.call(cmd)

    def settings(self):
        """UIFunc.settings()

        Opens Settings window (called from menu bar).
        """
        cmd='python '+os.path.join(self._path,'settings.py')
        self._execute(cmd)
        
    def helpfile(self):
        """UIFunc.help()

        Opens help file (called from menu bar).
        """
        os.startfile(os.path.join(self._path,HELP_FILE))

    def about(self):
        """UIFunc.about()

        Display program information (called from menu bar).
        """
        logo=ImageTk.PhotoImage(Image.open(os.path.join(self._path,'res',
                                                        'logo.png')))
        program_name='Android Explorer'
        copyright_info="""Written by Thuan Song Teoh.
Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR
ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""
        
        win=Toplevel(self._master)
        win.wm_title('About')
        win.resizable(width=FALSE,height=FALSE)
        Label(win,text='Copyright 2013').pack(side=TOP)
        lbl=Label(win,image=logo)
        lbl.image=logo
        lbl.pack(side=TOP)
        Label(win,text=program_name,font='bold').pack(side=TOP)
        Label(win,text=copyright_info).pack(side=TOP)

    def create_new_dialog(self,title,txt,size,cmd):
        """UIFunc.create_new_dialog(string,string,int,function)
        -> (object,object)

        Creates a small dialog box with an entry widget.
        """
        # Create a new window
        win=Toplevel(self._master)
        win.wm_title(title)
        win.minsize(200,100)
        win.resizable(width=FALSE,height=FALSE)
        # Instructions
        Label(win,text=txt).pack(side=TOP)
        # Entry box
        entry=Entry(win,width=size)
        entry.pack(side=TOP)
        # Separator
        separator=Frame(win,height=2,bd=1,relief=SUNKEN)
        separator.pack(side=TOP,fill=X,padx=5,pady=5)
        # Button
        btn=Button(win,text='OK',command=cmd)
        btn.pack(side=TOP,pady=5)

        return (entry,win)

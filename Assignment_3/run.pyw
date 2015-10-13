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
from Tkinter import *
from PIL import Image,ImageTk
import ConfigParser
from ui.main import *
from ui.func import *

CFG_FILE='configs/settings.cfg'
CFG_PATH=os.path.join(os.path.dirname(__file__),CFG_FILE)

class StartPage(object):
    """The main menu."""
    def __init__(self,master):
        """StartPage.__init__()

        Initialises StartPage.
        """
        # Top level configurations
        self._master=master
        master.resizable(width=FALSE,height=FALSE)
        master.title('Android Explorer')

        # Core functions
        self._func=UIFunc(self._master)
        self._path=os.path.dirname(__file__)
        self._config=ConfigParser.SafeConfigParser()
        self._opt_file_man=None
        self._opt_cli=None

        # Main UI
        self._main=MainUI(self._master,self._func)
        self._main.create_menubar()

        # Get configuration values
        try:
            self._config.read(CFG_PATH)
            self._opt_file_man=self._config.get('Settings','file_man')
            self._opt_cli=self._config.get('Settings','cli')
        # Ignore if no config file found
        except ConfigParser.NoSectionError:
            pass
        except ConfigParser.NoOptionError:
            pass

        # Buttons and banner
        self._create_widgets()

    def _create_widgets(self):
        """StartPage._create_widgets()

        Creates the buttons and banner.
        """
        # Icons
        ico1=ImageTk.PhotoImage(Image.open(os.path.join\
                                           (self._path,'res','folder.png')))
        ico2=ImageTk.PhotoImage(Image.open(os.path.join\
                                           (self._path,'res','drpbx.png')))
        ico3=ImageTk.PhotoImage(Image.open(os.path.join\
                                           (self._path,'res','cli.png')))
        ico4=ImageTk.PhotoImage(Image.open(os.path.join\
                                           (self._path,'res','settings.png')))
        
        frame=Frame(self._master)
        frame.pack(side=TOP,expand=True,fill=X)
        # File manager
        btn1=Button(frame,compound=TOP,text='File Manager',
                    image=ico1,command=self._file_man)
        btn1.image=ico1
        btn1.pack(side=LEFT,expand=True)
        # Dropbox
        btn2=Button(frame,compound=TOP,text='Dropbox Sync',
                    image=ico2,command=self._func.drpbx)
        btn2.image=ico2
        btn2.pack(side=LEFT,expand=True)
        # CLI
        btn3=Button(frame,compound=TOP,text='CLI',
                    image=ico3,command=self._cli)
        btn3.image=ico3
        btn3.pack(side=LEFT,expand=True)
        # Settings
        btn4=Button(frame,compound=TOP,text='Settings',
                    image=ico4,command=self._func.settings)
        btn4.iamge=ico4
        btn4.pack(side=LEFT,expand=True)
        # Banner
        logo=ImageTk.PhotoImage(Image.open(os.path.join\
                                           (self._path,'res','logo.png')))
        banner=Label(self._master,image=logo)
        banner.image=logo
        banner.pack(side=TOP,expand=True)

    def _file_man(self):
        """StartPage._file_man()

        Callback function for the File Manager button.
        """
        def ok():
            """Action when OK button is clicked"""
            self._func.single() if self._var.get() == 1 else self._func.dual()
            win.destroy()

        if self._opt_file_man == None or self._opt_file_man == '0':
            # Launch dialog if no config found or specifed to do so
            win=self._new_dialog('Single Panel','Dual Panel',ok)
        elif self._opt_file_man == '1':
            # Lauch single panel
            self._func.single()
        else:
            # Lauch dual panel
            self._func.dual()
    
    def _cli(self):
        """StartPage._cli()

        Callback function for the CLI button.
        """
        def ok():
            """Action when OK button is clicked"""
            self._func.cli_target() if self._var.get() == 1 else \
                                    self._func.cli_drpbx()
            win.destroy()
        
        if self._opt_cli == None or self._opt_cli == '0':
            # Launch dialog if no config found or specifed to do so
            win=self._new_dialog('ADB','Dropbox',ok)
        elif self._opt_cli == '1':
            # Launch ADB CLI
            self._func.cli_target()
        else:
            # Launch Dropbox CLI
            self._func.cli_drpbx()

    def _new_dialog(self,txt1,txt2,cmd):
        """StartPage._new_dialog(string,string,function) -> object

        Creates a new dialog with radio buttons.
        """
        # Initialise value container
        self._var=IntVar()

        # Create new window
        win=Toplevel(self._master)
        win.wm_title('Options')
        win.minsize(200,50)
        win.resizable(width=FALSE,height=FALSE)
        # Radio buttons
        rad1=Radiobutton(win,text=txt1,variable=self._var,
                         value=1)
        rad1.pack(side=TOP)
        rad1.select()
        rad2=Radiobutton(win,text=txt2,variable=self._var,
                    value=2)
        rad2.pack(side=TOP)
        # Separator
        separator=Frame(win,height=2,bd=1,relief=SUNKEN)
        separator.pack(side=TOP,fill=X,padx=5,pady=5)
        # OK button
        btn=Button(win,text='OK',command=cmd)
        btn.pack(side=TOP,pady=5)

        return win

def main():
    root = Tk()
    app=StartPage(root)
    root.mainloop()

if __name__=='__main__':
    main()

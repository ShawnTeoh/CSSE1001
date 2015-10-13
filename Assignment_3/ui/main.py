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

class MainUI:
    """Host main GUI items such as menu bar and context menu."""
    def __init__(self,master,func=None):
        """MainUI.__init__(instance,instance)

        Initialises MainUI.
        """
        self._master=master
        self._func=func
        self._path=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
    
    def create_menubar(self):
        """MainUI.create_menubar()

        Creates the menu bar.
        """
        menubar=Menu(self._master)
        self._master.config(menu=menubar)
        # Main menu
        mainmenu=Menu(menubar,tearoff=0)
        menubar.add_cascade(label='Main',menu=mainmenu)
        mainmenu.add_command(label='Exit',command=self._func.close)
        # File manager
        manmenu=Menu(menubar,tearoff=0)
        menubar.add_cascade(label='File Manager',menu=manmenu)
        manmenu.add_command(label='Single Panel',command=self._func.single)
        manmenu.add_command(label='Dual Panel',command=self._func.dual)
        # Dropbox
        menubar.add_command(label='Dropbox Sync',command=self._func.drpbx)
        # CLI
        climenu=Menu(menubar,tearoff=0)
        menubar.add_cascade(label='CLI',menu=climenu)
        climenu.add_command(label='ADB',command=self._func.cli_target)
        climenu.add_command(label='Dropbox',command=self._func.cli_drpbx)
        # Settings
        menubar.add_command(label='Settings',command=self._func.settings)
        # Help
        helpmenu=Menu(menubar,tearoff=0)
        menubar.add_cascade(label='Help',menu=helpmenu)
        helpmenu.add_command(label='Help',command=self._func.helpfile)
        helpmenu.add_command(label='About',command=self._func.about)

    def create_context_menu(self):
        """MainUI.create_context_menu()

        Creates the context menu.
        """
        self._context=Menu(self._master,tearoff=0)
        self._context.add_command(label='Refresh',command=self._func.refresh)
        self._context.add_separator()
        self._context.add_command(label='New folder',command=self._func.new_fol)
        self._context.add_command(label='Rename',command=self._func.rename)
        self._context.add_command(label='Delete',command=self._func.delete)
        self._master.bind('<Button-3>',self._pop_context)

    def _pop_context(self,event):
        """MainUI._pop_context(event)

        Callback function to reposition the context menu.
        """
        self._context.post(event.x_root,event.y_root)

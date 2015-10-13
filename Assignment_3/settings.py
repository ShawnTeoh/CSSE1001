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
import ConfigParser
from ui.main import *
from ui.func import *

CFG_FILE='configs/settings.cfg'
CFG_PATH=os.path.join(os.path.dirname(__file__),CFG_FILE)

class Settings(object):
    """Settings UI."""
    def __init__(self,master):
        """Settngs.__init__()

        Initialises Settings.
        """
        # Top level configurations
        self._master=master
        master.minsize(300,280)
        master.resizable(width=FALSE,height=FALSE)
        master.title('Settings')

        # Core functions
        self._func=UIFunc(self._master)
        self._config=ConfigParser.SafeConfigParser()
        self._opt_file_man=None
        self._opt_cli=None
        self._opt_drpbx=None

        # Main UI
        self._main=MainUI(self._master,self._func)
        self._main.create_menubar()

        # Get configuration values
        try:
            self._config.read(CFG_PATH)
            self._opt_file_man=self._config.get('Settings','file_man')
            self._opt_cli=self._config.get('Settings','cli')
            self._opt_drpbx=self._config.get('Settings','drpbx')
        # Ignore if no config file found
        except ConfigParser.NoSectionError:
            pass
        except ConfigParser.NoOptionError:
            pass

        # Checkboxes
        self._create_widgets()

    def _create_widgets(self):
        """Settings._create_widgets()

        Creates the checkboxes and buttons.
        """
        # Initialise value containers
        self._var1=IntVar()
        self._var2=IntVar()
        self._var3=IntVar()

        frame1=Frame(self._master)
        frame1.pack(anchor=W,pady=5)
        # First option
        Label(frame1,text='Default file manager:',font='bold').grid(row=0,
                                                                    sticky=W)
        subframe1=Frame(frame1)
        subframe1.grid(row=1,sticky=W)
        ckbtn1_1=Checkbutton(subframe1,text="Single Panel",variable=self._var1,
                             onvalue=1)
        ckbtn1_1.grid(row=0,column=0)
        ckbtn1_2=Checkbutton(subframe1,text="Dual Panel",variable=self._var1,
                             onvalue=2)
        ckbtn1_2.grid(row=0,column=1)
        ckbtn1_3=Checkbutton(subframe1,text="None",variable=self._var1,
                             onvalue=0)
        ckbtn1_3.grid(row=0,column=2)
        # Second option
        frame2=Frame(self._master)
        frame2.pack(anchor=W,pady=5)
        subframe2=Frame(frame2)
        subframe2.grid(row=1,sticky=W)
        Label(frame2,text='Default CLI:',font='bold').grid(row=0,sticky=W)
        ckbtn2_1=Checkbutton(subframe2,text="ABD",variable=self._var2,
                             onvalue=1)
        ckbtn2_1.grid(row=0,column=0)
        ckbtn2_2=Checkbutton(subframe2,text="Dropbox",variable=self._var2,
                             onvalue=2)
        ckbtn2_2.grid(row=0,column=1)
        ckbtn2_3=Checkbutton(subframe2,text="None",variable=self._var2,
                             onvalue=0)
        ckbtn2_3.grid(row=0,column=2)
        # Third option
        frame3=Frame(self._master)
        frame3.pack(anchor=W,pady=5)
        subframe3=Frame(frame3)
        subframe3.grid(row=1,sticky=W)
        Label(frame3,text='Auto Dropbox logout:',font='bold').grid(row=0,
                                                                   sticky=W)
        ckbtn3_1=Checkbutton(subframe3,text="Yes",variable=self._var3,
                             onvalue=1)
        ckbtn3_1.grid(row=0,column=0)
        ckbtn3_2=Checkbutton(subframe3,text="No",variable=self._var3,
                             onvalue=0)
        ckbtn3_2.grid(row=0,column=1)
        # Separator
        separator=Frame(self._master,height=2,bd=1,relief=SUNKEN)
        separator.pack(fill=X,padx=5,pady=3)
        # Info
        Label(self._master,text='Please restart program for changes to apply.')\
                                        .pack()
        # Buttons
        Button(self._master,text='OK',command=self._ok).pack(side=LEFT,
                                                             expand=True)
        Button(self._master,text='Cancel',
               command=self._cancel).pack(side=LEFT,expand=True)

        # If configutation file loaded, initialise checkboxes
        if self._opt_file_man == None or self._opt_file_man == '0':
            ckbtn1_3.select()
        elif self._opt_file_man == '1':
            ckbtn1_1.select()
        else:
            ckbtn1_2.select()

        if self._opt_cli == None or self._opt_cli == '0':
            ckbtn2_3.select()
        elif self._opt_cli == '1':
            ckbtn2_1.select()
        else:
            ckbtn2_2.select()

        if self._opt_drpbx == '1':
            ckbtn3_1.select()
    
    def _ok(self):
        """Settings._ok()

        Saves changes to a config file.
        """
        # Clears old settings
        if self._config.has_section('Settings'):
            self._config.remove_section('Settings')
        # Write new settings
        self._config.add_section('Settings')
        self._config.set('Settings','file_man',str(self._var1.get()))
        self._config.set('Settings','cli',str(self._var2.get()))
        self._config.set('Settings','drpbx',str(self._var3.get()))
        with open(CFG_PATH,'w') as f:
            self._config.write(f)
        # Close window afte operation
        self._master.destroy()

    def _cancel(self):
        """Settings._cancel()
        
        Cancels operation and closes window."""
        self._master.destroy()

def main():
    root = Tk()
    app=Settings(root)
    root.mainloop()

if __name__=='__main__':
    main()

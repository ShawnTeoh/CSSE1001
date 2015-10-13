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

from Tkinter import *
import ttk
import tkMessageBox
import tkFileDialog
from ui.main import *
from ui.func import *
from core.core_target import *

TREE_COL=('name','size','type')

class FileMan(object):
    """The file manager interface."""
    def __init__(self,master):
        """FileMan.__init__()

        Initialises FileMan.
        """
        # Top level configurations
        self._master=master
        master.resizable(width=False,height=False)
        master.title('File Manager')
        master.bind('<F5>',self._refresh)
        master.bind('<F2>',self._rename)
        master.bind('<Delete>',self._remove)

        # Core functions
        self._remote=Core_target()
        self._path=os.path.abspath(os.path.join(os.path.dirname(__file__)))

        # Buttons
        self._create_top_widgets()
        # Tree view
        self._create_tree()
        self._func=UIFunc(self._master,self._remote,self._tree)
        # More buttons
        self._create_bottom_widgets()
        # Main UI
        self._main=MainUI(self._master,self._func)
        self._main.create_menubar()
        self._main.create_context_menu()

        # Prompt to connect device if not connected
        if self._remote.connected == False:
            self._prompt_connect()
        else:
            self._build_tree()

    def _create_top_widgets(self):
        """FileMan._create_top_widgets()

        Creates the buttons on top.
        """
        # Open icons
        pic1=ImageTk.PhotoImage(Image.open(os.path.join(self._path,
                                                       'res','up.png')))
        pic2=ImageTk.PhotoImage(Image.open(os.path.join(self._path,
                                                       'res','new.png')))
        pic3=ImageTk.PhotoImage(Image.open(os.path.join(self._path,
                                                       'res','rm.png')))
        
        frame=Frame(self._master)
        frame.pack(side=TOP,anchor=E,padx=10)
        # Go up one directory
        btn1=Button(frame,image=pic1,command=self._cd_up)
        btn1.image=pic1
        btn1.pack(side=LEFT)
        # New folder
        btn2=Button(frame,compound=LEFT,text='New Folder',image=pic2,
                    command=self._mkdir)
        btn2.image=pic2
        btn2.pack(side=LEFT,padx=5)
        # Delete
        btn3=Button(frame,compound=LEFT,text='Delete',image=pic3,
                    command=self._rm)
        btn3.image=pic3
        btn3.pack(side=LEFT,padx=5)
        
    def _create_bottom_widgets(self):
        """FileMan._create_bottom_widgets()

        Creates the buttons and progrss bar.
        """
        # Icons
        pic1=ImageTk.PhotoImage(Image.open(os.path.join(self._path,
                                                       'res','upload.png')))
        pic2=ImageTk.PhotoImage(Image.open(os.path.join(self._path,
                                                       'res','download.png')))
        
        frame=Frame(self._master)
        frame.pack(side=TOP,pady=10,padx=10,fill=X)
        # Progress bar
        self._pbar=ttk.Progressbar(frame,orient="horizontal",
                                   length=300, mode="indeterminate")
        self._pbar.pack(side=TOP,expand=True,pady=3)
        # Buttons
        btn1=Button(frame,compound=LEFT,text='Upload',image=pic1,
                    command=self._upload)
        btn1.image=pic1
        btn1.pack(side=LEFT,expand=True,pady=5,ipadx=9)
        btn2=Button(frame,compound=LEFT,text='Download',image=pic2,
                    command=self._download)
        btn2.image=pic2
        btn2.pack(side=LEFT,expand=True,pady=5,ipadx=1)

    def _create_tree(self):
        """FileMan._create_tree()

        Creates a tree view of files.
        """
        frame=Frame(self._master)
        frame.pack(side=TOP,padx=5,pady=5,expand=True)
        # Tree view
        self._tree=ttk.Treeview(frame)
        vsb=ttk.Scrollbar(frame,orient="vertical",command=self._tree.yview)
        self._tree.configure(yscrollcommand=vsb.set)
        self._tree.grid(column=0,row=0,sticky='nsew')
        vsb.grid(column=1,row=0,sticky='ns')
        self._tree.bind('<Double-1>',self._cd)

        # Configure tree view
        self._tree['columns']=TREE_COL
        self._tree.column('#0',width=40)
        self._tree.column(TREE_COL[0],width=250)
        self._tree.column(TREE_COL[1],width=100)
        self._tree.column(TREE_COL[2],width=100)
        # Sorting actions
        self._tree.heading(TREE_COL[0],text='Name',
                           command=lambda c=TREE_COL[0]: self._sortby\
                           (self._tree,c,0))
        self._tree.heading(TREE_COL[1],text='Size',
                           command=lambda c=TREE_COL[1]: self._sortby\
                           (self._tree,c,0))
        self._tree.heading(TREE_COL[2],text='Type',
                           command=lambda c=TREE_COL[2]: self._sortby\
                           (self._tree,c,0))
        
    def _build_tree(self):
        """FileMan._build_tree()

        Adds items to the tree view.
        """
        # Progress bar not working due to Tkinter being single threaded
        self._pbar.start()
        # Clear tree view
        items=self._tree.get_children()
        for item in items: self._tree.delete(item)
        
        # Icons
        self._ico_fol=ImageTk.PhotoImage(Image.open(os.path.join(self._path,
                                                       'res','ico_folder.png')))
        self._ico_docs=ImageTk.PhotoImage(Image.open(os.path.join(self._path,
                                                       'res','ico_docs.png')))
        self._ico_images=ImageTk.PhotoImage(Image.open(os.path.join(self._path,
                                                       'res','ico_images.png')))
        self._ico_media=ImageTk.PhotoImage(Image.open(os.path.join(self._path,
                                                       'res','ico_media.png')))
        self._ico_others=ImageTk.PhotoImage(Image.open(os.path.join(self._path,
                                                       'res','ico_others.png')))
        # Get file names
        self._files=self._remote.ls()
        # File types
        docs=['pdf','doc','docx','ppt','pptx','xls','xlsx']
        images=['png','jpg','jpeg','gif']
        media=['mp3','mp4','wav','mpeg','avi','mkv']
        sort_files=[_ for _ in self._files]
        sort_files.sort()

        # Inserts data to tree view
        for i in sort_files:
            # File type
            if self._files[i]['is_dir']:
                _type='Folder'
                _size=''
            else:
                _type=i.split('.')[-1]
                _size=self._files[i]['size']
            # Icon type
            if _type in docs:
                pic=self._ico_docs
            elif _type in images:
                pic=self._ico_images
            elif _type in media:
                pic=self._ico_media
            elif _type == 'Folder':
                pic=self._ico_fol
            else:
                pic=self._ico_others
            self._tree.insert('','end',image=pic,values=(i,_size,_type))
        self._pbar.stop()

    def _prompt_connect(self):
        """"FileMan._prompt_connect()

        Prompts user to connect to device.
        """
        def ok():
            """Callback function when OK is clicked."""
            try:
                self._remote.connect()
                if self._remote.connected == False:
                    raise ADBError('Device not found!')
                else:
                    win.destroy()
                    self._build_tree()
            except Exception as e:
                tkMessageBox.showerror(title='ERROR',message=e)
                
        win=Toplevel(self._master)
        win.wm_title('Connect')
        win.minsize(200,100)
        win.resizable(width=FALSE,height=FALSE)
        # Instructions
        ins1='1. Connect your device '
        ins2='2. Click \"OK\" to connect.'
        Label(win,text=ins1).pack(side=TOP)
        Label(win,text=ins2).pack(side=TOP)
        # Separator
        separator=Frame(win,height=2,bd=1,relief=SUNKEN)
        separator.pack(side=TOP,fill=X,padx=5,pady=5)
        # Button
        btn=Button(win,text='OK',command=ok)
        btn.pack(side=TOP,pady=5)

    def _cd(self,event):
        """FileMan._cd(event)

        Change current directory.
        """
        if self._tree.selection():
            item=self._tree.selection()[0]
            path=self._tree.set(item,TREE_COL[0])
            if self._files[path]['is_dir']:
                self._remote.cd(path)
                self._build_tree()

    def _cd_up(self):
        """FileMan._cd_up()

        Goes up one directory.
        """
        if self._remote.pwd() != '/':
            self._remote.cd('..')
            self._build_tree()

    def _rm(self):
        """FileMan._rm()

        Deletes files/folders.
        """
        path=self._tree.selection()
        reply = tkMessageBox.askquestion(type=tkMessageBox.YESNO,
                                         title="Deleting Files",
                                         message="Are you sure?")
        if reply == tkMessageBox.YES:
            try:
                for i in path:
                    self._remote.rm(self._tree.set(i,TREE_COL[0]))
                self._build_tree()
            except Exception as e:
                tkMessageBox.showerror(title='ERROR',message=e)

    def _mkdir(self):
        """FileMan._mkdir()

        Creates a new folder.
        """
        def ok():
            """Callback function when OK is clicked."""
            try:
                self._remote.mkdir(entry.get())
                win.destroy()
                self._build_tree()
            except Exception as e:
                win.destroy()
                tkMessageBox.showerror(title='ERROR',message=e)

       # Create a new dialog to ask for folder name
        entry,win=self._func.create_new_dialog('New Folder',
                                               'Enter folder name',
                                               20,ok)     

    def _upload(self):
        """FileMan._upload()

        Uploads file from PC.
        """
        filename=tkFileDialog.askopenfilename()
        if filename:
            try:
                self._remote.upload(filename,
                                    self._remote.pwd()+'/'+os.path.basename\
                                    (filename))
                self._build_tree()
            except Exception as e:
                tkMessageBox.showerror(title='ERROR',message=e)
    
    def _download(self):
        """FileMan._upload()

        Downloads file to PC.
        """
        filename=tkFileDialog.asksaveasfilename()
        if filename:
            try:
                item=self._tree.selection()[0]
                path=self._tree.set(item,TREE_COL[0])
                self._remote.download(self._remote.pwd()+'/'+path,filename)
            except Exception as e:
                tkMessageBox.showerror(title='ERROR',message=e)

    def _refresh(self,event):
        """FileMan._refresh(event)

        Refreshes tree view.
        """
        self._build_tree()

    def _remove(self,event):
        """FileMan._remove(event)

        Deletes files/folders.
        """
        self._rm()

    def _rename(self,event):
        """FileMan._remove(event)

        Renames files/folders.
        """
        self._func.rename()
        
        
    def _sortby(self,tree,col,descending):
        """Sort tree contents when a column is clicked on.
        Code modified from http://svn.python.org/projects/python/branches/\
        pep-0384/Demo/tkinter/ttk/treeview_multicolumn.py
        
        """
        # Grab values to sort
        data=[(tree.set(child,col),child) for child in tree.get_children('')]

        # Reorder data
        data.sort(reverse=descending)
        for indx,item in enumerate(data):
            tree.move(item[1],'',indx)

        # Switch the heading so that it will sort in the opposite direction
        tree.heading(col,
            command=lambda col=col: self._sortby(tree,col,int(not descending)))

def main():
    root = Tk()
    app=FileMan(root)
    root.mainloop()

if __name__=='__main__':
    main()

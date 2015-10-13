




###################################################################
#
#   CSSE1001 - Assignment 2
#
#   Student Number:
#
#   Student Name:
#
###################################################################


#
# Do not change the following import
#

import MazeGenerator

####################################################################
#
# Insert your code below
#
####################################################################

from Tkinter import *
import tkFileDialog
import tkMessageBox

# Useful constants of maze elements
WALL='#'
FINISH='X'
FLOOR=' '
PLAYER='O'
DIRECTIONS={'Up':(-1,0),'Down':(1,0),'Left':(0,-1),'Right':(0,1)}

class MazeApp(object):
    """Frontend maze solver GUI."""
    def __init__(self, master):
        """MazeApp.__init__(instance)

        Initialises MazeApp.
        
        """
        # Top level window configurations
        self._maze_gen=MazeGenerator.MazeGenerator()
        self._master=master
        self._master.title('Maze Solver')
        self._master.minsize(300,300)
        # Bind arrow keys
        master.bind('<Left>',self._move)
        master.bind('<Right>',self._move)
        master.bind('<Up>',self._move)
        master.bind('<Down>',self._move)

        # Create the menu bar
        menubar=Menu(master)
        master.config(menu=menubar)
        filemenu=Menu(menubar)
        menubar.add_cascade(label='File',menu=filemenu)
        filemenu.add_command(label='Open Maze File',command=self._open_file)
        filemenu.add_command(label='Save Maze File',command=self._save_file)
        filemenu.add_command(label='Exit',command=self._close)

        # Create and pack the canvas
        self._canvas=Canvas(master,bg='black',bd=2,relief=SUNKEN)
        self._canvas.pack(side=TOP,expand=True)

        # Create the main frame for the bottom bar
        frame_main=Frame(master)
        # Create the sub frame for the spinbox and 'New' button
        frame_sub=Frame(frame_main,bd=1,relief=SUNKEN)
        # Create and pack the spinbox and 'New' button
        self._sbox=Spinbox(frame_sub,width=5,from_=2,to=20)
        self._sbox.pack(side=LEFT,padx=1)
        Button(frame_sub,text='New',command=self._new).pack(side=LEFT,
                                                         padx=1,pady=1)
        # Pack the sub frame
        frame_sub.pack(side=LEFT)
        # Create and pack the 'Reset' and 'Quit' buttons
        Button(frame_main,text='Reset',command=self._reset).pack(\
        side=LEFT,expand=True)
        Button(frame_main,text='Quit',command=self._close).pack(\
        side=LEFT)
        # Pack the main frame
        frame_main.pack(side=TOP,expand=True,padx=20,fill=X)

    def _draw(self):
        """MazeApp._draw()

        Draws the maze boxes on the canvas. All boxes start in black colour.
        
        """
        self._canvas.delete(ALL) # Clear the canvas
        size=self._maze.get_size() # Get size of maze
        y=0
        self._itemids=[] # Keep track of the ID of canvas items, stored as list
        # Start drawing maze boxes according to maze size
        while y < size[1]:
            x=0
            boxid=[]
            while x < size[0]:
                tmp=self._canvas.create_rectangle(x*20,y*20,(x+1)*20,(y+1)*20,
                                                  fill='black')
                boxid.append(tmp)
                x+=1
            # ID list, has structure similar to Maze._maze_list
            self._itemids.append(boxid)
            y+=1
            
        self._draw_pos() # Draw the player circle and reveal the first 3x3 boxes

    def _draw_pos(self):
        """MazeApp._draw_pos()

        Draws the player's positions as a circle. Reveals walls,
        floors and end point as player progresses.

        """
        y,x=self._maze.get_pos() # Get position of player

        # Skip deleting of circle on first run, only circle is cleared to avoid
        # excessive deleting of other canvas items
        if '_circleid' in self.__dict__:
            self._canvas.delete(self._circleid)
        # Draw circle and keep track of circle ID
        self._circleid=self._canvas.create_oval(x*20+4,y*20+4,
                                                (x+1)*20-4,(y+1)*20-4,
                                                fill='cyan',
                                                outline='cyan')

        # Reveal maze as player progresses in a 3x3 manner
        for i in range(-1,2):
            r=y+i
            for j in range(-1,2):
                c=x+j
                # Determine the colour of the respective tiles
                if self._maze.get_tile(r,c) == FLOOR:
                    colour='white'
                elif self._maze.get_tile(r,c) == WALL:
                    colour='red'
                else:
                    colour='blue'
                
                self._canvas.itemconfigure(self._itemids[r][c],
                                           fill=colour)

    def _new(self):
        """MazeApp._new()

        Generates a new maze using value from spinbox.

        """
        # Get value from spinbox and generates new maze
        try:
            # Attempt to load the maze (just in case the generator does
            # something wrong)
            self._maze=Maze(self._maze_gen.make_maze(int(self._sbox.get())))
            self._set_size() # Set size of canvas and window
            self._draw() # Initialise the maze
        except Exception as e:
            # Show an error dialog when the maze is invalid
            tkMessageBox.showerror(title='INVALID MAZE',message=e)

    def _open_file(self):
        """MazeApp._open_file()

        Opens and loads a file containing maze characters.

        """
        filename=tkFileDialog.askopenfilename() # Get path and name of file
        # Only attempt to open file if a file is seleted
        if filename:
            with open(filename,'rU') as f:
                try:
                    # Attempt to load the maze
                    self._maze=Maze(f.read())
                    self._set_size() # Set size of canvas and window
                    self._draw() # Initialise the maze
                except Exception as e:
                    # Show an error dialog when the maze file is invalid
                    tkMessageBox.showerror(title='INVALID MAZE',message=e)
        
    def _save_file(self):
        """MazeApp._save_file()

        Saves current maze into a file so that it can be loaded again. 

        """
        filename=tkFileDialog.asksaveasfilename() # Get path and name of file
        # Only attempt to save file if a path and name is given
        if filename:
            # Only attempt to save if a maze is already loaded
            if '_maze' in self.__dict__: 
                # Save maze into file
                with open(filename,'w') as f:
                    f.write(str(self._maze))
            else:
                # Show an error dialog if no maze is loaded
                tkMessageBox.showerror(title='ERROR',
                                       message='No maze loaded yet')
        
    def _reset(self):
        """MazeApp._reset()

        Resets the position of the player.

        """
        # Only attempt to reset maze if a maze is initialised
        if '_maze' in self.__dict__:
            self._maze.reset() # Reset player position
            self._draw() # Redraw the maze

    def _move(self,event):
        """MazeApp._move()

        Player movement.

        """
        # Only attempt to move if a maze is initialised
        if '_maze' in self.__dict__:
            self._maze.move(event.keysym) # Attempt to move player
            self._draw_pos() # Reveal tiles and update player position
            # If reached end point, display dialog
            if self._maze.is_solved():
                tkMessageBox.showinfo(title='Congratulations',
                                      message='We have a winner')

    def _set_size(self):
        """MazeApp._set_size()

        Adjusts canvas and window size according to maze size

        """
        # Get maze dimensions
        size=self._maze.get_size()
        # Set canvas size
        self._canvas.config(width=size[0]*20,height=size[1]*20)
        # Set window size (prevent manual resizing from breaking auto resize)
        self._master.geometry('%dx%d'%(size[0]*20+8,size[1]*20+40))
    
    def _close(self):
        """Maze._close()

        Exits the application.

        """
        self._master.destroy()

class InvalidMaze(Exception):
    """Exception raised for an invalid maze"""
    pass # Only need error message, the rest already handled by Exception

class Maze(object):
    """Holds maze data and position of player."""
    def __init__(self,string):
        """Maze.__init__(string)

        Initialises Maze.
        
        """
        self._maze=string.strip() # Keep track of string representation of maze
        tmp=self._maze.split('\n') # Split maze string into list
        self._maze_list=[list(i) for i in tmp] # Split into list of lists
        self._cur_pos=(1,1) # Initialise player position
        
        test=self._test_maze() # Test if maze is invalid
        if not test[0]:
            raise InvalidMaze(test[1]) # Raise exception with message

    def __str__(self):
        """Maze.__str__() <==> str(Maze)

        Returns string representation of stored maze.

        """
        return self._maze

    def _test_maze(self):
        """Maze._test_maze() -> (bool,string)

        Checks if stored maze is valid. Also returns error message if error is
        found.

        """ 
        occr=0
        count=0

        if len(self._maze_list) < 3 :
            return (False,'Not enough rows') # Maze has too little rows

        for i in self._maze_list:
            if len(i) != len(self._maze_list[0]):
                return (False,'Not all rows are same length') # Rows are uneven
            elif i[0] != WALL or i[-1] != WALL:
                # Either side of maze not made completely of walls
                return (False,'Outside of maze not made '\
                        'up entirely of wall tiles')
            for j in i:
                if count == 0 or count == len(self._maze_list)-1:
                    if j != WALL:
                        # Top and bottom not made completely of walls
                        return (False,'Outside of maze not made '\
                                'up entirely of wall tiles')
                elif j == FINISH:
                    occr+=1
                    if occr > 1:
                        # More than one finish tile
                        return (False,'More than one square '\
                                'representing finish tile')
                elif j != WALL and j != FLOOR and j != FINISH:
                    # Invalid character detected
                    return (False,'Non maze character detected')
            count+=1
        
        if occr < 1:
            # No finish tile
            return (False,'No square representing finish tile')

        return (True,None)

    def move(self,direction):
        """Maze.move(string)

        Moves the player according to direction.
        
        """
        y,x=DIRECTIONS[direction] # Get movement 
        pos=self._cur_pos[0]+y,self._cur_pos[1]+x # Attempt to move

        # Update player position if move is valid
        if self.get_tile(pos[0],pos[1]) != WALL:
            self._cur_pos=pos

    def reset(self):
        """Maze.reset()

        Resets the position of the player.

        """
        self._cur_pos=(1,1)

    def get_size(self):
        """Maze.get_size() -> (tuple)

        Returns dimensions of maze.

        """
        return (len(self._maze_list[0]),len(self._maze_list))

    def get_tile(self,r,c):
        """Maze.get_tile(int,int) -> (string)

        Returns tile type when given position coordinates.

        """
        return self._maze_list[r][c]

    def get_pos(self):
        """Maze.get_pos() -> (tuple)

        Returns current position coordinate of player.

        """
        return self._cur_pos

    def is_solved(self):
        """Maze.is_solved() -> (bool)

        Returns True if maze is solved.

        """
        if self.get_tile(self._cur_pos[0],self._cur_pos[1]) == FINISH:
            return True
        else:
            return False
            
####################################################################
#
# WARNING: Leave the following code at the end of your code
#
# DO NOT CHANGE ANYTHING BELOW
#
####################################################################

def main():
    root = Tk()
    app = MazeApp(root)
    root.mainloop()

if  __name__ == '__main__':
    main()


###################################################################
#
#   CSSE1001 - Assignment 1
#
#   Student Number: 
#
#   Student Name: 
#
###################################################################

#####################################
# Support given below - DO NOT CHANGE
#####################################

HELP = """? - Help.
n - move North one square.
s - move South one square.
e - move East one square.
w - move West one square.
r - Reset to the beginning.
b - Back up a move.
p - List all possible legal directions from the current position.
q - Quit.
"""

WALL = '#'
FINISH = 'X'
FLOOR = ' '
PLAYER = 'O'

# The following dictionary may be useful - you can ignore if you wish.
DIRECTIONS = {'n': (-1, 0), 's': (1, 0), 'e': (0, 1), 'w': (0, -1)}

#####################################
# End of support 
#####################################

# Add your code here

def load_maze(filename):
    """Takes the name of maze file and returns a list of list
    representing the maze file selected.

    Precondition: filename is a string representing the available
    maze files
    
    """
    
    # Initialise variables
    f=open(filename,'rU')
    maze=[]
    maze_all=[]
        
    while True:
        # Read one character at a time
        i=f.read(1)
        """When it detects a newline character, append the temporay list 'maze'
        into the main list 'maze_all'
        Also resets the temporary list 'maze'
        """
        if i == '\n':
            maze_all.append(maze)
            maze=[]
        # Close the file and break the loop when there are no more characters   
        elif not i:
            f.close()
            break
        # Append characters into temporary list
        else:
            maze.append(i)
    return maze_all

def get_position_in_direction(position,direction):
    """Takes a position tuple and direction, then returns the new position.

    Precondition: position is a tuple with 2 values, direction is in the
    DIRECTIONS dictionary
    
    """

    # Initialise variables
    row,column=position
    move1,move2=DIRECTIONS[direction] # Get values from global 'DIRECTIONS'

    new_position=(row+move1,column+move2) # Compute new position

    return new_position

def move(maze,position,direction):
    """Takes a maze list, position tuple and direction,
    then returns the new position if possible, else returns original position.
    Also returns the result of the move as '#', ' ' or 'X'.

    Precondition: maze is a list of lists, position is a tuple with 2 values,
    direction is in the DIRECTIONS dictionary
    
    """

    pos=get_position_in_direction(position,direction) # Propose a new position
    row,column=pos # Assign propsed position to seperate variables
    # Determine kind
    row1=maze[row]
    kind=row1[column]

    # Overwrite pos with original position if kind is found as '#'
    if kind == WALL:
        pos=position

    return (pos,kind)

def print_maze(maze,position):
    """Takes a maze list and position tuple,
    then prints out the maze with 'O' representing the player's position.

    Precondition: maze is a list of lists, position is a tuple with 2 values.
    
    """

    # Initialise variables
    row,column=position
    j=0 # Sets the first list in maze as current list

    # Loop for n times determined by the length of maze
    while j < len(maze):
        # Reset temporay variables after each loop
        output=''
        counter=0
        # Loop for n times determined by the length of current list
        while counter < len(maze[j]):
            # Add player's position as 'O' if hits assigned position
            if counter == column and j == row:
                output+=PLAYER
            else:
                """Add contents of current list
                into a string (output) for formatted printing
                """
                output+=maze[j][counter]
            counter+=1
        print output
        j+=1 # Proceed with next list in maze

def get_possible_directions(maze,position):
    """Takes a maze list and current position tuple,
    then returns the possible moves.

    Precondition: maze is a list of lists, position is a tuple with 2 values.
    
    """
    
    # Initialise empty list
    legal=[]

    # Test for every move available in DIRECTIONS dictionary
    for i in DIRECTIONS:
        """Propose new position by moving according to the
        current direction being tested
        """
        _,kind=move(maze,position,i)
        
        # Add move to list if it is a possibe move
        if kind == FLOOR or kind == FINISH:
            legal.append(i)
    return legal

def interact():
    """Text based user interface

    """

    # Initialise variables
    cur_position=[(1,1)]
    end=0

    # Prompt for maze file
    maze=load_maze(raw_input('Maze File: '))

    """Keep on looping until player specifies to quit or stopped
    by internal statements
    """
    while end != 1:
        print_maze(maze,cur_position[len(cur_position)-1]) # Print maze
        cmd=raw_input('Command: ') # Prompt for player input

        # Print help file
        if cmd == '?':
            print HELP
        
        # Quit program
        elif cmd == 'q':
            while True:
                opt=raw_input('Are you sure you want to quit? [y] or n: ')
                # If player agrees, end program
                if opt == 'y':
                    end=1
                    break
                # Continue main loop if player denies
                elif opt == 'n':
                    break
                # Print an error message if an invalid command is entered
                else:
                    print 'Invalid Command: '+opt
        
        # List possible moves at the current position
        elif cmd == 'p':
            # Initialise variables
            output=''
            # Get possible moves
            possible_move=get_possible_directions(maze,
                                                  cur_position
                                                  [len(cur_position)-1])
            count=len(possible_move)

            # Format string for printing
            for i in possible_move:
                output+=i
                # Append a ',' if more than one character left
                if count > 1:
                    output+=','
                    count-=1
            print 'Possible directions: '+output
    
        # Go back one step
        elif cmd == 'b':
            # Only do this if player is not at starting point
            if len(cur_position) > 1:
                cur_position.pop() # Remove last tuple inside cur_position
        
        # Resets the whole maze
        elif cmd == 'r':
            cur_position=[(1,1)]
        
        # Attempt to move 'O'
        elif cmd in DIRECTIONS:
            out=move(maze,cur_position[len(cur_position)-1],cmd)

            if out[1] == FLOOR:
                # If the move is legal, update current position
                cur_position.append(out[0])
            elif out[1] == FINISH:
                """If reached end point, print congratulations message
                and end program
                """
                print 'Congratulations - you made it!'
                break
            else:
                # If the move is illegal, print warning message
                print 'You can\'t go in that direction'
        
        # Print an error message if an invalid command is entered
        else:
            print 'Invalid Command: '+cmd
                

##################################################
# !!!!!! Do not change (or add to) the code below !!!!!
# 
# This code will run the interact function if
# you use Run -> Run Module  (F5)
# Because of this we have supplied a "stub" definition
# for interact above so that you won't get an undefined
# error when you are writing and testing your other functions.
# When you are ready please change the definition of interact above.
###################################################

if __name__ == '__main__':
    interact()
            

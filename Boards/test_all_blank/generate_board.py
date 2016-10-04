#write out each board element space as a dictionary
#
#Notations being used so far:
#Each board tile is identified in a dictionary by its tuple
#each dictionary can be composed of the following keys:
#boardtile (MANDATORY) - identifies what is the underlying type of tile to be used
#if it is blank, checkpoint, or pit, it will be identified as such
#if it is a conveyor belt, the specific kind of conveyor belt will be listed later
#walls - provides a list of tuples on locations of walls within the tile
#lasers - provides a list of tuples on locations of walls within the tile
#conveyorbelt - provides a dictionary of items representing the type of conveyor belt, the speed, and the orientation of it
#example: 'cb':{'conveyor_type':'straight','speed':'slow','orientation':(0,1)} will produce a straight, slow conveyor belt pointing down
import yaml


#Reminder, (x,y) refers to x as the column, y as the row -> (column, row)
board={(0,0):{'boardtile':'blank'},
(0,1):{'boardtile':'blank'},
(0,2):{'boardtile':'blank'},
(0,3):{'boardtile':'blank'},
(0,4):{'boardtile':'blank'},
(0,5):{'boardtile':'blank'},
(0,6):{'boardtile':'blank'},
(0,7):{'boardtile':'blank'},
(0,8):{'boardtile':'blank'},
(0,9):{'boardtile':'blank'},
(0,10):{'boardtile':'blank'},
(0,11):{'boardtile':'blank'},
(1,0):{'boardtile':'blank'},
(1,1):{'boardtile':'blank'},
(1,2):{'boardtile':'blank'},
(1,3):{'boardtile':'blank'},
(1,4):{'boardtile':'blank'},
(1,5):{'boardtile':'blank'},
(1,6):{'boardtile':'blank'},
(1,7):{'boardtile':'blank'},
(1,8):{'boardtile':'blank'},
(1,9):{'boardtile':'blank'},
(1,10):{'boardtile':'blank'},
(1,11):{'boardtile':'blank'},
(2,0):{'boardtile':'blank'},
(2,1):{'boardtile':'blank'},
(2,2):{'boardtile':'blank'},
(2,3):{'boardtile':'blank'},
(2,4):{'boardtile':'blank'},
(2,5):{'boardtile':'blank'},
(2,6):{'boardtile':'blank'},
(2,7):{'boardtile':'blank'},
(2,8):{'boardtile':'blank'},
(2,9):{'boardtile':'blank'},
(2,10):{'boardtile':'blank'},
(2,11):{'boardtile':'blank'},
(3,0):{'boardtile':'blank'},
(3,1):{'boardtile':'blank'},
(3,2):{'boardtile':'blank'},
(3,3):{'boardtile':'blank'},
(3,4):{'boardtile':'blank'},
(3,5):{'boardtile':'blank'},
(3,6):{'boardtile':'blank'},
(3,7):{'boardtile':'blank'},
(3,8):{'boardtile':'blank'},
(3,9):{'boardtile':'blank'},
(3,10):{'boardtile':'blank'},
(3,11):{'boardtile':'blank'},
(4,0):{'boardtile':'blank'},
(4,1):{'boardtile':'blank'},
(4,2):{'boardtile':'blank'},
(4,3):{'boardtile':'blank'},
(4,4):{'boardtile':'blank'},
(4,5):{'boardtile':'blank'},
(4,6):{'boardtile':'blank'},
(4,7):{'boardtile':'blank'},
(4,8):{'boardtile':'blank'},
(4,9):{'boardtile':'blank'},
(4,10):{'boardtile':'blank'},
(4,11):{'boardtile':'blank'},
(5,0):{'boardtile':'blank'},
(5,1):{'boardtile':'blank'},
(5,2):{'boardtile':'blank'},
(5,3):{'boardtile':'blank'},
(5,4):{'boardtile':'blank'},
(5,5):{'boardtile':'blank'},
(5,6):{'boardtile':'blank'},
(5,7):{'boardtile':'blank'},
(5,8):{'boardtile':'blank'},
(5,9):{'boardtile':'blank'},
(5,10):{'boardtile':'blank'},
(5,11):{'boardtile':'blank'},
(6,0):{'boardtile':'blank'},
(6,1):{'boardtile':'blank'},
(6,2):{'boardtile':'blank'},
(6,3):{'boardtile':'blank'},
(6,4):{'boardtile':'blank'},
(6,5):{'boardtile':'blank'},
(6,6):{'boardtile':'blank'},
(6,7):{'boardtile':'blank'},
(6,8):{'boardtile':'blank'},
(6,9):{'boardtile':'blank'},
(6,10):{'boardtile':'blank'},
(6,11):{'boardtile':'blank'},
(7,0):{'boardtile':'blank'},
(7,1):{'boardtile':'blank'},
(7,2):{'boardtile':'blank'},
(7,3):{'boardtile':'blank'},
(7,4):{'boardtile':'blank'},
(7,5):{'boardtile':'blank'},
(7,6):{'boardtile':'blank'},
(7,7):{'boardtile':'blank'},
(7,8):{'boardtile':'blank'},
(7,9):{'boardtile':'blank'},
(7,10):{'boardtile':'blank'},
(7,11):{'boardtile':'blank'},
(8,0):{'boardtile':'blank'},
(8,1):{'boardtile':'blank'},
(8,2):{'boardtile':'blank'},
(8,3):{'boardtile':'blank'},
(8,4):{'boardtile':'blank'},
(8,5):{'boardtile':'blank'},
(8,6):{'boardtile':'blank'},
(8,7):{'boardtile':'blank'},
(8,8):{'boardtile':'blank'},
(8,9):{'boardtile':'blank'},
(8,10):{'boardtile':'blank'},
(8,11):{'boardtile':'blank'},
(9,0):{'boardtile':'blank'},
(9,1):{'boardtile':'blank'},
(9,2):{'boardtile':'blank'},
(9,3):{'boardtile':'blank'},
(9,4):{'boardtile':'blank'},
(9,5):{'boardtile':'blank'},
(9,6):{'boardtile':'blank'},
(9,7):{'boardtile':'blank'},
(9,8):{'boardtile':'blank'},
(9,9):{'boardtile':'blank'},
(9,10):{'boardtile':'blank'},
(9,11):{'boardtile':'blank'},
(10,0):{'boardtile':'blank'},
(10,1):{'boardtile':'blank'},
(10,2):{'boardtile':'blank'},
(10,3):{'boardtile':'blank'},
(10,4):{'boardtile':'blank'},
(10,5):{'boardtile':'blank'},
(10,6):{'boardtile':'blank'},
(10,7):{'boardtile':'blank'},
(10,8):{'boardtile':'blank'},
(10,9):{'boardtile':'blank'},
(10,10):{'boardtile':'blank'},
(10,11):{'boardtile':'blank'},
(11,0):{'boardtile':'blank'},
(11,1):{'boardtile':'blank'},
(11,2):{'boardtile':'blank'},
(11,3):{'boardtile':'blank'},
(11,4):{'boardtile':'blank'},
(11,5):{'boardtile':'blank'},
(11,6):{'boardtile':'blank'},
(11,7):{'boardtile':'blank'},
(11,8):{'boardtile':'blank'},
(11,9):{'boardtile':'blank'},
(11,10):{'boardtile':'blank'},
(11,11):{'boardtile':'blank'}
}
#yaml will store the list of dict
s=yaml.dump(board)
f=open('board_config.txt','w')
f.write(s)
f.close()

#The file is exported to a file which is used to load in the board when used

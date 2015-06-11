#write out each board element space as a dictionary
#
#Notations being used so far:
# wall: indicates a wall on the board. must be prefaced by n_,w_,e_,or s_ to indicate location
# laser: indicates the origin of a laser. must be prefaced by we,ew,ns, or sn. This two character code represents 1. the wall of origin and 2. the firing direction. So 'we_laser' represents a laser on the west wall firing east.
# cb: indicates a conveyor belt.  must be prefaced by n,s,e,w or combinations of the two. n,s,e,and w are straight arrows, while combinations of 2 represent incoming direction and outgoing direction (with rotation). For example, if a belt was 'ne_cb', the belt would be going north and turning east.
# checkpoint: indicates a checkpoint is in this location.
import yaml

board={(1,1):[{walls:[(0,1)]}],
(1,2):['w_wall','we_laser'],
(1,3):['w_wall','n_wall'],
(2,1):['sw_cb'],
(2,2):['s_cb'],
(2,3):['ws_cb'],
(3,1):['w_cb'],
(3,2):['e_wall','checkpoint'],
(3,3):[]}

#yaml will store the list of dict
s=yaml.dump(board)
f=open('test_config.txt','w')
f.write(s)
f.close()

#The file is exported to a file which is used to load in the board when used

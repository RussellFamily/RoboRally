#write out each board element space as a dictionary
#
#Notations being used so far:
# wall: indicates a wall on the board. must be prefaced by n_,w_,e_,or s_ to indicate location
# laser: indicates the origin of a laser. must be prefaced by we,ew,ns, or sn. This two character code represents 1. the wall of origin and 2. the firing direction. So 'we_laser' represents a laser on the west wall firing east.
# cb: indicates a conveyor belt.  must be prefaced by n,s,e,w or combinations of the two. n,s,e,and w are straight arrows, while combinations of 2 represent incoming direction and outgoing direction (with rotation). For example, if a belt was 'ne_cb', the belt would be going north and turning east.
# checkpoint: indicates a checkpoint is in this location.
#
aa={'loc':(1,1),'features':['s_wall','w_wall']}
ab={'loc':(1,2),'features':['w_wall','we_laser']}
ac={'loc':(1,3),'features':['w_wall','n_wall']}
ba={'loc':(2,1),'features':['sw_cb']}
bb={'loc':(2,2),'features':['s_cb']}
bc={'loc':(2,3),'features':['ws_cb']}
ca={'loc':(3,1),'features':['w_cb']}
cb={'loc':(3,2),'features':['e_wall','checkpoint']}
cc={'loc':(3,3),'features':[]}

board=[aa,ab,ac,ba,bb,bc,ca,cb,cc]
import json
s=json.dumps(board)
f=open('test_config.txt','w')
f.write(s)
f.close()

#Classes used in the game
#Game object that starts each game and controls game flow
###########################
class Game():

	def __init__(self):


###########################
#Card object is used by robots to move or rotate, can either be in a deck, discard, hand, or register (locked or unlocked)
###########################
class Card(priority,type):
	#initialize object
	def __init__(self):
		self.priority=priority
		self.type=typerally.py
###########################
#Deck object used by the game to control the movement cards.  Contains the discard and draw pile, and can be shuffled
###########################
class Deck():

	def __init__(self):
		self.deck=[]
		self.discard=[]

###########################
#Player Object is created by the game to represent an individual player.  Has a robot and deck attached to it.
###########################
class Player(name,robot_name):

	def __init__(self):
		self.name=name
		self.robot=Robot(robot_name)
		self.deck=
###########################
#Robot Object is created under a player.  It controls its registers, spot on the board, facing, and damage.
###########################
class Robot(robot_name)

	def __init__(self):
		self.robot_name=robot_name
		#import image used for robot
		self.damage=0
		####HOW SHOULD I INITIALIZE REGISTERS???? Dictionary with phase number as the key?
		self.registers={}
###########################
#Register is an object owned by a robot which represents a container for a phase action and register lock
###########################
class Register(number)

	def __init__(self):
		self.number=number
		self.register_lock=False
		self.card=None

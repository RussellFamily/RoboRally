#Classes used in the game
#Game object that starts each game and controls game flow
###########################
class Game():

	def __init__(self):
		pass

###########################
#Card object is used by robots to move or rotate, can either be in a deck, discard, hand, or register (locked or unlocked)
###########################
class Card():
	#initialize object
	def __init__(self,priority,cardtype):
		self.priority=priority
		self.cardtype=cardtype
###########################
#Deck object used by the game to control the movement cards.  Contains the discard and draw pile, and can be shuffled
###########################
class Deck():

	def __init__(self):
		self.deck=[]
		self.discard=[]
		self.create_deck()
	#create all the cards in the movement deck
	def create_deck(self):
		#create Uturns
		for i in [x for x in range(10,70,10)]:
			newcard=Card(i,'U-turn')
			self.deck.append(newcard)
		for i in [x for x in range(70,430,20)]:
			newcard=Card(i,'Rotate_Left')
			self.deck.append(newcard)
		for i in [x for x in range(80,440,20)]:
			newcard=Card(i,'Rotate_Right')
			self.deck.append(newcard)
		for i in [x for x in range(430,490,10)]:
			newcard=Card(i,'Backup')
			self.deck.append(newcard)
		for i in [x for x in range(490,670,10)]:
			newcard=Card(i,'Move_1')
			self.deck.append(newcard)
		for i in [x for x in range(670,790,10)]:
			newcard=Card(i,'Move_2')
			self.deck.append(newcard)
		for i in [x for x in range(790,850,10)]:
			newcard=Card(i,'Move_3')
			self.deck.append(newcard)
###########################
#Player Object is created by the game to represent an individual player.  Has a robot and deck attached to it.
###########################
class Player():

	def __init__(self,name,robot_name):
		self.name=name
		self.robot=Robot(robot_name)
		self.deck=Deck()
###########################
#Robot Object is created under a player.  It controls its registers, spot on the board, facing, and damage.
###########################
class Robot():

	def __init__(self,robot_name):
		self.robot_name=robot_name
		#import image used for robot
		self.damage=0
		####HOW SHOULD I INITIALIZE REGISTERS???? Dictionary with phase number as the key?
		self.registers={1:None,2:None,3:None,4:None,5:None}
		self.shutdown=False
###########################
#Register is an object owned by a robot which represents a container for a phase action and register lock
###########################
class Register():

	def __init__(self,number):
		self.number=number
		self.register_lock=False
		self.card=None
###########################
#Board will contain an object of board spaces, stored in a 2D array.
###########################
class Board():

	def __init__(self):
		pass

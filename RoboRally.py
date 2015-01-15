#Modules!
import random
import yaml
#Classes used in the game
#Game object that starts each game and controls game flow
###########################
class Game():

	def __init__(self):
		self.playerlist=[]
		self.deck=Deck()
		self.game_setup()
		#hardcoding staring board 'test'
		self.board=Board('test')

	def game_setup(self):
		pname=raw_input('What is the players name?\n')
		self.playerlist.append(Player(pname,'Twonky'))

	#temporary print function used to print the status of the board
	def print_board(self):
		print(' - - L - - - - - - - - - - - - \n')
		print('|         |         |         |\n')
		print('W         |    +--- |  <----  |\n')
		print('|         |    v    |         |\n')
		print(' - - - - - - - - - - - - - - - \n')

	#Function that deals out cards to all players
	def deal_hands(self):
		for player in playerlist:
			if player.robot.shutdown==True:
				pass
			else:
				for i in range(player.robot.damage):
					self.deal_card(player)

	#Function used to deal out a single card to a player.  Used to check if deck is also empty when dealing
	def deal_card(self,player):
		if len(self.deck.draw) ==0:
			self.deck.shuffle_deck()
		player.hand.append(self.deck.draw.pop())

	#Execute move actions of all robots
	def execute_move_phase(self,register):
		moveorder=[]=list(playerlist)
		sorted(moveorder,key=lambda player:player.robot.registers[register].priority)
		for player in moveorder:
			execute_move(player.robot.registers[register].cardtype)

	#Execute individual move action specified by a movement card
	#def execute_move(movetype):

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

	#create draw
	def __init__(self):
		self.draw=[]
		self.discard=[]
		self.create_deck()
		self.shuffle_deck(True)

	#create all the cards in the movement deck
	def create_deck(self):
		#create Uturns
		for i in [x for x in range(10,70,10)]:
			newcard=Card(i,'U-turn')
			self.draw.append(newcard)
		for i in [x for x in range(70,430,20)]:
			newcard=Card(i,'Rotate_Left')
			self.draw.append(newcard)
		for i in [x for x in range(80,440,20)]:
			newcard=Card(i,'Rotate_Right')
			self.draw.append(newcard)
		for i in [x for x in range(430,490,10)]:
			newcard=Card(i,'Backup')
			self.draw.append(newcard)
		for i in [x for x in range(490,670,10)]:
			newcard=Card(i,'Move_1')
			self.draw.append(newcard)
		for i in [x for x in range(670,790,10)]:
			newcard=Card(i,'Move_2')
			self.draw.append(newcard)
		for i in [x for x in range(790,850,10)]:
			newcard=Card(i,'Move_3')
			self.draw.append(newcard)

	#shuffles the deck, used at game start and any time a new deck needs to be formed
	def shuffle_deck(self,init=False):
			#swap discard and draw piles, then shuffle the draw pile.  If init is true, doesn't switch the decks
		if init == False:
			self.draw,self.discard=self.discard,self.draw
		random.shuffle(self.draw)


###########################
#Player Object is created by the game to represent an individual player.  Has a robot and deck attached to it.
###########################
class Player():

	def __init__(self,name,robot_name):
		self.name=name
		self.robot=Robot(robot_name)
		self.hand=[]
###########################
#Robot Object is created under a player.  It controls its registers, spot on the board, facing, and damage.
###########################
class Robot():

	def __init__(self,robot_name):
		self.robot_name=robot_name
		#import image used for robot
		self.damage=0
		self.registers=self.initiate_registers()
		self.shutdown=False


	def initiate_registers(self):
		reg={}
		for i in range(1,6):
			reg[i]=Register(i)
		return reg
###########################
#Register is an object owned by a robot which represents a container for a phase action and register lock
###########################
class Register():

	def __init__(self,number):
		self.number=number
		self.register_lock=False
		self.card=None
###########################
#Board will contain an object of board spaces, stored in a dictionary keyed by an (x,y) pair
###########################
class Board():

	def __init__(self,boardname):
		self.boardname=boardname
		self.board_dict=self.load_board(boardname)

	#load yaml'd dictionary of board elements into an array
	def load_board(self,boardname):
		loaded_dict=yaml.load(open("Boards/"+boardname+"/"+boardname+"_config.txt").read()[:-1])
		bdict={}
		for key,value in loaded_dict.iteritems():
			bdict[key]=Boardspace(key,value)
		return bdict
###########################
#Board game space used to store the location and properties of that space
###########################
class Boardspace():

	def __init__(self,location,features):
		self.location=location
		self.walls=[]
		self.lasers=[]
		self.cb=[False,None]
		self.checkpoint=False
		self.Flag=None
		self.strip_features(features)

	def strip_features(self,features):
		for feature in features:
			if feature=='checkpoint':
				self.checkpoint=True
			elif feature[-5:]=='_wall':
				self.walls.append(feature[:-5])
			elif feature[-3:]=='_cb':
				self.cb=[True,feature[:-3]]
			elif feature[-6:]=='_laser':
				self.lasers.append(feature[:-6])

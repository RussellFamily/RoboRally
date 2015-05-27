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

	def game_setup(self):
		#Determine how many players are going to be playing the game
		num_allowed_players=[2,3,4]
		print 'Welcome to Robo Rally!\n'
		while True:
			try:
				x=int(raw_input('How many players are playing? Valid numbers are 2, 3, and 4.\n'))
			except:
				print 'Not a valid value. Please try again.'
				continue
			else:
				if x in num_allowed_players:
					break
				else:
					print 'Not a valid number of players. Please try again.'
		
		#Determine board to be used - for now will be a test board - and load the dictionary of the board
		self.board='test'
		board_file=open(self.board+'/'+self.board+'_config.txt','r')
		board_dict=yaml.load(board_file)
		
		#Convert board dict to usable input
		
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
		if len(self.deck.draw) == 0:
			self.deck.shuffle_deck()
		player.hand.append(self.deck.draw.pop())

	#Execute move actions of all robots by sorting moves of active players
	def execute_move_phase(register):
		moveorder=[player for player in self.playerlist if player.robot.dead==False and player.robot.shutdown=False]
		moveorder=sorted(moveorder,key=lambda player:player.robot.registers[register].priority)
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
		self.dead=False
		self.num_death=0


	def initiate_registers():
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
	def load_board(boardname):
		loaded_dict=yaml.load(open(boardname+"_config.txt").read()[:-1])
		bdict={}
		for key,value in loaded_dict.iteritems():
			bdict[key]=Boardspce(key,value)
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
		self.strip_features()

	def strip_features():
		for feature in features:
			if feature=='checkpoint':
				self.checkpoint=True
			elif feature[-5:]=='_wall':
				self.walls.append(feature[:-5])
			elif feature[-3:]=='_cb':
				self.cb=[True,feature[:-3]]
			elif feature[-6:]=='_laser':
				self.lasers.append(feature[:-6])

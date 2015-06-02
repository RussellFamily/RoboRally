#Modules!
import random
import yaml
import pygame
import numpy as np
import math
#Classes used in the game
###########################
#Game Object that runs the display, handling updates to the screen
###########################
class Display():
	def __init__(self):
		pygame.init()
		self.screensize=(1200,800)
		self.screen=pygame.display.set_mode(self.screensize)
		



###########################
#Game object that starts each game and controls game flow
###########################

class Game():

	def __init__(self):
		self.playerlist=[]
		self.deck=Deck()
		

	def run_game(self):
		#get the board and players setup to play
		self.game_setup()
		#run game
		self.play_game()
		
		
	def assign_registers(self):
		for player in self.playerlist:
			if not player.robot.shutdown and not player.robot.dead:
				while True:
					#print hand and registers
					player.print_hand()
					player.print_registers()
					
					try:
						card_choice=int(raw_input("Please choose a card you want to play based on the hand above: "))
					except:
						print 'The input was not a valid integer, please try again\n'
						continue
					if card_choice not in range(len(player.hand)):
						print 'The integer was not a valid answer, please try again\n'
						continue
						
					try:
						reg_choice=int(raw_input("Which register do you want to put this card into?: "))
					except:
						print 'The input was not valid'
						continue
					if reg_choice not in range(1,6):
						print 'not a valid register choice'
						continue
					elif player.robot.registers[reg_choice].card != None:
						if player.robot.registers[reg_choice].register_lock==True:
							print 'this register is locked, and cannot be changed'
							continue
						else:
							player.hand.append(player.robot.registers[reg_choice].card)
					
					player.robot.registers[reg_choice].card=player.hand[card_choice]
					#is it pop or drop?
					player.hand.pop(card_choice)
					
					filled_regs=0
					for reg in player.robot.registers:
						if player.robot.registers[reg].card!=None:
							filled_regs+=1
					answer=''
					if filled_regs==5:
						player.print_hand()
						player.print_registers()
						while True:
							answer=raw_input('Is this your final choice for registers (y/n)?')
							if answer=='y':
								break
							if answer=='n':
								break
							else:
								print 'not a valid response, enter again'

					if answer=='y':
						break
		
		
	def play_game(self):
		
		#iterate through rounds of play
		
		#first step is to deal out cards to all players
		self.deal_hands()
		
		#next, each player has to choose which order of cards they will be dealing out
		#for the first iteration, each player will take turns individually choosing all of his/her cards through the terminal
		#they will be told what cards they have in hand, which registers currently have cards chosen in them, and which ones are locked
		#finally they will confirm if the choices are what they will make them out to be

		self.assign_registers()
		
		#time to execute all of the moves register by register
		#execute movement for each register phase
		for i in range(1,6):
			pass

	def game_setup(self):
		#Determine how many players are going to be playing the game
		num_allowed_players=[2,3,4]
		print 'Welcome to Robo Rally!\n'
		while True:
			try:
				num_players=int(raw_input('How many players are playing? Valid numbers are 2, 3, and 4.\n'))
			except:
				print 'Not a valid value. Please try again.'
				continue
			else:
				if num_players in num_allowed_players:
					break
				else:
					print 'Not a valid number of players. Please try again.'
		
		#READ in the names for each player
		#maybe functionalize to reduce code here
		playernames=[]
		for i in range(num_players):
			while True:
				playername=raw_input('What is the name of Player '+str(i)+'?')
				if len(playername)==0:
					print 'Not a valid name. The length of the name must be at least 1 character'
				elif len(playername)>10:
					print 'Not a valid name. The length of the name is too long.'
				elif playername in playernames:
					print 'Not a valid name.  That name has already been taken. Please choose another name'
				else:
					break
			playernames.append(playername)
		#Determine board to be used - for now will be a test board - and load the dictionary of the board
		#self.board='test'
		#board_file=open(self.board+'/'+self.board+'_config.txt','r')
		#board_dict=yaml.load(board_file)
		
		#Convert board dict to usable input
		#TODO
		
		#Assign robots to players - default arrangement for now
		#TODO - make dynamic
		robots=['r1','r2','r3','r4']
		#list comprehension to create list of players
		self.playerlist=[Player(player,robots[i]) for i,player in enumerate(playernames)]
		#The game now has a list of the players, their names, and which robots they are playing!
		#Setup is complete, time to play the game
		
		
	#Function that deals out cards to all players
	def deal_hands(self):
		for player in self.playerlist:
			if player.robot.shutdown==True:
				pass
			else:
				for i in range(10-player.robot.damage):
					self.deal_card(player)

	#Function used to deal out a single card to a player.  Used to check if deck is also empty when dealing
	def deal_card(self,player):
		if len(self.deck.draw) == 0:
			self.deck.shuffle_deck()
		player.hand.append(self.deck.draw.pop())

	#Execute move actions of all robots by sorting moves of active players
	def execute_move_phase(self,register):
		moveorder=[player for player in self.playerlist if player.robot.dead==False and player.robot.shutdown==False]
		moveorder=sorted(moveorder,key=lambda player:player.robot.registers[register].priority)
		for player in moveorder:
			execute_move(player.robot.registers[register].card.cardtype)

	#Execute individual move action specified by a movement card
	#the steps to be performed for each is listed here
	def execute_move(self,movetype):
		if movetype=='Move_3':
			for i in range(3):
				


	def rotate_vector(self, dir_array,theta_deg):
		theta_rad=math.radians(theta_deg)
		rotation_vector=np.array([[math.cos(theta_rad),-math.sin(theta_rad)],[math.sin(theta_rad),math.cos(theta_rad)]])
		final_vector=rotation_vector.dot(dir_array)
		return np.around(final_vector,0)

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

	def __init__(self,name,robot_name='None'):
		self.name=name
		self.robot=Robot(robot_name)
		self.hand=[]
	
	#prints the current hand of the player	
	def print_hand(self):
		print 'PLAYER HAND\n'
		for i,card in enumerate(self.hand):
			print str(i)+":"+card.cardtype+ " : " + str(card.priority)
			
	#prints out current registers of the player's robot
	def print_registers(self):
		print 'CURRENT REGISTERS\n'
		for i in range(1,6):
			register=self.robot.registers[i]
			if register.card==None:
				print str(i) + " : NONE"
			elif register.register_lock==True:
				print str(i)+" : " + register.card.cardtype + " : " + str(register.card.priority) + " LOCKED"
			else:
				print str(i)+" : " + register.card.cardtype + " : " + str(register.card.priority)
			
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
		#positional and directional information for each bot
		self.position=np.array([0,0])
		self.direction=np.array([0,0])


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

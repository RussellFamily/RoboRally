#Modules!
import random
import yaml
import pygame
import numpy as np
import math
import weakref as wr
#Classes used in the game
###########################
#Game Object that runs the display, handling updates to the screen
###########################
class Display():
	def __init__(self,board):
		pygame.init()
		self.screensize=(1200,1200)
		self.screen=pygame.display.set_mode(self.screensize)
		self.board=board
		
		
		
		
	def blitscreen(self,Game):
		self.screen.fill((0,0,0))
		for row in range(12):
			for col in range(12):
				image=self.board.images_dict[self.board.board_dict[(row,col)].boardtile]
				self.screen.blit(image,(row*100,col*100))
		for player in Game.playerlist:
			self.screen.blit(player.robot.image,(player.robot.position[0]*100,player.robot.position[1]*100))
		pygame.display.update()	
		
	#currently the blitscreen needs the positions of the robots, so i'm gonna grab i
	#it from the Game object, there is probably a better way to do this
	#now defunct blitscreen function
	#instead load images upon game creation, instead of loading images
	#everytime we call the blitscreen function
	"""def blitscreen(self,Game):
		self.screen.fill((0,0,0))
		for row in range(len(self.board)):
			for col in range(len(self.board[row])):
				image=pygame.image.load('Images/Board_Elements/'+self.board[row][col]+'.jpg')
				reducedimage=pygame.transform.scale(image,(100,100))
				self.screen.blit(reducedimage,(row*100,col*100))
		for player in Game.playerlist:
			image=pygame.image.load('Images/Robots/'+player.robot.robot_name+'.jpg')
			reducedimage=pygame.transform.scale(image,(100,100))
			self.screen.blit(reducedimage,(player.robot.position[0]*100,player.robot.position[1]*100))

		pygame.display.update()"""
		
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
		#create display with each players robot
		self.display.blitscreen(self)
		#first step is to deal out cards to all players
		self.deal_hands()
		
		#next, each player has to choose which order of cards they will be dealing out
		#for the first iteration, each player will take turns individually choosing all of his/her cards through the terminal
		#they will be told what cards they have in hand, which registers currently have cards chosen in them, and which ones are locked
		#finally they will confirm if the choices are what they will make them out to be

		self.assign_registers()
		
		#time to execute all of the moves register by register
		#execute movement for each register phase
		#require input to begin first movement
		raw_input('Press any key to start movement')
		for i in range(1,6):
			#execute player moves
			self.execute_move_phase(i)
			#print position to check if update is working
			for player in self.playerlist:
				print player.robot.position
			
			#check for death offboard
			self.check_offboard()
			#update board
			self.display.blitscreen(self)
			#require button to go to next phase
			raw_input('press any key to continue')
	#check if players' robots ended up offboard		
	def check_offboard(self):
		for player in self.playerlist:
			if player.robot.position[0]>=0 and player.robot.position[0]<12 and player.robot.position[1]>=0 and player.robot.position[1]<12:
				#robot is fine
				pass
			else:
				player.robot.dead==True
				print player.name+ "'s robot is off the board!\n"
			

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
		#instead, make a board whose only tiles are blank
		#ignore board object for now
		
		#CODE FOR BASIC BOARD
		#board=[['blank']*12]*12
		#self.display=Display(board)
		
		
		#implement blank board, needs to be changed to alternating boards later
		self.board=Board('test_all_blank')
		self.display=Display(self.board)
		#Convert board dict to usable input
		#TODO
		
		
		#Assign robots to players - default arrangement for now
		#TODO - make dynamic
		robots=['player-1','player-2','player-3','player-4']
		#list comprehension to create list of players
		self.playerlist=[Player(player,robots[i]) for i,player in enumerate(playernames)]
		#The game now has a list of the players, their names, and which robots they are playing!
		#Setup is complete, time to play the game
		#initialize robots onto the bottom row for now, will create additional starting positions later
		for i,player in enumerate(self.playerlist):
			player.robot.position=np.array([i,0])
			player.robot.direction=np.array([0,1])
		
		
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
		moveorder=sorted(moveorder,key=lambda player:player.robot.registers[register].card.priority)
		for player in moveorder:
			#execute_move(player.robot.registers[register].card.cardtype)
			player.robot.execute_move(register)
	
	
	

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
		self.image=self.load_image()
		self.damage=0
		self.registers=self.initiate_registers()
		self.shutdown=False
		self.dead=False
		self.num_death=0
		#positional and directional information for each bot
		self.position=np.array([0,0])
		self.direction=np.array([0,0])

	def load_image(self):
		image=pygame.transform.scale(pygame.image.load('Images/Robots/'+self.robot_name+'.jpg'),(100,100))
		return image

	def initiate_registers(self):
		reg={}
		for i in range(1,6):
			reg[i]=Register(i)
		return reg
		
	#Execute individual move action specified by a movement card
	#the steps to be performed for each is listed here
	#for now, movement will be confined to a grid with no restrictions.  Collisions for walls when moving will be handled later
	#probably need another function to handle what happens during a move
	def execute_move(self,register):
		movetype=self.registers[register].card.cardtype
		if movetype=='Move_3':
			for i in range(3):
				self.move_one_square()
		elif movetype=='Move_2':
			for i in range(2):
				self.move_one_square()
		elif movetype=='Move_1':
			for i in range(1):
				self.move_one_square()
		elif movetype=='Backup':
			self.move_one_square(backup=True)
		#since the convention of pygame is to treat the origin in the upper left corner,
		#the rotation is inverted from the unit circle, hence angle changes
		elif movetype=='Rotate_Right':
			self.rotate_robot(90)
		elif movetype=='Rotate_Left':
			self.rotate_robot(-90)
		elif movetype=='U-turn':
			self.rotate_robot(180)
		else:
			print 'NOT A VALID MOVE TYPE'
	
	#time to include collision code for other robots as well as walls
	#other robots should be pushed one square when moved into the way of another robot, and should stop when a movement would coincide with a wall
	#this needs to be recursively called for each robot that may
	def move_one_square(self,backup=False,direction=self.direction):
		#check if the boundary in the direction of movement is a wall - identified by feature in boardspace parameter
		#lookup key for the current boardspace of the robot
		current_space=
		if backup==False:
			self.position=self.position+direction
		else:
			self.position=self.position-direction
	def rotate_robot(self,theta):
		#rotate direction vector of the robot
		self.direction=self.rotate_vector(self.direction,theta)
		#robot the image of the robot to reflect the rotation of the robot
		self.image=pygame.transform.rotate(self.image,-1*theta)
	
	#function that handles rotation of a vector by 90,-90, or 180 degrees and returns the resulting vector
	#reminder, since the convention of pygame is to treat the origin as the upper left corner,
	#we are using an inverted unit circle, so the signs are flipped for rotations
	def rotate_vector(self, dir_array,theta_deg):
		theta_rad=math.radians(theta_deg)
		rotation_vector=np.array([[math.cos(theta_rad),-math.sin(theta_rad)],[math.sin(theta_rad),math.cos(theta_rad)]])
		final_vector=rotation_vector.dot(dir_array)
		return np.around(final_vector,0)
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
		self.images_dict=self.load_images()

	#load yaml'd dictionary of board elements into an array
	def load_board(self,boardname):
		loaded_dict=yaml.load(open("Boards/"+boardname+"/board_config.txt").read()[:-1])
		bdict={}
		for key,value in loaded_dict.iteritems():
			bdict[key]=Boardspace(key,value[0],value[1])
		return bdict
		
	#currently load all board elements into 	
	def load_images(self):
		board_spaces=['blank','checkpoint-1','checkpoint-2','fast','flag','laser','pit','slow','wall']
		image_dict={}
		for space in board_spaces:
			image_dict[space]=pygame.transform.scale(pygame.image.load('Images/Board_Elements/'+space+'.jpg'),(100,100))
		return image_dict
###########################
#Board game space used to store the location and properties of that space
###########################
class Boardspace():

	def __init__(self,location,boardtile,features):
		self.location=location
		self.boardtile=boardtile
		self.walls=[]
		self.lasers=[]
		self.cb=[False,None]
		self.checkpoint=False
		self.Flag=None
		self.strip_features()

	
	#notes for feature coding
	#all features will be coded into the features function as a dictionary
	#walls will be keyed by the word 'walls', then following a list of all walls in that board space, identified by tuples as the direction of the square
	#lasers will be keyed similarly, with instead a tuple of the initial laser point - the board will need to determine which squares the laser passes through and where it terminates
	def strip_features(self):
		pass
		"""for feature in features:
			if feature=='checkpoint':
				self.checkpoint=True
			elif feature[-5:]=='_wall':
				self.walls.append(feature[:-5])
			elif feature[-3:]=='_cb':
				self.cb=[True,feature[:-3]]
			elif feature[-6:]=='_laser':
				self.lasers.append(feature[:-6])"""

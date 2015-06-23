#Modules!
import sys
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
		#blit boardtiles
		for row in range(12):
			for col in range(12):
				#blit the board tile
				image=self.board..board_dict[(row,col)].boardtile_image
				self.screen.blit(image,(row*100,col*100))
				#if there are any walls, blit the walls on top of the tile
				#this overwrites the tile for now, until transparent pngs get used
				wall_list=self.board.board_dict[(row,col)].walls
				for direction in wall_list:
					blit_image=self.board.determine_wall_orientation(tuple(direction))
					self.screen.blit(blit_image,(row*100,col*100))
		#finally, blit player robots
		for player in Game.playerlist:
			self.screen.blit(player.robot.image_dict[tuple(player.robot.direction)],(player.robot.position[0]*100,player.robot.position[1]*100))
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
		self.end=False
		#default setting for now, need to implement selection of flags to place on board, or build it into the board property
		self.num_flags=5

	def run_game(self):
		#get the board and players setup to play
		self.game_setup()
		#run game
		while not self.end:
			self.play_game_round()
		print 'GAME OVER!!!!!'
		
	def read_player_choices(self,player):
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
	
	def assign_registers(self):
		for player in self.playerlist:
			if not player.robot.shutdown and not player.robot.dead:
				self.read_player_choices(player)
	
	#ADDED: function also checks for any repairs to be made to robots
	#only handles single checkpoints for now	
	#function that will restore cards to the discard pile out of players hands, except those that are shutdown	
	def cleanup(self):
		#determine any damage removal from checkpoints
		for player in self.playerlist:
			if self.board.board_dict[tuple(player.robot.postition)].checkpoint==True:
				if player.robot.damage>0:
					player.robot.heal_damage(1)
					
		#cleanup cards for the next round
		for player in self.playerlist:
			
			for card in player.hand:
				self.deck.discard=self.deck.discard+player.hand
				player.hand=[]
			if player.robot.shutdown==False:
				for register_num, register in player.robot.registers.iteritems():
					if register.register_lock==False:
						self.deck.discard.append(register.card)
						register.card=None
	
	def play_game_round(self):
		
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
		#allow each player to shutdown their robot for the following turn:
		self.determine_shutdown()
		#execute all of the register phases
		self.complete_registers()
		#update shutdown flags for robots
		self.update_shutdown()
		#respawn any dead robots
		self.respawn_dead_robots()
		#discard unlocked registers and extra cards in hands to all players
		self.cleanup()
	
	def determine_shutdown(self):
		for player in self.playerlist:
			while True:
				shutdown_answer=raw_input('Player '+player.name+': Do you wish to shutdown for the following round? (y|n)')
				if shutdown_answer in ['y','n']:
					if shutdown_answer=='y':
						player.declare_shutdown=True
					break
				else:
					print 'Invalid response'
	
	def complete_registers(self):
		#print final registers before executing phases
		for player in self.playerlist:
			print player.name
			player.print_registers()
		
		#time to execute all of the moves register by register
		#execute movement for each register phase
		#require input to begin first movement
		
		#execute movement, board elements, lasers, and checkpoints
		raw_input('Press any key to start movement')
		for i in range(1,6):
			#execute player moves
			self.execute_move_phase(i)
			#print position to check if update is working
			for player in self.playerlist:
				print player.robot.position,player.robot.direction
			#this is where board elements will go
		
			#fire the lasers!
			self.fire_laser_phase()
			#this is where checkpoint touches will go
			self.checkpoint_phase()			
			#update board
			self.display.blitscreen(self)
		
		#currently ask to quit the game, as currently no other function allows for this
		#allows for a single round of testing and quitting
		quitgame=raw_input('Do you wish to quit the game? (q)')
		if quitgame=='q':
			sys.exit()
	#updates robots who were shut down and who are about to shut down
	def update_shutdown(self):
		# if a robot is not dead and was previously shutdown, remove the shutdown condition
		for player in self.playerlist:
			if player.robot.shutdown==True and player.robot.dead==False:
				player.robot.shutdown=False
		# for all robots preparing to shutdown, change their condition to shutdown, remove their damage, and set register lock flags to False
		for player in self.playerlist:
			if player.declare_shutdown==True and player.robot.dead==False:
				player.declare_shutdown=False
				player.robot.shutdown=True
				player.robot.damage=0
				for register_num,register in player.robot.registers.iteritems():
					register.register_lock=False
	
	def respawn_dead_robots(self):
		#for those robots that have died, determine respawn positions
		for player in self.playerlist:
			if player.robot.dead==True:
				#first things first, remove the death flag!
				player.robot.dead=False
				#in case a robot died while shutdown, remove the shutdown flag
				player.robot.shutdown=False
				#robot comes back at archive location
				player.robot.position=player.robot.archive
				#determine whether they want to come in shut down or up and running
				print 'Player '+player.name+', You can choose to:'
				print '1. Come back into play shutdown for the following round with 0 damage'
				print '2. Come back into play active for the following round with 2 damage'
				
				
				#TODO FIX THE rawinput statements to reflect adjusting the value to an integer
				while True:
					try:
						after_dead_result=int(raw_input('How would you like to come back into play? (Please select 1 or 2)'))
					except:
						print 'Invalid response. Input was not an integer. The only valid inputs are 1 or 2'
						continue
					if after_dead_result not in [1,2]:
						print 'Invalid response. Please enter 1 or 2.'
					else:
						break
				if after_dead_result==1:
					player.robot.shutdown==True
					player.robot.damage=0
				elif after_dead_result==2:
					player.robot.damage=2
				else:
					print 'ERROR IN RESPAWN PROCESS'
				#clear register locks if any were locked
				for register_num,register in player.robot.registers.iteritems():
					register.register_lock=False	
				#determine what direction they will be facing
				print 'You need to select a direction upon respawn.'
				print '1. Up'
				print '2. Down'
				print '3. Left'
				print '4. Right'
				while True:
					try:
						after_dead_direction=int(raw_input('Which direction would you like to face?'))
					except:
						print 'Invalid response. The value must be an integer from 1 to 4'
						continue
					
					if after_dead_direction not in [1,2,3,4]:
						print 'Invalid response. Please enter 1,2,3, or 4'
						continue
					else:
						if after_dead_direction==1:
							player.robot.direction=np.array([0,-1])
						elif after_dead_direction==2:
							player.robot.direction=np.array([0,1])
						elif after_dead_direction==3:
							player.robot.direction=np.array([-1,0])
						elif after_dead_direction==4:
							player.robot.direction=np.array([1,0])
						else:
							print 'ERROR IN ASSIGNING DIRECTION'
							player.robot.direction=np.array([-1,-1])
						break
	#old function, use newer function that does it by robot
	#check if players' robots ended up offboard		
	"""def check_offboard(self):
		for player in self.playerlist:
			if player.robot.position[0]>=0 and player.robot.position[0]<12 and player.robot.position[1]>=0 and player.robot.position[1]<12 and player.robot.dead==False:
				#robot is fine or already dead
				pass
			else:
				player.robot.dead=True
				print player.name+ "'s robot is off the board!\n"
				player.robot.position=(-1,-1)
				player.robot.num_death+=1"""
	
	def check_offboard(self,robot):
		if robot.dead==True:
			#robot is already dead, so do nothing
			pass
		elif robot.position[0]>=0 and robot.position[0]<12 and robot.position[1]>=0 and robot.position[1]<12:
			#robot is on the board
			pass
		else:
			#robot was alive, and now must be offboard
			robot.dead=True
			print robot.robot_name+ " is off the board!\n"
			robot.position=(-1,-1)
			robot.num_death+=1
	
	#checks if the robot has fallen into pit
	def check_pit(self,robot):
		if robot.dead==False:
			if self.board.board_dict[tuple(robot.position)].pit==True:
				robot.dead=True
				print robot.name+' fell into a pit!\n'
				player.robot.position=(-1,-1)
	
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
		self.board=Board('test_walls')
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
			player.robot.archive=player.robot.position
		
	#Function that deals out cards to all players
	def deal_hands(self):
		for player in self.playerlist:
			if player.robot.shutdown==True:
				pass
			else:
				for i in range(9-player.robot.damage):
					self.deal_card(player)

	#Function used to deal out a single card to a player.  Used to check if deck is also empty when dealing
	def deal_card(self,player):
		if len(self.deck.draw) == 0:
			self.deck.shuffle_deck()
		player.hand.append(self.deck.draw.pop())

	#Execute move actions of all robots by sorting moves of active players
	def execute_move_phase(self,register):
		moveorder=[player for player in self.playerlist if player.robot.dead==False and player.robot.shutdown==False]
		moveorder=sorted(moveorder,key=lambda player:player.robot.registers[register].card.priority,reverse=True)
		
		for player in moveorder:
			#test to see if a robot is dead, if it is then it doesn't do its move
			if player.robot.dead==False:
				#execute_move(player.robot.registers[register].card.cardtype)
				self.execute_move(register,player.robot)
				self.display.blitscreen(self)
				raw_input('press any key to continue')

	
	#move functions are now handled by the Game class, so that it can handle collisions	
	#Execute individual move action specified by a movement card
	#the steps to be performed for each is listed here
	#for now, movement will be confined to a grid with no restrictions.  Collisions for walls when moving will be handled later
	#probably need another function to handle what happens during a move
	def execute_move(self,register,robot):
		movetype=robot.registers[register].card.cardtype
		if movetype=='Move_3':
			for i in range(3):
				temp=self.move_one_square(robot,robot.direction)
		elif movetype=='Move_2':
			for i in range(2):
				temp=self.move_one_square(robot,robot.direction)
		elif movetype=='Move_1':
			for i in range(1):
				temp=self.move_one_square(robot,robot.direction)
		elif movetype=='Backup':
			backup_dir=robot.direction*-1
			temp=self.move_one_square(robot,backup_dir,backup=True)
		#since the convention of pygame is to treat the origin in the upper left corner,
		#the rotation is inverted from the unit circle, hence angle changes
		elif movetype=='Rotate_Right':
			self.rotate_robot(90,robot)
		elif movetype=='Rotate_Left':
			self.rotate_robot(-90,robot)
		elif movetype=='U-turn':
			self.rotate_robot(180,robot)
		else:
			print 'NOT A VALID MOVE TYPE'
	
	#time to include collision code for other robots as well as walls
	#other robots should be pushed one square when moved into the way of another robot, and should stop when a movement would coincide with a wall
	#this needs to be recursively called for each robot that may
	def move_one_square(self,robot,direction,backup=False):
		#test to see if the robot is dead, if it is we won't do any collision testing
		if robot.dead==True:
			return 'dead'
		#first test to see if colliding into wall, as a robot in the next square is not push if a wall seperates them
		wall_collision=False
		current_position=robot.position
		destination_position=current_position+direction
		try:
			if tuple(direction) in self.board.board_dict[tuple(current_position)].walls:
				wall_collision=True
			else:
				if tuple(destination_position) in self.board.board_dict:
					if tuple(direction*-1) in self.board.board_dict[tuple(destination_position)].walls:
						wall_collision=True
		except:
			print robot.robot_name
			print 'death',robot.dead
			print 'curpos',current_position
			print 'robdir',robot.direction
			print 'dir',direction
		
		
			
		robot_collision=False
	
		#test for collision of robots
		if wall_collision==False:
			colliding_robot=None
			for player in self.playerlist:
				if tuple(player.robot.position)==tuple(robot.position+direction):
					robot_collision=True
					colliding_robot=player.robot
					#can only be one, so we need to break the loop
					break
			if robot_collision==True:
				collision_result=self.move_one_square(colliding_robot,direction)
				if collision_result=='wall':
					wall_collision=True

		#print out robot variables to understand what the variables are after each movement
		print robot.robot_name,'wall_collision',wall_collision,'robot_collision',robot_collision,'position',robot.position


		if wall_collision==True:
			return 'wall'
		else:
			#move robot one square
			robot.position=robot.position+direction
			#test for death conditions
			self.check_offboard(robot)
			self.check_pit(robot)

			return 'no_wall'
		
	def rotate_robot(self,theta,robot):
		#rotate direction vector of the robot
		robot.direction=self.rotate_vector(robot.direction,theta)
		#robot the image of the robot to reflect the rotation of the robot
		#robot.image=pygame.transform.rotate(robot.image,-1*theta)
	#function that handles rotation of a vector by 90,-90, or 180 degrees and returns the resulting vector
	#reminder, since the convention of pygame is to treat the origin as the upper left corner,
	#we are using an inverted unit circle, so the signs are flipped for rotations
	def rotate_vector(self, dir_array,theta_deg):
		theta_rad=math.radians(theta_deg)
		rotation_vector=np.array([[math.cos(theta_rad),-math.sin(theta_rad)],[math.sin(theta_rad),math.cos(theta_rad)]])
		final_vector=rotation_vector.dot(dir_array)
		
		return np.around(final_vector,0)
	
	
	#need to write a function that handles the laser fire round, both of robots and of board lasers
	#neither board lasers nor robot lasers pass through a robot, so the laser only fires until it hits a robot, wall, or edge of the board
	#timing for lasers is simultaneous
	#for future use of option cards, this is the steps:
	#1. resolve all damaging weapons first (simultaneously)
	#2. resolve all moving and other weapons in order of robot priority card numbers
	#3. if the weapon damages and moves, resolve the damage during step 1, then then effect during step 2
	# Due to the simultaneous nature of laser fire, a stack will need to be created that stores all robot laser fire that will occur,
	# then assign all the effects in the stack.
	# This prevents robots from missing being able to fire due to dying while iterating, and assigns all damage to the robot it is going to hit,
	# even if there is overkill damage (such as 2 lasers hitting a robot with 9 damage, both should hit it, instead of one killing him then the other
	# firing free of impedence
	#The main difference between board and laser fire is the origin square of the laser:
	#board lasers will hit the square they are in, while robot lasers start in the square in the direction they are facing
	#(unless there happens to be a wall immediately in the direction he is facing
	
	#another note: lasers are being stored as tuples, and locations as numpy arrays.  the function should take
	#a numpy array in order to do vector addition, and check against a tuple-ized version for value comparison
	
	def fire_laser_phase(self):
		fire_list=self.board_laser_fire()+self.robot_laser_fire()
		for robot in fire_list:
			robot.assign_damage(1)
			print robot.robot_name+' just took a point of laser damage! They have now taken ' + robot.robot_name + ' damage!'
	
	
	#this function currently only handles single laser board fire, needs to be modified for double lasers
	#these could be stored as two instances of the laser in the board space object? then they can be iterated over
	def fire_laser(self,location,direction,origin):
		current_space=location
		laser_target_flag=False
		target=None
		close_wall=direction
	
		far_wall=self.rotate_vector(direction,180)
		#if the origin is a board laser, check the space immediately in front of it, else, check for the edge of the space to begin wall detection
		if origin=='board':
			for player in self.playerlist:
				if tuple(player.robot.position)==tuple(current_space):
					return player.robot
		#check for current wall space, check if next space is off board, then advance to next space if not, check closest wall, then check for robot in the square
		while not laser_target_flag:
			#check the far wall on the current space
			if tuple(far_wall) in self.board.board_dict[tuple(current_space)].walls:
				#laser has hit a wall, and stops
				laser_target_flag=True
				continue
			#check to see if the laser is off the board
			current_space+=direction
			if current_space[0]>11 or current_space[0]<0 or current_space[1]>11 or current_space[1]<0:
				#next space is off board, laser not terminated by wall
				laser_target_flag=True
				continue
			#check close wall of next space
			if tuple(close_wall) in self.board.board_dict[tuple(current_space)].walls:
				#laser has hit a wall, and stops
				laser_target_flag=True
				continue
			#finally, check again for robots
			for player in self.playerlist:
				if tuple(player.robot.position)==tuple(current_space):
					return player.robot
			
			
		#if it breaks out after not finding a robot, return None
		return None	
	
	def robot_laser_fire(self):
		to_fire=[]
		for player in self.playerlist:
			if player.robot.dead==False:
			laser_origin,laser_direction=player.robot.position,player.robot.direction
			laser_hit=self.fire_laser(laser_origin,laser_direction,'robot')
			if laser_hit is not None:
				to_fire.append(laser_hit)
		return to_fire
	def board_laser_fire(self):
		#fire board lasers
		#array of lasers to be stored on a stack
		to_fire=[]
		for laser_loc in self.board.lasers:
			lasers=self.board.board_dict(tuple(laser_loc))
			for laser in lasers:
				laser_origin,laser_direction=laser_loc,laser
				#board laser vals need to be converted to numpy arrays
				laser_hit=self.fire_laser(np.array(laser_origin),np.array(laser_direction),'board')
				if laser_hit is not None:
					to_fire.append(laser_hit)
		return to_fire

	#checkpoint phase of the register, allow for robots who are on a checkpoint to update their archive, and touch flags
	def checkpoint_phase(self):
		for player in self.playerlist:
			if self.board.board_dict[tuple(player.robot.position)].flag==True:
				if player.robot.next_flag==self.board.board_dict[tuple(player.robot.position)].flag_num:
					print player.robot.robot_name+' has touched Flag ' + player.robot.next_flag+'!'
					if player.robot.next_flag==self.num_flags:
						print player.name + ' has touched the last the last flag and won the game! Congrats!'
						raw_input('Press enter to quit')
						sys.quit()
					else:
						player.robot.next_flag+=1
			if self.board.board_dict[tuple(player.robot.position)].checkpoint==True:
				while True:
					answer=raw_input("You've reached a checkpoint! Do you want to update your archive to this location? (y|n)")
					if answer not in ['y','n']:
						print 'Invalid response. Please enter y or n.'
					elif answer=='y':
						player.robot.archive=player.robot.position
				
	
	#Board elements! Only working on conveyor belts for this iteration, but it will all be wrapped int the board element function
	
	def execute_board_elements(self):
		
	#Conveyor Belts!
	#only need to execute conveyor belt spaces that robots are on, use their keys to check if conveyor belts exist
	
	#notes for thoughts behind convention to program conveyor belts:
	#the trick with conveyor belts is when the following square will rotate the robot in some fashion
	#to be dynamic, the previous square has no knowledge of the rotation: the robot MUST check the square he is entering
	#there will be a directional attribute relative to the space that can be checked against to see if the robot is to rotate or not
	#this attribute needs to be dynamically changed for the boardspace at time of tile creation
	#as a board tile can have 4 seperate orientations
	#i can probably leverage the rotation vector function in order to create the correct in vectors
	# a conveyor belt will have an out vector, as well as in vectors
	# i believe the way this is programmed that when a conveyor belt merges onto another, it will ALWAYS rotate
	#but just in case, it will check the origin direction of the robot, see if that has a rotation direction
	#and if there is a rotation, apply the cooresponding rotation
	#however, you MUST check whether the next space is a conveyor belt first
	#QUESTION: will the conveyor belt be its own object to check against?
	#i believe it should be, and the boardspace links to this object which it can check against
	#it will mostly be a storage of values relative to the space
	def execute_conveyor_belts(self):
	
	
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
		self.declare_shutdown=False
	
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
		self.image_dict=self.create_image_dict()
		self.damage=0
		self.registers=self.initiate_registers()
		self.shutdown=False
		self.dead=False
		self.num_death=0
		#positional and directional information for each bot
		self.position=np.array([0,0])
		self.direction=np.array([0,0])
		self.archive=np.array([0,0])
		#a variable to store what the next flag to touch is
		self.next_flag=1

	def load_image(self):
		image=pygame.transform.scale(pygame.image.load('Images/Robots/'+self.robot_name+'.jpg'),(100,100))
		return image

	def initiate_registers(self):
		reg={}
		for i in range(1,6):
			reg[i]=Register(i)
		return reg
	
	#instead of rotating the robots images, for now simply prerotate all directions and call the one that matches the value of the robot's direction
	def create_image_dict(self):
		image_dict={}
		image_dict[(0,1)]=self.image
		image_dict[(0,-1)]=pygame.transform.rotate(self.image,180)
		image_dict[(1,0)]=pygame.transform.rotate(self.image,90)
		image_dict[(-1,0)]=pygame.transform.rotate(self.image,-90)
		return image_dict
	
	def assign_damage(self,damage):
		for i in range(damage):
			self.damage+=1
			if self.damage>=10:
				self.dead=True
				self.num_death+=1
				break
			elif self.damage>4:
				register_to_lock=10-self.damage
				self.registers[register_to_lock].register_lock=True
	
	def heal_damage(self,damage):
		for i in range(damage):
			if self.damage==0:
				break
			elif self.damage<5:
				self.damage-=1
			elif self.damage<10:
				register_to_unlock=10-self.damage
				self.registers[register_to_unlock].register_lock=False
				self.damage-=1
##########################
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
		self.lasers=[]

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
		
	#have the board control rotations of the wall image when blitting the screen
	#this may later want to be turned into a dictionary of prerotated images that can be called in the image_dict	
	def determine_wall_orientation(self,wall_direction):
		base_image=self.images_dict['wall']
		if wall_direction==(0,1):
			return base_image
		elif wall_direction==(0,-1):
			return pygame.transform.rotate(base_image,180)
		elif wall_direction==(1,0):
			return pygame.transform.rotate(base_image,90)
		elif wall_direction==(-1,0):
			return pygame.transform.rotate(base_image,-90)
		else:
			print 'WALL IMAGE ERROR'

	#a function that locations and assigns all the board space keys for firing lasers
	def locate_lasers(self):
		all_lasers=[]
		for key, value in self.board_dict.iteritems():
			if len(value.walls)>0:
				all_lasers.append(key)
		return all_lasers

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
		self.flag=False
		self.flag_num=None
		#define load board tile
		self.boardtile_image=None
		self.strip_features(features)
		self.pit=False
		
	
	def load_board_tile(self):
		if self.boardtile=='cb':
			pygame.transform.scale(pygame.image.load('Images/Board_Elements/'++'.jpg'),(100,100))
	
	#notes for feature coding
	#all features will be coded into the features function as a dictionary
	#walls will be keyed by the word 'walls', then following a list of all walls in that board space, identified by tuples as the direction of the square
	#lasers will be keyed similarly, with instead a tuple of the initial laser point - the board will need to determine which squares the laser passes through and where it terminates
	
	#notes for conveyor belts
	#conveyor belts should be identified as what type of movement they are, followed by their orientation
	#types of basic movement names: straight, rotate right, rotate left
	#more advanced merges: merge straight/left, merge straight/right, merge left/right, merge straight/left/right
	#how to program merges? need to know direction of origin relative to the square to determine type of rotation if any
	#solving this will trickle down to the easier parts to program
	
	def setup_boardspace(self,features):
		if self.boardtile=='cb':
			
		elif self.boardtile=='blank':
			
		elif self.boardtile=='pit':
	
		elif self.
		
	#this function will now check for walls, lasers, and flags in the features
	def strip_features(self,features):
		
		for feature in features:
			if feature=='checkpoint':
				self.checkpoint=True
			elif feature=='wall':
				self.walls=features[feature]
			elif feature=='cb':
				self.cb=[True,Conveyor_Belt(features[feature])]
				#rotate_image
				self.rotate_image(features[feature]['orientation'])
			elif feature=='laser':
				self.lasers=features[feature]
			else:
				
				print 'INVALID FEATURE SELECTED'
				print feature
	
	def rotate_image(self,orientation):
		if orientation==(0,1):
			pass
		elif orientation==(0,-1):
			self.boardtile_image= pygame.transform.rotate(self.boardtile_image,180)
		elif orientation==(1,0):
			self.boardtile_image= pygame.transform.rotate(self.boardtile_image,90)
		elif orientation==(-1,0):
			self.boardtile_image= pygame.transform.rotate(self.boardtile_image,-90)
		else:
			print 'ERROR, INVALID ORIENTATION'
########################
#A class to store an instance of a Conveyor Belt, and the location properties of said piece
########################


class Conveyor_Belt():
	#the default direction for each piece will be (0,1) -> pointing 'up' towards the positive y axis, in the down direction
	def __init__(self,features):
		self.orientation=features['orientation']
		self.conveyor_type=features['conveyor_type']
		self.conveyor_out=self.orientation
		self.conveyor_in=self.initialize_conveyor_properties(features['conveyo
		
	def initialize_conveyor_properties(self):
		#first, identify the type of piece 

import sys
import random
import yaml
import pygame
import numpy as np
import math
import ConfigParser
import os
import RoboRally as RR

class TestGame(RR.Game)
    def game_setup(self):
        # Determine how many players are going to be playing the game
        num_allowed_players = [2, 3, 4]
        print 'Welcome to Robo Rally!\n'
        print '\nNumber of Players is 2!'
        num_players=2
        # READ in the names for each player
        # maybe functionalize to reduce code here
        playernames = ['RAZ','PM8K']

        print '\nRAZ and PM8K are playing this game!'


        # implement named test board, needs to be changed to alternating boards
        # later
        self.board = Board(self.test_get_boards())
        self.display = Display(self.board)

        # determine flag setup
        self.test_setup_flags()

        # Assign robots to players - default arrangement for now
        # TODO - make dynamic
        robots = ['robot1', 'robot2', 'robot3', 'robot4']
        # list comprehension to create list of players
        self.playerlist = [Player(player, robots[i])
                           for i, player in enumerate(playernames)]
        # The game now has a list of the players, their names, and which robots they are playing!
        # Setup is complete, time to play the game
        # initialize robots onto the bottom row for now, will create additional
        # starting positions later
        for i, player in enumerate(self.playerlist):
            player.robot.position = np.array([i, 0])
            player.robot.direction = np.array([0, 1])
            player.robot.archive = player.robot.position

    def get_boards(self):
        return 'cross'

    def test_setup_flags(self):
        # determine how many flags to touch to end the game
        flag_int = int(1)
        self.num_flags = flag_int
        # For now we will use the defaults lined up in each config -> There
        # will be 3 for each
        flag_setup = int(1)
        # now read in the setup from the config parser
        configParser = ConfigParser.RawConfigParser()
        configFilePath = r"Boards/" + self.board.boardname + "/flag_setup_config.cfg"
        configParser.read(configFilePath)

        section = 'Default' + str(flag_int)
        # setup board to be used for testing
        # flag_dict={}
        for i in range(1, self.num_flags + 1):
            flagx = configParser.get(section, 'Flag' + str(i) + 'x')
            flagy = configParser.get(section, 'Flag' + str(i) + 'y')
            # flag_dict[i]=(flagx,flagy)
            flagx = int(flagx)
            flagy = int(flagy)

            self.board.board_dict[(flagx, flagy)].flag = True
            self.board.board_dict[(flagx, flagy)].flag_num = i

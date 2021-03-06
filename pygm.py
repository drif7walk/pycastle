#!/usr/bin/env python

import pygame
import time
import random
import math

from GameObjects import *

gamestate = 0	# 0 Main menu
	  	# 1 Game
		# 2 Choose race

playerrace = 0  # 0 Knights
		# 1 Zombies
		# 2 Robots

def setGameState(state):
	global gamestate
	gamestate = state

def getGameState():
	global gamestate
	return gamestate

def LoadImage(filename):
	spr = pygame.image.load(filename)
	spr.set_colorkey(0xFF00FF)
        return spr

class Menu:
	def __init__(self, options):
		self.options = options
		self.font = pygame.font.SysFont(None, 24)

		self.prevmouse1 = 0
		self.prevmouse2 = 0
		self.prevmouse3 = 0

	def draw(self, targetsurface):
		i = 0
		basex = 10
		basey = 10

		self.currentMouse = pygame.mouse.get_pressed()
		
		# Get mouse button state
		mouse1, mouse2, mouse3 = tuple(self.currentMouse)
		mousex, mousey = pygame.mouse.get_pos()

		for item in self.options:
			textcol = (255, 255, 255)

			text = self.font.render(item, 1,(255,255,255))

			textw = text.get_width()
			texth = text.get_height()
			
			
			if (mousex > basex and mousex < basex + textw and
				mousey > basey + i * texth and mousey < basey + i * texth + texth):
				textcol = (150, 150, 150)

				if (self.prevmouse1 == True and mouse1 == False): # Check mousepress on menu item
					return i;
					
			
			text = self.font.render(item, 1, textcol)	

    			targetsurface.blit(text,(basex, basey + i * texth))
			i += 1

		self.prevmouse1, self.prevmouse2, self.prevmouse3 = mouse1, mouse2, mouse3

def main():

	### Initialization

	pygame.init() # Prepare module

	# Initialize font
	pygame.font.init()
	font = pygame.font.SysFont(None, 14)

	wWidth = 640 #Screen width
	wHeight = 480 #Screen height

	# Set screen with specified dimensions
	scrsurf = pygame.display.set_mode((wWidth, wHeight))

	# Load sprites
	sprKing = LoadImage("Sprites/king.png")
	sprGrass = LoadImage("Sprites/grass.png")
	sprCastle = LoadImage("Sprites/castle.png")
	sprTree = LoadImage("Sprites/tree.png")
	sprCursor = LoadImage("Sprites/finger.png")
	sprVillager = LoadImage("Sprites/villager.png")
	sprMine = LoadImage("Sprites/mine.png")
	sprWindmill = LoadImage("Sprites/windmill.png")
	sprMiner = LoadImage("Sprites/miner.png")
	# End load sprites

	# Load icon set
	icoCastle = LoadImage("Iconset/castle.png")
	# End load icon set

	# List of buildings the player is allowed to build
	buildList = []
	buildList.append(icoCastle);

	# Create main menu
	mainmenu = Menu(["START NEW GAME"])
	racemenu = Menu(["KNIGHTS","ZOMBIES","ROBOTS"])
	
	# Create cursor
	cursor = Cursor(sprCursor)

	# Set color keys for sprites
	spritelist = []
	resourcemines = []

	dude = King(sprKing, (100, 10))
	spritelist.append(dude)

	

	# Spawn resource mine
	mine = ResourceMine(sprMine, (340, 250), "mine", 20)
	resourcemines.append(mine)
	spritelist.append(mine)

	# Spawn resource mine windmill
	mill = ResourceMine(sprWindmill, (100, 120), "windmill", 20)
	resourcemines.append(mill)
	spritelist.append(mill)

	# Generate a bunch of trees
	for i in range(0, random.randint(50, 100)):
		t = GameObject(sprTree, (random.randint(0, wWidth),random.randint(0, wHeight)))
		spritelist.append(t)

	# Make house
	house = Base(sprCastle, (300,150))
	spritelist.append(house)

	# Spawn villagers

		# Farmers
	for i in range(0, 5):
		vlgr = Villager(sprVillager, (200 + random.uniform(-100, 100),150 + random.uniform(-100, 100)), "knight")
		vlgr.setGoal(mill)
		vlgr.setBase(house)
		spritelist.append(vlgr)
		
		# Miners
	for i in range(0, 5):
		vlgr = Villager(sprMiner, (200 + random.uniform(-100, 100),150 + random.uniform(-100, 100)), "knight")
		vlgr.setGoal(mine)
		vlgr.setBase(house)
		spritelist.append(vlgr)

	# Initialize clock
	gameclock = pygame.time.Clock()

	### End initialization

	while True:

		# Poll pygame events
		ev = pygame.event.poll()

		# Handle events
		if ev.type == pygame.QUIT:
			break
		# Key up
		if ev.type == pygame.KEYUP:
			# esc key pressed
			if ev.key == pygame.K_ESCAPE:
				break
		
		# GAME STATE HANDLING UPDATE
		if gamestate == 0: # Update main 
			pass # Do cool main menu stuff here
		elif gamestate == 1: # Update game loop
			for sprt in spritelist: # Update sprite behaviors
				sprt.update()
		
		# GAME STATE HANDLING DRAW
		if gamestate == 0:
			menuchoice = mainmenu.draw(scrsurf)
			if menuchoice == 0:
				setGameState(2)
		elif gamestate == 1:
			# Draw grass background
			for y in range(0, 10):
				for x in range(0, 10):
					scrsurf.blit(sprGrass,(x*64, y*64))

			# Iterate through spritelist and call draw
			for sprt in spritelist:
				sprt.draw(scrsurf)

			# HUD
			text = font.render(str(house.grain), 1,(255,255,255))
    			scrsurf.blit(text,(1, 1))

			# Draw available buildings
			for sprt in buildList:
				scrsurf.blit(sprt, (0, 0))
		elif gamestate == 2:
			menuchoice = racemenu.draw(scrsurf)
			if menuchoice > 0:
				playerrace = menuchoice
				setGameState(1)


		# Draw cursor
		cursor.draw(scrsurf)

		# Flip display to draw it.
		pygame.display.flip()

		# Keep framerate at 120fps
		gameclock.tick(120)

	pygame.quit()
main()

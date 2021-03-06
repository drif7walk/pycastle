#!/usr/bin/env python

import pygame
import time
import random
import math

# Template
class GameObject:
	def __init__(self, img, pos):
		self.image = img
		self.position = pos

		# Nation color that the object belongs to.
		self.nation = { 255, 255, 255 } 

	def update(self):
		return

	def getHeight(self):
		return self.image.get_height()
	def getWidth(self):
		return self.image.get_width()

	def draw(self, targetsurface):
		targetsurface.blit(self.image, self.position)

class GameObject:
	def __init__(self, img, pos):
		self.image = img
		self.position = pos
	
	def update(self):
		return

	def draw(self, targetsurface):
		targetsurface.blit(self.image, self.position)

class Barracks(GameObject):
	def __init__(self, img, pos, nation):
		GameObject.__init__(self)
class Base:
	def __init__(self, img, pos):
		self.image = img
		self.position = pos
	
		self.grain = 0
	def update(self):
		return

	def draw(self, targetsurface):
		targetsurface.blit(self.image, self.position)

class ResourceMine:
	def __init__(self, img, pos, restype, amnt):
		self.image = img
		self.position = pos
		self.type = restype
		self.amount = amnt
	
	def update(self):
		return

	def draw(self, targetsurface):
		targetsurface.blit(self.image, self.position)

class King:
	def __init__(self, img, pos):
		self.image = img
		self.position = pos
	
	def update(self):
		return

	def draw(self, targetsurface):
		targetsurface.blit(self.image, self.position)

# ===
# VILLAGER
# ===
class Villager:
	def __init__(self, img, pos, race):
		self.race = race 
			# "knight"
			# "robot"
			# "zombie"

		self.image = img
		self.position = pos
		self.posadd = (0, 0)
		self.goal = False
		self.selected = False	
		self.prevmouse1, self.prevmouse2, self.prevmouse3 = 0, 0, 0
		self.health = 1	

		# Internal
		self.animate = True
		self.animcounter = 0
		self.carryweight = 0

		self.walkspeed = 0.31
		
		self.state = 1

		self.framesize = (self.image.get_width() / 3, self.image.get_height() / 6)
	def setGoal(self, g):
		self.goal = g
	def setBase(self, base):
		self.base = base

	def update(self):
		self.currentMouse = pygame.mouse.get_pressed()
		
		# Get mouse button state
		mouse1, mouse2, mouse3 = tuple(self.currentMouse)
	
		x, y = tuple(self.position)
		xadd, yadd = tuple(self.posadd)

		x = x + xadd
		y = y + yadd
		
		if (x <= 0):
			x = -x
		if (y <= 0):
			y = -y

		self.position = (x, y)

		# Frame size
		framew, frameh = self.framesize

		# If left mouse release
		if mouse1 == 0 and self.prevmouse1 == 1:
			(mx, my) = pygame.mouse.get_pos()
			# If cursor inside sprite
			if (mx > x and mx < x + framew and
			    my > y and my < y + frameh):
				self.selected = True
			else:
				self.selected = False

		# If right mouse release
		if mouse3 == 0 and self.prevmouse3 == 1:
			(mx, my) = pygame.mouse.get_pos()
			# If cursor inside sprite
			if (mx > x and mx < x + framew and
			    my > y and my < y + frameh):
				self.health -= 0.25


		# BEHAVIORS
			# Walking around
		if self.state == 0:	
			if (random.randint(0, 100) < 10):
				self.posadd = (random.uniform(-0.5,0.5), random.uniform(-0.5,0.5))
			# Going to goal
		elif self.state == 1:
			(selfx, selfy) = self.position
			(goalx, goaly) = self.goal.position
			dx = selfx - goalx
			dy = selfy - goaly
			dist = math.sqrt( dx*dx + dy*dy )
			
			addx = 0
			addy = 0
			if dist > 20:
				if dx > 0:
					addx -= self.walkspeed
				elif dx < 0:
					addx += self.walkspeed

				if dy > 0:
					addy -= self.walkspeed
				elif dy < 0:
					addy += self.walkspeed
			elif dist <= 20:
				self.state = 4

			self.posadd = (addx, addy)

			# Going to base
		elif self.state == 2:
			(selfx, selfy) = self.position
			(goalx, goaly) = self.base.position
			dx = selfx - goalx
			dy = selfy - goaly
			dist = math.sqrt( dx*dx + dy*dy )
			
			addx = 0
			addy = 0
			if dist > 20:
				if dx > 0:
					addx -= self.walkspeed
				elif dx < 0:
					addx += self.walkspeed

				if dy > 0:
					addy -= self.walkspeed
				elif dy < 0:
					addy += self.walkspeed
			elif dist <= 20:
				self.carryweight -= 0.05
				self.base.grain += 5
				# Check if has picked up maximum weight
				if self.carryweight <= 0:
					self.state = 1

			self.posadd = (addx, addy)
			# Dead
		elif self.state == 3:
			self.posadd = (0, 0)
			self.carryweight = 0

			# Harvesting
		elif self.state == 4:
			self.carryweight += 0.005
			# Check if has picked up maximum weight
			if self.carryweight >= 1:
				self.state = 2
		# Check health
		if self.health < 0:
			self.health = 0
		if self.health == 0:
			self.state = 3

		self.prevmouse1, self.prevmouse2, self.prevmouse3 = mouse1, mouse2, mouse3

	def draw(self, targetsurface):

		# Calculate spritesheet position
		framewidth, frameheight = self.framesize
		x = 0

		# Set sprite according to state
		if not self.state == 3:
			x = framewidth + (math.floor(self.animcounter) % 2) * framewidth

			# Determine direction
			(xadd, yadd) = self.posadd

			y = 0
			# If moving to the right
			if xadd > 0:
				y = 0
			# If not moving on x axis
			elif xadd == 0:
				y = frameheight * 2
			# If moving to the left
			elif xadd < 0:
				y = frameheight * 1
		# Check if dead
		elif self.state == 3:
			y = frameheight * 4 
		# Check if harvesting
		elif self.state == 4:
			y = frameheight * 6

		frame = (x, y, framewidth, frameheight)

		if self.animate:
			self.animcounter = self.animcounter + 0.05

		targetsurface.blit(self.image, self.position, frame)

		barpad = 1
		# Draw health bar if selected
		if self.selected:
			(x, y) = self.position
			barw = 15
			# XXX Draw health bar background 
			pygame.draw.rect(targetsurface, 0x000000, (x, y - 7, barw, 5))
			# XXX Draw health bar 
			pygame.draw.rect(targetsurface, 0xFF0000, (x, barpad + y - 7, barw * self.health - barpad, 5 - barpad))

		# If carrying something draw weight
		if self.carryweight > 0:
			(x, y) = self.position
			barw = 15
			# XXX Draw carry bar background 
			pygame.draw.rect(targetsurface, 0x000000, (x, y - 15, barw, 5))
			# XXX Draw carry bar 
			pygame.draw.rect(targetsurface, 0x00FF00, (x, barpad + y - 15, barw * self.carryweight, 5 - barpad))
		

class Cursor:
	def __init__(self, img):
		self.image = img
		pygame.mouse.set_visible(False)
		self.mode = 0; # 0 - CUrsor
		

        def draw(self, targetsurface):
		targetsurface.blit(self.image, pygame.mouse.get_pos())

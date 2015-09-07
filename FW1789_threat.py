#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys, os, random, time, math

import pygame
from pygame.locals import *

pygame.init()

#minileter = pygame.font.Font(None,48)
minileter = pygame.font.Font("freesansbold.ttf",48)

class threat(pygame.sprite.Sprite):
	def __init__(self, image, speed, life):
		pygame.sprite.Sprite.__init__(self)
		self.time = speed #30
		self.life = life #200
		
		self.image = pygame.image.load("Images/%s" %image)
		#tostring(Surface, format, flipped=False) -> string
		self.imageOri = pygame.image.tostring(self.image, "RGBA_PREMULT")
		#fromstring(string, size, format, flipped=False) -> Surface
		#self.image = pygame.image.fromstring(self.imageOri, self.rect, "RGBA_PREMULT")
		
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(30,760) #random initial position
		self.rect.y = random.randrange(30,540) #random initial position
		self.newrect = self.image.get_rect()
		self.newrect.x = random.randrange(30,760) #random initial position
		self.newrect.y = random.randrange(30,540) #random initial position
		self.movx = (self.newrect.x - self.rect.x)/self.time
		self.movy = (self.newrect.y - self.rect.y)/self.time
		self.counter = int(self.time)
		
		self.shooted(0) #only to blit the life
		
	def move(self):
		"""move jump from point to new position point"""
		self.counter += 1
		if self.counter >= self.time:
			self.rect.x = random.randrange(30,760)
			self.rect.y = random.randrange(30,540)
			self.counter = 0
			
		fenetre.blit(self.image,self.rect)
		#fenetre.blit(self.image, self.rect)
		#instead: threat.draw(fenetre) in main loop

	def update(self): # used for (sprite.Group).update
		"""move linear to new position"""
		self.counter += 1
		if self.counter >= self.time:
			self.newrect.x = random.randrange(30,760)
			self.newrect.y = random.randrange(30,540)
			self.movx = (self.newrect.x - self.rect.x)/self.time
			self.movy = (self.newrect.y - self.rect.y)/self.time
			while (abs(self.movx) < 2) and (abs(self.movy) < 2): # ensure a minimal movement
				self.newrect.x = random.randrange(30,760)
				self.newrect.y = random.randrange(30,540)
				self.movx = (self.newrect.x - self.rect.x)/self.time
				self.movy = (self.newrect.y - self.rect.y)/self.time
			self.counter = 0
		self.rect.x += self.movx
		self.rect.y += self.movy

		#fenetre.blit(self.image, self.rect)
		#instead: threat.draw(fenetre) in main loop
		
	def shooted(self, malus):
		self.life -= malus
		if self.life < 0:
			self.life = 0

		self.image = pygame.image.fromstring(self.imageOri, (self.rect[2], self.rect[3]), "RGBA")
		# life remain
		if self.life > 1:
			#rebuilt completly the new png image with new life
			#self.image = pygame.image.fromstring(self.imageOri, (self.rect[2], self.rect[3]), "RGBA")

			self.textLife = minileter.render(str(self.life), 1, (255,0,0)) #red
			self.textLifePos = self.textLife.get_rect()
			self.textLifePos[0] = (self.rect[2]-self.textLifePos[2])/2
			self.textLifePos[1] = (self.rect[3]-self.textLifePos[3])/2
			#for contrast
			self.textLife2 = minileter.render(str(self.life), 1, (0,0,0)) #black
			self.textLife2Pos = self.textLife2.get_rect()
			self.textLife2Pos[0] = (self.rect[2]-self.textLife2Pos[2])/2 + 3
			self.textLife2Pos[1] = (self.rect[3]-self.textLife2Pos[3])/2 + 3

			self.image.blit(self.textLife2, (self.textLife2Pos[0], self.textLife2Pos[1])) # 1st black
			self.image.blit(self.textLife, (self.textLifePos[0], self.textLifePos[1])) # then red

	def getlife(self):
		return self.life


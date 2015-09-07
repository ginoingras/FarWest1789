#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys, os, random, time, math

import pygame
from pygame.locals import *

pygame.init()

class caravan(pygame.sprite.Sprite):
	def __init__(self, image, speed):
		pygame.sprite.Sprite.__init__(self)
		self.time = speed #90
		self.life = 10
		self.image = pygame.image.load("Images/%s" %image)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(30,760) #random initial position
		self.rect.y = 500 # initial position
		self.newrect = self.image.get_rect()
		self.newrect.x = random.randrange(30,760) #random final position
		self.newrect.y = 500 # final position
		self.movx = (self.newrect.x - self.rect.x)/self.time
		#self.movy = (self.newrect.y - self.rect.y)/self.time
		self.movy = 0
		self.counter = int(self.time)

	def update(self):
		"""move horizontal to new position"""
		self.counter += 1
		if self.counter >= self.time:
			self.newrect.x = random.randrange(30,760)
			self.movx = (self.newrect.x - self.rect.x)/self.time
			while (abs(self.movx) < 2): # ensure a minimal movement
				self.newrect.x = random.randrange(30,760)
				self.movx = (self.newrect.x - self.rect.x)/self.time
			self.counter = 0
		self.rect.x += self.movx
		self.rect.y += self.movy
		
		#fenetre.blit(self.image, self.rect)
		#instead: caravan.draw(fenetre) in main loop


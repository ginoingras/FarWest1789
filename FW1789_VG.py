#!/usr/bin/env python
# -*- coding: utf8 -*-

#Far West 1789 Variables Globales

import os, sys, time, random #, platform, threading, math
import pygame
from pygame.locals import *

FW1789_version = "0.0.1"

pdb_debug = False
#pdb_debug = True

#Colors RGB
Aqua=(0, 255, 255)
Black=(0, 0, 0)
Blue=(0, 0, 255)
#DeepBlue=(0, 0, 210)
DeepBlue=(0, 0, 160)
Fuchsia=(255, 0, 255)
Gray=(128, 128, 128)
Green=(0, 255, 0)
#DeepGreen=(0, 164, 0)
DeepGreen=(0, 140, 0)
Lime=(0, 255, 0)
Brown=(128, 0, 0)
NavyBlue=(0, 0, 128)
Olive=(128, 128, 0)
Purple=(128, 0, 128)
Red=(255, 0, 0)
#DeepRed=(200, 0, 0)
DeepRed=(160, 0, 0)
Silver=(192, 192, 192)
Teal=(0, 128, 128)
White=(255, 255, 255)
Yellow=(255, 255, 0)
#DeepYellow=(210, 210, 0)
DeepYellow=(160, 160, 0)

last5sec = 5

ParPlayerName = "Gino"
ParFPS = 40
ParGrabMouse = False
ParLife = 100
ParBulletQty = 30
ParGrenadeQty = 10
ParGrenadeSpeed = 30

ParMusicYN = True
ParMusicVol = 0.4

#################################################
def load_cfg(name="FW1789.cfg"):
	"""Load file FW1789.cfg and return config paramters
	return (ParPlayerName, ParFPS, ParScreenSize, ParLockMouse, ParShowMouse, ParLives, ParBulletQty, ParGrenadeQty, ParGrenadeSpeed, 
	ParMusicYN, ParMusicVol)"""

	#DEFAULT VALUES IF NOT FOUND IN CONFIG FILE
	ParPlayerName = "Gino"
	ParFPS = 60 #60	
	ParGrabMouse =False
	ParLife = 100
	ParBulletQty = 30
	ParGrenadeQty = 10
	
	ParGrenadeSpeed = 15
	ParMusicYN = True
	ParMusicVol = 0.9
	ParIPServer = "127.0.0.1"
	ParIPServerPort = 50010
	ParIPaddressLocal = "127.0.0.1"
	
	ParKeybUnicode = True
	ParKeybi18n = "fr"

	ParBallSpeedSlow = 4 # is level parameter
	ParBallSpeedFast = 6 # is level parameter
	ParDwngrdBrick = True # is level parameter
	ParScreenSize = (640, 640)# is level parameter
		
	try:
		#open config file extension ".cfg" in correct directory.
		fullname = os.path.join('', name)
		configstext = []
		fichier = open(fullname,'r')
		# pass on each lines with command for
		for ligne in fichier.readlines() :
			# split line in words - split remove spaces and carriage return
			donnees = ligne.split()
			# finally add to config array 
			configstext.extend(donnees)
		# end of loop for, close config file
		fichier.close()
		
		#print (configstext)
		#WARNING: somes parameters in v10x only, have to check version header file!
		for idx, line in enumerate(configstext):
			#print idx
			if line =="[ParPlayerName]":
				ParPlayerName = (configstext[idx+1])
				print ("ParPlayerName: %s" %(ParPlayerName))
			if line =="[ParFPS]":
				ParFPS = eval(configstext[idx+1])
				print ("ParFPS: %s" %(ParFPS))
			if line =="[ParScreenSize]":
				ParScreen = eval(configstext[idx+1])
				ParScreenSize = (ParScreen, ParScreen)
				print ("ParScreenSize: %s x %s" %(ParScreen, ParScreen))
			if line =="[ParGrabMouse]":
				ParGrabMouse = eval(configstext[idx+1])
				print ("ParGrabMouse: %s" %(ParGrabMouse))
			if line =="[ParLockMouse]":
				ParLockMouse = eval(configstext[idx+1])
				print ("ParLockMouse: %s" %(ParLockMouse))
			if line =="[ParBulletQty]":
				ParBulletQty = eval(configstext[idx+1])
				print ("ParBulletQty: %s" %(ParBulletQty))
			if line =="[ParGrenadeQty]":
				ParGrenadeQty = eval(configstext[idx+1])
				print ("ParGrenadeQty: %s" %(ParGrenadeQty))
			if line =="[ParGrenadeSpeed]":
				ParGrenadeSpeed = eval(configstext[idx+1])
				print ("ParGrenadeSpeed: %s" %(ParGrenadeSpeed))
			if line =="[ParLife]":
				ParLife = eval(configstext[idx+1])
				print ("ParLife: %s" %(ParLife))
			if line =="[ParMusicYN]":
				ParMusicYN = eval(configstext[idx+1])
				print ("ParMusicYN: %s" %(ParMusicYN))
			if line =="[ParMusicVol]":
				ParMusicVol = eval(configstext[idx+1])
				print ("ParMusicVol: %s" %(ParMusicVol))
			if line =="[ParIPServer]":
				ParIPServer = (configstext[idx+1])
				print ("ParIPServer: %s" %(ParIPServer))
			if line =="[ParIPServerPort]":
				ParIPServerPort = eval(configstext[idx+1])
				print ("ParIPServerPort: %s" %(ParIPServerPort))
			if line =="[ParIPaddressLocal]":
				ParIPaddressLocal =(configstext[idx+1])
				print ("ParIPaddressLocal: %s" %(ParIPaddressLocal))
			if line =="[ParKeybUnicode]":
				ParKeybUnicode = eval(configstext[idx+1])
				print ("ParKeybUnicode: %s" %(ParKeybUnicode))
			if line =="[ParKeybi18n]":
				ParKeybi18n = (configstext[idx+1])
				print ("ParKeybi18n: %s" %(ParKeybi18n))
				
	except:
		print ("Warning: INVALIDE PARAMETERS IN %s !!!" %(name))

	return (ParPlayerName, ParFPS, ParScreenSize, ParGrabMouse, ParLife, ParBulletQty, ParGrenadeQty, ParGrenadeSpeed, \
	ParMusicYN, ParMusicVol, ParIPServer, ParIPServerPort, ParIPaddressLocal, ParKeybUnicode, ParKeybi18n) 

#################################################
def save_cfg(name="FW1789.cfg"):
	fullname = os.path.join("", name)
	try:
		fichier = open(fullname, "w")
		
		fichier.write("# FW1789.cfg version: %s\n" %(VG.FW1789_version))
		fichier.write("# only the 1st line just downside paramater is checked\n")
		fichier.write("[ParPlayerName]\n")
		fichier.write(ParPlayerName+"\n")

		fichier.write("[ParFPS]\n")
		fichier.write(str(ParFPS)+"\n")

		fichier.write("[ParGrabMouse]\n")
		fichier.write(str(ParGrabMouse)+"\n")
		fichier.write("True | False\n")

		fichier.write("[ParLife]\n")
		fichier.write(str(ParLife)+"\n")

		fichier.write("[ParBulletQty]\n")
		fichier.write(str(ParBulletQty)+"\n")

		fichier.write("[ParGrenadeQty]\n")
		fichier.write(str(ParGrenadeQty)+"\n")
		fichier.write("[ParGrenadeSpeed]\n")
		fichier.write(str(ParGrenadeSpeed)+"\n")

		fichier.write("[ParMusicYN]\n")
		fichier.write(str(ParMusicYN)+"\n")
		fichier.write("True | False\n")

		fichier.write("[ParMusicVol]\n")
		fichier.write(str(ParMusicVol)+"\n")

		fichier.write("[ParIPServer]\n")
		fichier.write(ParIPServer+"\n")

		fichier.write("[ParIPServerPort]\n")
		fichier.write(str(ParIPServerPort)+"\n")

		fichier.write("[ParIPaddressLocal]\n")
		fichier.write(IPaddressLocal+"\n")

		fichier.write("[ParKeybUnicode]\n")
		fichier.write(str(ParKeybUnicode)+"\n")
		fichier.write("True | False\n")
		
		fichier.write("[ParKeybi18n]\n")
		fichier.write((ParKeybi18n)+"\n")
		fichier.write("fr | us | gb - see pybreak360_kbd\n")


		# NOT USED
		fichier.write("# not need, updated by level config\n")
		fichier.write("[ParDwngrdBrick]\n")
		fichier.write(str(ParDwngrdBrick)+"\n")

		fichier.write("[ParBallSpeedSlow]\n")
		fichier.write(str(ParBallSpeedSlow)+"\n")

		fichier.write("[ParBallSpeedFast]\n")
		fichier.write(str(ParBallSpeedFast)+"\n")

		fichier.write("[ParScreenSize]\n")
		fichier.write(str(ParScreenSize[0])+"\n")
		fichier.write("480 640 800\n")

		fichier.close()

		print ("%s saved" %(name))
	except pygame.error, message:
		print ("Warning: unable to save %s" %(name))

ParPlayerName, ParFPS, ParScreenSize, ParGrabMouse, ParLife, ParBulletQty, ParGrenadeQty, ParGrenadeSpeed, \
ParMusicYN, ParMusicVol, ParIPServer, ParIPServerPort, ParIPaddressLocal, ParKeybUnicode, ParKeybi18n = load_cfg("FW1789.cfg")

a="""
players = [["free", "player1", 0, 0, ParBulletQty, ParLives], ["free", "player2", "free", 0, ParBulletQty, ParLives], \
["free", "player3", "free", 0, ParBulletQty, ParLives], ["free", "player4", "free", 0, ParBulletQty, ParLives]]

# client know if player exist if angle != "free"
#[0 objOriBatImage, 1 objBatImageAngle, 2 objOriBatPos(posx, posy), 3 center(posx, posy), 4 objBatAnglePos(posx, posy), 5 animation]
playersbat = [[g_bat_yellow2, "free", "free", "free", "free", 0], [g_bat_green2, "free", "free", "free", "free", 0], \
[g_bat_blue2, "free", "free", "free", "free", 0], [g_bat_red2, "free", "free", "free", "free", 0]]

playerno = 0 # actual number of player in local game

balls = [["free", (0,0,0,0), 0], ["free", (0,0,0,0), 0], ["free", (0,0,0,0), 0], ["free", (0,0,0,0), 0]]
bullets = []
bricks = []

#background, toto = load_backgnd(levelBackGnd)
background = pygame.Surface((480,480))
background = background.convert()
background.fill((255, 255, 255))

BatDim = [0, 0, 0, 0]
BatDimTime = [0, 0, 0, 0]
InvertTime = [0, 0, 0, 0]

#allowed for all players
WallTime = 0

rayon = 240 #default 480 screen size
fenetre_center = (240, 240) #default 480 screen size
fenetre_size = ParScreenSize #default 480
fenetre = pygame.display.set_mode(fenetre_size)

nb_levels = 1
levels = []
levelNumber = 0
#nb_levels, levels = load_levels(ParLevelPack)

#global levelName, levelBackGnd, levelClient
levelName = "Unknow"
levelBackGnd = "Unknow"
levelClient =  [(0,6,4,3,2), (0,0,6,0,0), (1,2,3,0,0), (7,0,0,2,0), (0,0,3,0,0), (2,3,4,5,6)]
a="""


#global PenalityDelays   # when lose ball
PenalityDelayP1 = time.time() + 2
PenalityDelayP2 = time.time() + 2
PenalityDelayP3 = time.time() + 2
PenalityDelayP4 = time.time() + 2
PenalityDelays = [PenalityDelayP1, PenalityDelayP2, PenalityDelayP3, PenalityDelayP4]

anouncetexte = ["Far West 1789 V%s" %(FW1789_version)]
anouncetime = 4
anouncetimeactu = 0
anouncealpha = 180 #128
anouncealphaactu = 1

howplayers = 1

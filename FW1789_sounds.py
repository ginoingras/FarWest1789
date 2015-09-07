#!/usr/bin/env python
# -*- coding: utf8 -*-

import os, pygame

#pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
pygame.mixer.pre_init()
pygame.init()
pygame.mixer.set_num_channels(4)
pygame.mixer.init()

#################################################
def sound_play(song, volume=50):
	"""play a sound Freq, Vol"""

	sound = False
	#if VG.ParMusicYN:
	if True:
		#path = os.path.join("sounds", song + ".ogg")
		#path = os.path.join("Data", "Sounds", song)
		path = os.path.join("Sounds", song)
		sound = pygame.mixer.Sound(path)  #load sound
		#sound.play()
		#sound.set_volume(VG.ParMusicVol*100)
		sound.set_volume(volume)

	return sound
	#for sound effects: 
	#Sound.play(loops=0, maxtime=0, fade_ms=0): return Channel
	#jump.play() # play the jump sound effect once

#Loading sounds

S_Applause = pygame.mixer.Sound("Sounds/Applause.ogg")
S_Shoot = pygame.mixer.Sound("Sounds/shoot.ogg")
S_Rire = pygame.mixer.Sound("Sounds/rire2.ogg")
S_Bomb = pygame.mixer.Sound("Sounds/bomb.ogg")
S_Bomb1 = pygame.mixer.Sound("Sounds/bomb1.ogg")
S_Argh = pygame.mixer.Sound("Sounds/argh.ogg")
S_Yeah = pygame.mixer.Sound("Sounds/yeah.ogg")
S_Menu = pygame.mixer.Sound("Sounds/menu.ogg")

S_Beep1 = pygame.mixer.Sound("Sounds/beep1.ogg")
S_Beep5 = pygame.mixer.Sound("Sounds/beep5.ogg")
S_Beep9 = pygame.mixer.Sound("Sounds/beep9.ogg")

S_glassbreak = sound_play("glassbreak.ogg")

#pygame.mixer.music.set_volume(VG.ParMusicVol)

#pygame.mixer.music.load("Sounds/%s.ogg" %(StagesMusic[StageNumber]))
#pygame.mixer.music.play()

#fondomusic = pygame.mixer.Sound("Sounds/%s.ogg" %(StagesMusic[StageNumber]))
#fondomusic.play()


#!usr/bin/python
# -*- coding: utf-8 -*- 

# Far West 1798, a shooter multi player network game
# (C) Jean Ingrasciotta 2015 ginoingras@gmail.com
# licencied under GPLV3
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#    see COPYING file.
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

# How to contribute:
# see README.TXT
# check "FIXME:" in code
# check "WARNING:" in code
# check "TODO:" in code
# github: git clone git://git.code.sf.net/p/pybreak360/code pybreak360-code
#
# report bug, send your levelpack at adresse below
# ginoingras@gmail.com 
#
#FIXME:
# 1 sec bip when less 5 sec remain don't work always
#
#TODO:
# add fullscreen
# add freeze ice malus 2 sec.
# add little mire malus 5 sec.
# add big mire bonus 5 sec.
# add 4 mulitplayers network

try:
	import pygame
	from pygame.locals import *
	import sys, os, random, time, math

	#from json import load
	import json
	
	#local imports
	import FW1789_VG as VG
	from FW1789_stages import *
	from FW1789_sounds import *
	from FW1789_caravan import caravan
	from FW1789_threat import threat


except ImportError, message:
	print ("ERROR IMPORTING MODULES: %s" % message)
	raise SystemExit, "ERROR IMPORTING MODULES: %s" % message
	sys.exit(1)

global hiscore
hiscore = 20 #time to stage die
try:
	with open("hiscore.json", "rt") as infile:
		hiscore = json.load(infile)
except:
	print "WARNING: unable to load HiScore"
	
pygame.init()

#fenetre = pygame.display.set_mode((860,640))
fenetre = pygame.display.set_mode((800,600))
#fenetre = pygame.display.set_mode((1024,600))
pygame.display.set_caption("FW1789 - v%s" %(VG.FW1789_version))
icone = pygame.image.load("Images/icone2b.png").convert_alpha()
pygame.display.set_icon(icone)
pygame.mouse.set_visible(False)

#lettre = pygame.font.Font(None,30)
lettre = pygame.font.Font("freesansbold.ttf",30)

FWlettre = pygame.font.Font("fonts_western/RioGrande2.ttf",28)
#FWlettre = pygame.font.Font("fonts_western/BURNSTOW.TTF",40)

explode1 = pygame.image.load("Images/explosion1.png").convert_alpha()       
explode2 = pygame.image.load("Images/explosion2.png").convert_alpha()       
explode3 = pygame.image.load("Images/explosion3.png").convert_alpha()       
explode4 = pygame.image.load("Images/explosion4.png").convert_alpha()       
explode5 = pygame.image.load("Images/explosion5.png").convert_alpha()       
explode6 = pygame.image.load("Images/explosion6.png").convert_alpha()       

#################################################
class mire(pygame.sprite.Sprite):
	def __init__(self, image, owner):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load("Images/%s" %image)
		self.rect = self.image.get_rect()
		self.rect.x = 800/2
		self.rect.y = 600/2

		self.grenades = VG.ParGrenadeQty #10
		self.bullets = VG.ParBulletQty #30
		self.life = VG.ParLife #100
		self.score = 0

	def move(self):
		mousepos = pygame.mouse.get_pos()
		self.rect.x = mousepos[0] 
		self.rect.y = mousepos[1]
		fenetre.blit(self.image, self.rect)
		
		#fenetre.blit(self.image, self.rect)
		#instead: (spriteGroup)mire.draw(fenetre) in main loop
		
	def shoot(self):
		if self.bullets > 0:
			self.bullets -= 1
			S_Shoot.play()

			yeah = pygame.sprite.spritecollide(self, groupBandits, dokill=False)
			if yeah:
				for bandi in yeah:
					bandi.shooted(10)
					self.score += 10
					if bandi.life > 0:
						S_Rire.play()
					else:
						S_Argh.play()
						groupBandits.remove(bandi)
						
			yeah = pygame.sprite.spritecollide(self, groupBonusGrenades, dokill=True)
			if yeah:
				for idx, tt in enumerate(yeah):
					if yeah[idx].life > 0:
						yeah[idx].shooted(1000)
						self.grenades += 5
						S_Yeah.play()
				
			yeah = pygame.sprite.spritecollide(self, groupBonusBullets, dokill=True)
			if yeah:
				for idx, tt in enumerate(yeah):
					if yeah[idx].life > 0:
						yeah[idx].shooted(1000)
						self.bullets += 10
						S_Yeah.play()
				
			HoNo = pygame.sprite.spritecollide(self, groupFarmers, dokill=False)
			if HoNo:
				self.life -= 10
				S_Argh.play()
				return "Loser"
			else:
				return "Ouf"
			
	def getxy(self):
		return (self.rect.x, self.rect.y)

#################################################
class grenade(pygame.sprite.Sprite):
	def __init__(self, image, owner):
		pygame.sprite.Sprite.__init__(self)
		self.time = 30
		self.image = pygame.image.load("Images/%s" %image)
		self.rect = self.image.get_rect()
		self.imageOri = pygame.image.load("Images/%s" %image)
		self.rectOri = self.imageOri.get_rect()

		self.launched = False
		self.owner = owner # 1,2,3,4 to know who player got this grenade

		self.rect.x = 30 # initial position
		self.rect.y = 550
		self.newrect = self.image.get_rect()
		self.newrect.x = mire1.getxy()[0] # final position
		self.newrect.y = 550
		self.movx = (self.newrect.x - self.rect.x)/self.time
		self.movy = (self.newrect.y - self.rect.y)/self.time
		self.counter = int(self.time)

		if self.newrect.x > self.rect.x:
			self.elipse_fwrw = True
			self.elipse_rayon = int((self.newrect.x - self.rect.x) / 2)
			self.elipse_center = self.rect.x + self.elipse_rayon
			self.angle = 0
		else:
			self.elipse_fwrw = False
			self.elipse_rayon = int((self.rect.x - self.newrect.x) / 2)
			self.elipse_center = self.newrect.x + self.elipse_rayon
			self.angle = math.pi

	def launch(self):
		self.newrect.x = mire1.getxy()[0]
		self.newrect.y = 550
		
		if mire1.getxy()[0] > 400:
			self.rect.x = 760
		else:
			self.rect.x = 0
		self.rect.y = 550

		self.newrect = self.image.get_rect()
		self.newrect.x = mire1.getxy()[0]+25 # final position [mireWidth-grenadeWidth]
		self.newrect.y = 550
		self.movx = (self.newrect.x - self.rect.x)/self.time
		self.movy = (self.newrect.y - self.rect.y)/self.time
		self.counter = 0

		if self.newrect.x > self.rect.x:
			self.elipse_fwrw = True
			self.elipse_rayon = int((self.newrect.x - self.rect.x) / 2)
			self.elipse_center = self.rect.x + self.elipse_rayon
			self.angle = 0
		else:
			self.elipse_fwrw = False
			self.elipse_rayon = int((self.rect.x - self.newrect.x) / 2)
			self.elipse_center = self.newrect.x + self.elipse_rayon
			self.angle = math.pi
			
		self.launched = True
		#print ("update grenade rayon: %s , center: %s" %(self.elipse_rayon, self.elipse_center))
		#print ("grenade launched from %s to %s" %(self.rect.x, self.newrect.x))

	def rot_center(self, image, rect, angle):
		"""rotate an image while keeping its center"""
		self.image = pygame.transform.rotate(image, angle)
		w = math.sqrt(rect.width**2 + rect.height**2)
		self.rect = self.image.get_rect(center=rect.center, size=(w,w))

	def moveElipse(self):
		"""move elipse to new position, use angle from -180 to 0 to 180
		return self.launched"""

		if (self.angle > math.pi) or (self.angle < 0):
			#some more delay to explode
			self.counter += 1
			if (self.counter >= 30):
				fenetre.blit(explode4, (self.rect[0]-30, 500))
			if (self.counter >= 20) and (self.counter < 30):
				fenetre.blit(explode3, (self.rect[0]-30, 500))
			if (self.counter >= 10) and (self.counter < 20):
				fenetre.blit(explode2, (self.rect[0]-30, 500))
			# delay to chech if shoot caravan
			if self.counter < 10:
				fenetre.blit(explode1, (self.rect[0]-30, 500))
			
				yeah = pygame.sprite.spritecollide(self, groupCaravans, dokill=True)
				for idx, cara in enumerate(yeah):
					yeah[idx].life = 0
					mire1.score += 100
					S_Bomb.play() # caravan shooted
					S_Bomb1.stop()
					self.counter = 10 # pass to big explosion animation

				if self.counter == 9:
					S_Bomb1.play() # caravan not shooted
					self.launched = False
			
			if self.counter > 40:
				self.launched = False

		else:
			if self.elipse_fwrw:
				self.angle += VG.ParGrenadeSpeed #0.03
			else:
				self.angle -= VG.ParGrenadeSpeed #0.03
				
			self.rot_center(self.imageOri, self.rectOri, math.degrees(float(self.angle*2)))

			self.movx = math.cos(self.angle)*self.elipse_rayon
			self.movy = math.sin(self.angle)*550
			
			if self.elipse_fwrw:
				self.rect.x = self.elipse_center - self.movx
				self.rect.y = 550 - self.movy
			else:
				self.rect.x = self.elipse_center - self.movx
				self.rect.y = 550 - self.movy

			fenetre.blit(self.image, self.rect)

		return self.launched

	def getxy(self):
		return (self.rect.x, self.rect.y)

	def getangle(self):
		return (self.angle)

	def getfwrw(self):
		return (self.elipse_fwrw)

#################################################
def wait_mouse_click():
	"""wait for  0.5 second, then mouse click, and 0.2 second"""
	time.sleep(0.5) # minimum time
	for event in pygame.event.get(): #purge pygame event queue
		pass
	wait_mouse_click = True
	while wait_mouse_click:
		for event in pygame.event.get():
			#FIXME: pass in var glob to effectivly exit game
			if event.type == QUIT:
				is_running = False
				wait_mouse_click = False
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					is_running = False
					wait_mouse_click = False


			if event.type == MOUSEBUTTONDOWN:
				wait_mouse_click = False
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					wait_mouse_click = False
	time.sleep(0.2) # minimum time
	
#################################################
def save_hiscore(score):
	"""Save HiScore if new record"""
	global hiscore
	if hiscore < score:
		hiscore = score
		try:
			with open('hiscore.json', 'w') as outfile:
				json.dump(hiscore, outfile)
		except:
			print "WARNING: unable to write HiScore"

#################################################
def blit_scores():
	"""finally blit scores for all players"""
	fenetre.blit(FWlettre.render("Remaining Time: %s.%s " %(timeLeft/10, timeLeft%10),True,(255,0,0)),(5,5))
	fenetre.blit(FWlettre.render("HiScore: %s " %(hiscore),True,(255,0,0)),(5,30))
	fenetre.blit(FWlettre.render("Stage: %s " %(StageNumber + 1),True,(255,0,0)),(5,55))
	fenetre.blit(FWlettre.render("Life: "+str(mire1.life),True,(255,0,0)),(600,5))
	fenetre.blit(FWlettre.render("Bullets:  "+str(mire1.bullets),True,(255,0,0)),(600,30))
	fenetre.blit(FWlettre.render("Grenades:  "+str(mire1.grenades),True,(255,0,0)),(600,55))
	fenetre.blit(FWlettre.render("Score:  "+str(mire1.score),True,(255,0,0)),(600,80))

#################################################
def gameOver():
	#time.sleep(1)
	wait_mouse_click()
	#save_hiscore(timeLeft)
	save_hiscore(mire1.score)
	
	# game over, try again
	#mire1.grenades = VG.ParGrenadeQty #10
	#mire1.bullets = VG.ParBulletQty #30
	#mire1.life = VG.ParLife #100
	#mire1.score = 0
	#grenade1.launched = False
	listGrenades = []
	gameTerminate = False
	crono = pygame.time.Clock()
	milli = 0
	VG.last5sec = 5

	StageNumber = 0
	StageTerminate = False
	fondo1, fondo2, fondomusic = loadStageEnv(StageNumber)
	fondomusic.play()
	
#################################################
def loadStageSprites(StageNumber):
	groupBandits = pygame.sprite.Group()
	for idx in range(StagesBandits[StageNumber][0]):
		varRand = random.randrange(0, 3)
		if varRand == 0:
			bandit1 = threat("Dalton-Williamb.png", StagesBandits[StageNumber][1], StagesBandits[StageNumber][2])
		elif varRand == 1:
			bandit1 = threat("bandit2b.png", StagesBandits[StageNumber][1], StagesBandits[StageNumber][2])
		elif varRand >= 2:
			bandit1 = threat("bandit4b.png", StagesBandits[StageNumber][1], StagesBandits[StageNumber][2])
		groupBandits.add(bandit1)

	groupFarmers = pygame.sprite.Group()
	for idx in range(StagesFarmers[StageNumber][0]):
		varRand = random.randrange(0, 2)
		if varRand == 0:
			farmer1 = threat("farmerb.png", StagesFarmers[StageNumber][1], 1) #image, speed, life
		elif varRand >= 1:
			farmer1 = threat("Dalton-Ma-b.png", StagesFarmers[StageNumber][1], 1) #image, speed, life
		groupFarmers.add(farmer1)

	listCaravans = []
	groupCaravans =  pygame.sprite.Group()
	for idx in range(StagesDiligences[StageNumber][0]):
		varRand = random.randrange(0, 4)
		if varRand == 0:
			caravan1 = caravan("caravan4a.png", 90)
		elif varRand == 1:
			caravan1 = caravan("caravan2b.png", 90)
		elif varRand == 2:
			caravan1 = caravan("caravan1c.png", 90)
		elif varRand >= 3:
			caravan1 = caravan("caravan3b.png", StagesDiligences[StageNumber][1]) #image, speed
		
		listCaravans.append(caravan1)
		groupCaravans.add(caravan1)

	# add grenades bonus for diligences to hit
	groupBonusGrenades = pygame.sprite.Group()
	for idx in range(StagesGrenades[StageNumber][0]):
		bonus1 = threat("Grenade-6b.png", StagesGrenades[StageNumber][1], 1) #image, speed, life
		groupBonusGrenades.add(bonus1)

	# add as bullets bonus 
	groupBonusBullets = pygame.sprite.Group()
	for idx in range(StagesBullets[StageNumber][0]):
		#bonus1 = threat("bullets-2b.png", StagesBullets[StageNumber][1], 1) #image, speed, life
		bonus1 = threat("bullets-b.png", StagesBullets[StageNumber][1], 1) #image, speed, life
		groupBonusBullets.add(bonus1)
		
	return groupBandits, groupFarmers, listCaravans, groupCaravans, groupBonusGrenades, groupBonusBullets

#################################################
def loadStageEnv(StageNumber):
	fondo1 = pygame.image.load("background/%s.jpg" %(StagesBckGnd1[StageNumber]))
	fondo2 = pygame.image.load("background/%s.png" %(StagesBckGnd2[StageNumber]))
	if fondo2.get_alpha is None:
		fondo2 = fondo2.convert()
	else:
		fondo2 = fondo2.convert_alpha()

	fondomusic = pygame.mixer.Sound("Sounds/%s.ogg" %(StagesMusic[StageNumber]))
	#pygame.mixer.music.play()
	pygame.mixer.stop()
	return fondo1, fondo2, fondomusic
	
BckGndWin = pygame.image.load("background/festival-far-westa.jpg")
BckGndLoseTime = pygame.image.load("background/western-jail.jpg")
BckGndLoseLife = pygame.image.load("background/pendu-meridien-de-sang.jpg")

pygame.mixer.init()
pygame.mixer.music.set_volume(VG.ParMusicVol)

S_Menu.play()

background = pygame.image.load("background/FarWest1789b.jpg")
fenetre.blit(background,(0,0))
pygame.display.update()
#time.sleep(9)
wait_mouse_click()

mire1 = mire("mire-red.png", 1)
listMire =  pygame.sprite.Group()
listMire.add(mire1)

grenadeBlue = grenade("grenade-blue.png", 1)
grenadeRed = grenade("grenade-red.png", 2)
grenadeGreen = grenade("grenade-green.png", 3)
grenadeYellow = grenade("grenade-yellow.png", 4)
listGrenades = []
groupGrenades =  pygame.sprite.Group()
listGrenades.append(grenadeBlue)
groupGrenades.add(grenadeBlue)

crono = pygame.time.Clock()
milli = 0

StageNumber = 0
StageTerminate = False

groupBandits, groupFarmers, listCaravans, groupCaravans, groupBonusGrenades, groupBonusBullets = loadStageSprites(StageNumber)

fondo1 = pygame.image.load("background/%s.jpg" %(StagesBckGnd1[StageNumber]))
#fondo1.scroll(dx=-860+scroll, dy=0)

fondo2 = pygame.image.load("background/%s.png" %(StagesBckGnd2[StageNumber]))
if fondo2.get_alpha is None:
	fondo2 = fondo2.convert()
else:
	fondo2 = fondo2.convert_alpha()

#pygame.mixer.stop()
fondo1, fondo2, fondomusic = loadStageEnv(StageNumber)
fondomusic.play()

gameTerminate = False

scroll1 = 0
scroll2 = 0

VG.last5sec = 5

if VG.ParGrabMouse:
	pygame.event.set_grab(True) # lock mouse and event inside windows

is_running = True
while is_running:
	
	# ensure game working at 30 FramesPerSeconde, synchro with clients
	#crono.tick(30)
	#crono.tick(VG.ParFPS)
	#print crono.tick() #~20 ticks needed

	milli += crono.tick()
	#milli += 30
	timeLeft = milli/100
	#timeLeft = 200 - timeLeft
	timeLeft = StagesTime[StageNumber] - timeLeft

	# quick !!! beep on last seconds...
	if timeLeft%10 == 0:
		if int(timeLeft) == 40:
			if VG.last5sec == 5:
				S_Beep1.stop()
				S_Beep1.play()
				VG.last5sec = 4
		if int(timeLeft) == 30:
			if VG.last5sec == 4:
				S_Beep1.stop()
				S_Beep1.play()
				VG.last5sec = 3
		if int(timeLeft) == 20:
			if VG.last5sec == 3:
				S_Beep1.stop()
				S_Beep1.play()
				VG.last5sec = 2
		if int(timeLeft) == 10:
			if VG.last5sec == 2:
				S_Beep1.stop()
				S_Beep1.play()
				VG.last5sec = 1

	if timeLeft < 1:
		gameTerminate = True
		
	scroll1 +=1
	if scroll1 >= 800*2:
		scroll1 = 0
	scroll2 +=2
	if scroll2 >= 800*2:
		scroll2 = 0

		#StageNumber +=1
		#fondo1, fondo2, fondomusic = loadStageEnv(StageNumber)
		#fondomusic.play()
	
	for action in pygame.event.get():
                
		if action.type == QUIT:
			is_running = False

		if action.type == KEYDOWN:
			if action.key == K_ESCAPE:
				is_running = False

		if action.type == MOUSEBUTTONDOWN:
			if action.button == 3:
				#print "RightButon"
				if mire1.grenades >0:
					grenadeBlue = grenade("grenade-blue.png", 1)
					listGrenades.append(grenadeBlue)
					#del grenadeBlue
					listGrenades[len(listGrenades)-1].launch()
					#grenadeBlue.launch()
					mire1.grenades -= 1
				
			if action.button == 1:
				#print "LeftButon"
				shot = mire1.shoot()
				if shot == "Loser": #shot where not to hit
					if mire1.life <= 0:
						gameTerminate = True
		
	if not gameTerminate:
		mousepos = pygame.mouse.get_pos() 

		fenetre.blit(fondo1,(-800*2+scroll1, 0))
		# scores should be under all sprites
		blit_scores()
		
		groupCaravans.update()
		groupCaravans.draw(fenetre)
		
		# caravan should be under 1st background
		fenetre.blit(fondo2,(-800*2+scroll2, 600-mousepos[1]))
		
		
		if len(listGrenades) > 0:
			for idx, gren in enumerate(listGrenades):
				if listGrenades[idx].launched:
					#print idx, len(listGrenades)
					listGrenades[idx].moveElipse()
					# grenade should be under 1st background when goes down
					if not listGrenades[idx].getfwrw():
						if (listGrenades[idx].getangle() <= math.pi/2):
							fenetre.blit(fondo2,(-800*2+scroll2, 600-mousepos[1]))
					if listGrenades[idx].getfwrw():
						if (listGrenades[idx].getangle() > math.pi/2):
							fenetre.blit(fondo2,(-800*2+scroll2, 600-mousepos[1]))
					if not listGrenades[idx].launched:
						#print idx, gren
						listGrenades.remove(gren)
				else:
					#FIXME: minor: bypass moveElipse for next iteration idx+1
					listGrenades.remove(gren)
					idx -=1

		#4 type from class threat
		groupBandits.update()
		groupBandits.draw(fenetre)

		groupFarmers.update()
		groupFarmers.draw(fenetre)

		groupBonusGrenades.update()
		groupBonusGrenades.draw(fenetre)

		groupBonusBullets.update()
		groupBonusBullets.draw(fenetre)
		
		mire1.move()
		
		if len(groupBandits) == 0:
			fenetre.blit(BckGndWin,(0,0))
			if StageNumber < 9:
				StageNumber +=1
			blit_scores()
			S_Applause.play()
			
			mire1.score += timeLeft
			#display next stage message
			msg1 = (FWlettre.render("SCORE TIME BONUS: +%s" %(timeLeft), True, (255,0,0)))
			msg2 = (FWlettre.render("NEXT STAGE:", True, (255,0,0)))
			msg3 = (FWlettre.render(StagesMsg[StageNumber], True, (255,0,0)))
			
			msg1pos = msg1.get_rect()
			msg1pos.centerx = fenetre.get_rect().centerx
			msg1pos.centery = fenetre.get_rect().centery - 25
			msg2pos = msg2.get_rect()
			msg2pos.centerx = fenetre.get_rect().centerx
			msg2pos.centery = fenetre.get_rect().centery + 25
			msg3pos = msg3.get_rect()
			msg3pos.centerx = fenetre.get_rect().centerx
			msg3pos.centery = fenetre.get_rect().centery + 50

			fenetre.blit(msg1, (msg1pos[0], msg1pos[1]))
			fenetre.blit(msg2, (msg2pos[0], msg2pos[1]))
			fenetre.blit(msg3, (msg3pos[0], msg3pos[1]))

			pygame.display.update()
			gameOver()
			#mire1.grenades = 10
			mire1.bullets += 10 # bonus stage win
			#mire1.life = 50
			#grenade1.launched = False
			listGrenades = []

			#pygame.mixer.stop()
			fondo1, fondo2, fondomusic = loadStageEnv(StageNumber)
			fondomusic.play()
			groupBandits, groupFarmers, listCaravans, groupCaravans, groupBonusGrenades, groupBonusBullets = loadStageSprites(StageNumber)

			#print pygame.sprite.Group.sprites
			#print groupBandits.sprites()[0].life

			gameTerminate = False
			crono = pygame.time.Clock()
			milli = 0

	else:
		if timeLeft > 0:
			#if mire1.life == 0:
			fenetre.blit(BckGndLoseLife,(0,0))
			msg1 = (FWlettre.render("YOU LOSE BY LIFE", True, (255,0,0)))			
			msg1pos = msg1.get_rect()
			msg1pos.centerx = fenetre.get_rect().centerx
			msg1pos.centery = fenetre.get_rect().centery - 25
			fenetre.blit(msg1, (msg1pos[0], msg1pos[1]))

		else:
			fenetre.blit(BckGndLoseTime,(0,0))
			msg1 = (FWlettre.render("YOU LOSE BY TIME", True, (255,0,0)))			
			msg1pos = msg1.get_rect()
			msg1pos.centerx = fenetre.get_rect().centerx
			msg1pos.centery = fenetre.get_rect().centery - 25
			fenetre.blit(msg1, (msg1pos[0], msg1pos[1]))

		blit_scores()
		pygame.display.update()

		S_Rire.play()

		gameOver()

		StageNumber = 0
		#pygame.mixer.stop()
		fondo1, fondo2, fondomusic = loadStageEnv(StageNumber)
		fondomusic.play()
		groupBandits, groupFarmers, listCaravans, groupCaravans, groupBonusGrenades, groupBonusBullets = loadStageSprites(StageNumber)

		mire1.grenades = VG.ParGrenadeQty #10
		mire1.bullets = VG.ParBulletQty #30
		mire1.life = VG.ParLife #100
		mire1.score = 0
		listGrenades = []
		gameTerminate = False
		crono = pygame.time.Clock()
		milli = 0
		
	#pygame.time.delay(10) #in 1/10
	pygame.time.delay(10) #1sec, in /100
	pygame.display.flip()

pygame.quit()
sys.exit(0)

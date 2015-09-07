#!/usr/bin/env python
# -*- coding: utf8 -*-

#Far West 1789 Stages Parameters

StagesMsg = ["just hit 1 bandit", "hit 2 bandits", "hit 3 bandits", 
"hit 1 bandit, avoide 1 farmer", "hit 2 bandits, avoide 1 farmer", "hit 3 bandits, avoide 1 farmer", 
"hit 1 bandit, shoot 1 diligence", 
"hit 1 bandit, avoide 1 farmer, shoot 1 diligence", "hit 2 bandits, avoide 1 farmer, shoot 1 diligence", "hit 3 bandits, avoide 2 farmers, shoot 2 diligences"]
StagesBandits = [(1, 60, 50), (2, 50, 100), (3, 40, 100), (1, 30, 100), (2, 30, 100), (3, 40, 100), (1, 30, 300), (1, 30, 100), (2, 30, 200), (3, 40, 300)] #(nb, speed, life)
StagesFarmers = [(0, 0), (0, 0), (0, 0), (1, 60), (1, 50), (1, 40), (0, 0), (1, 30), (1, 30), (2, 30)] #(nb, speed)
StagesDiligences = [(1, 40), (2, 60), (0, 0), (0, 0), (0, 0), (0, 0), (1, 40), (1, 50), (1, 60), (2, 40)] #(nb, speed)
StagesGrenades = [(1, 40), (0, 0), (0, 0), (0, 0), (1, 30), (1, 20), (0, 0), (0, 0), (1, 60), (2, 30)] #(nbGrenades, speed)
StagesBullets = [(1, 60), (1, 40), (2, 30), (1, 30), (2, 40), (2, 30), (2, 20), (2, 50), (2, 40), (3, 30)] #(nbBullets, speed)
StagesTime = [200, 200, 300, 200, 200, 300, 200, 200, 200, 400] #10th of secondes
StagesBckGnd1 = ["farwest_f1a", "farwest_f2a", "farwest_f3a", "farwest_f4a", "farwest_f5a", "farwest_f1a", "farwest_f2a", "farwest_f3a", "farwest_f4a", "farwest_f5a"] #jpg from /BckGnd
StagesBckGnd2 = ["branche1c",  "charlottes1b", "western1b",   "stepp1b",    "branche1c",    "charlottes1b", "western1b",   "stepp1b",    "branche1c",   "charlottes1b"] #png from /BckGnd
StagesMusic = ["theme", "Pheasant-Never_Coming_Back", "Pheasant-Letting_Go", "Pheasant-Country_Young", "TheBackRoadBand-SecondChance", "Uke_Stanza-Burglar_Bill", "theme", "Pheasant-Never_Coming_Back", "Pheasant-Letting_Go", "Dead_End_Canada-The_Western_Front"] #ogg from /Sounds

# stage 01-10 slow speed
# stage 11-20 medium speed
# stage 21-30 high speed
#
# diligence can be shooted only with grenades (bonus appears only with diligences)


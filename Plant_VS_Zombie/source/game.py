import image
from const import *
import plantBase
import zombieBase
import pygame as py
import data_object
import zombieBase
import time
import random
class Game(object):
    def __init__(self, Win):
        self.Win = Win
        self.back = image.Image(PATH_BACK, 0, (0,0), GAME_SIZE, 0)
        self.plants = []
        self.zombies = []
        self.summons = []
        self.hasPlant = []
        self.sunshine = 1000
        self.zombieGenerateTime = 0
        self.sunshineFont = py.font.Font('Font1.ttf', 30)
        for i in range(GRID_COUNT[0]):
            col = []
            for j in range(GRID_COUNT[1]):
                col.append(0)
            self.hasPlant.append(col)

        # for i in range(3):
        #     for j in range(GRID_COUNT[1]):
        #         self.addSunFlower(i, j)

    def renderFont(self):
        textImage = self.sunshineFont.render(str(self.sunshine), True, (255, 255, 255))
        self.Win.blit(textImage, (130, 23))
    def fight(self, a, b):
        while True:
            a.hp -= b.atk
            b.hp -= a.atk
            if b.hp <= 0:
                return True
            if a.hp <= 0:
                return False
            return
    def draw(self):
        self.back.draw(self.Win)
        for plant in self.plants:
            plant.draw(self.Win)
        for summon in self.summons:
            summon.draw(self.Win)
        for zombie in self.zombies:
            zombie.draw(self.Win)
        self.renderFont()
    def update(self):

        self.back.update()
        for plant in self.plants:
            plant.update()
            if plant.hasSummon():
                summ = plant.doSummon()
                self.summons.append(summ)
        for summon in self.summons:
            summon.update()
        for zombie in self.zombies:
            zombie.update()
        if time.time() - self.zombieGenerateTime > 2:
            self.zombieGenerateTime = time.time()
            self.addZombie(12, random.randint(0, 4))

        self.checkSummonVSZombie()
    def checkSummonVSZombie(self):
        for summon in self.summons:
            for zombie in self.zombies:
                if summon.isCollide(zombie):
                    self.fight(summon, zombie)
                    if zombie.hp <= 0:
                        self.zombies.remove(zombie)
                    if summon.hp <= 0:
                        summon.summonSound()
                        self.summons.remove(summon)
                    return
    def getIndexByPos(self, pos):
        x = (pos[0] - LEFT_TOP[0]) // GRID_SIZE[0]
        y = (pos[1] - LEFT_TOP[1]) // GRID_SIZE[1]
        return x, y
    def addSunFlower(self, x, y):
        if self.hasPlant[x][y] == 1:
            return False
        self.hasPlant[x][y] = 1
        pos = LEFT_TOP[0] + x * GRID_SIZE[0], LEFT_TOP[1] + y * GRID_SIZE[1]
        sunFlower = plantBase.SunFlower(SUNFLOWER_ID, pos)
        self.plants.append(sunFlower)
    def addPeaShooter(self, x, y):
        if self.hasPlant[x][y] == 1:
            return False
        self.hasPlant[x][y] = 1
        pos = LEFT_TOP[0] + x * GRID_SIZE[0], LEFT_TOP[1] + y * GRID_SIZE[1]
        peaShooter = plantBase.PeaShooter(PEASHOOTER_ID, pos)
        self.plants.append(peaShooter)
    def addZombie(self, x, y):
        sound1 = py.mixer.Sound(PATH_ZOMBIE_VOICE)
        sound1.play()
        pos = LEFT_TOP[0] + x * GRID_SIZE[0], LEFT_TOP[1] + y * GRID_SIZE[1]-50
        zombie = zombieBase.ZombieBase(NORMALZOMBIE_ID, pos)
        self.zombies.append(zombie)
    def checkPick(self, mousePos):
        for summon in self.summons:
            if not summon.canPick():
                continue
            rect = summon.getRect()
            if rect.collidepoint(mousePos):
                sound1 = py.mixer.Sound(PATH_COLLECT_SUN)
                sound1.play()
                self.summons.remove(summon)
                self.sunshine += summon.getPrice()
                return True

        return False
    def checkAddPlant(self, mousePos, objID):
        x, y = self.getIndexByPos(mousePos)
        if x<0 or x>GRID_COUNT[0]:
            return
        if y<0 or y>GRID_COUNT[1]:
            return
        if self.sunshine < data_object.data[objID]['PRICE']:
            return
        if self.hasPlant[x][y] == 1:
            return False
        self.sunshine -= data_object.data[objID]['PRICE']
        if objID == SUNFLOWER_ID:
            sound1 = py.mixer.Sound(PATH_PLANT)
            sound1.play()
            self.addSunFlower(x, y)
        elif objID == PEASHOOTER_ID:
            sound1 = py.mixer.Sound(PATH_PLANT)
            sound1.play()
            self.addPeaShooter(x, y)


    def mouseClickHandler(self, btn):
        mousePos = py.mouse.get_pos()
        if self.checkPick(mousePos):
            return
        if btn == 1:
            self.checkAddPlant(mousePos, SUNFLOWER_ID)
        elif btn == 3:
            self.checkAddPlant(mousePos, PEASHOOTER_ID)
import image
from const import *
import plantBase
import zombieBase
import pygame as py
import data_object
import zombieBase
import time
import random
import card_menu
class Game(object):
    def __init__(self, Win):
        self.Win = Win
        self.back = image.Image(0, PATH_BACK, PATH_BACK,0, (0,0), GAME_SIZE, 0)
        self.plants = []
        self.zombies = []
        self.summons = []
        self.hasPlant = []
        self.sunshine = 1000
        self.zombieGenerateTime = 0
        self.menu_bar = card_menu.MenuBar(CARD_LIST, self.sunshine) # 将 card_menu 传入 Game 类
        self.menu_bar.updateSunshine(self.sunshine)  # 更新 menu_bar 中的阳光值(self.sunshine)  # 初始化时更新阳光值
        self.sunshineFont = py.font.Font(FONT_PATH, 24)  # 初始化 sunshineFont 属性
        for i in range(GRID_COUNT[0]):
            col = []
            for j in range(GRID_COUNT[1]):
                col.append(0)
            self.hasPlant.append(col)

        for i in range(3):
            for j in range(GRID_COUNT[1]):
                self.addSunFlower(i, j)

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


        self.checkHaveZombie()
        for plant in self.plants:
            plant.update()
            py.draw.rect(self.Win, BLACK, plant.getRect(plant.getCollideDeviation(), plant.getCollideDeviationY(), plant.getCollideSize()))
            if plant.hasSummon():
                summ = plant.doSummon()
                self.summons.append(summ)
        for summon in self.summons:
            if summon.status == -100:
                self.summons.remove(summon)
            summon.update()
            #py.draw.rect(self.Win, BLACK, summon.getRect(summon.getCollideDeviation(), summon.getCollideDeviationY(), summon.getCollideSize()))
        for zombie in self.zombies:
            if zombie.status == -100:
                self.zombies.remove(zombie)
            zombie.update()
            py.draw.rect(self.Win, BLACK, zombie.getRect(zombie.getCollideDeviation(), zombie.getCollideDeviationY(), zombie.getCollideSize()))
        if time.time() - self.zombieGenerateTime > 2:
            self.zombieGenerateTime = time.time()
            self.addZombie(12, random.randint(0, 4))

        self.checkSummonVSZombie()
        self.checkZombieVSPlant()
    def checkSummonVSZombie(self):
        for summon in self.summons:
            if not summon.canFight():
                continue
            for zombie in self.zombies:
                if zombie.status == -2:
                    continue
                if summon.isCollide(zombie):
                    self.fight(summon, zombie)
                    if zombie.hp <= 0 and zombie.status != -1:
                        zombie.status = -1
                        zombieHead = zombieBase.ZombieBase(5, zombie.pos)
                        self.summons.append(zombieHead)
                    if summon.hp <= 0:
                        summon.summonSound()
                        summon_copy = summon
                        self.summons.remove(summon)
                        summon_copy.summonBurst(self.Win)
                        del summon_copy
                        break








    def checkZombieVSPlant(self):

        for zombie in self.zombies:
            if zombie.status == -1:
                continue
            for plant in self.plants:
                if zombie.isCollide(plant):
                    zombie.status = 1
                    if time.time() - zombie.preAttackTime <= zombie.getAttackCD():
                        continue
                    zombie.preAttackTime = time.time()
                    self.fight(zombie, plant)
                    if plant.hp <= 0:
                        x, y = self.getIndexByPos(plant.pos)
                        self.plants.remove(plant)
                        self.hasPlant[x][y] = 0
                        zombie.status = 0
                    if zombie.hp <= 0:
                        zombieHead = zombieBase.ZombieBase(5, zombie.pos)
                        self.summons.append(zombieHead)
                        self.status = -1
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
                self.menu_bar.updateSunshine(self.sunshine)  # 更新 menu_bar 中的阳光值
                return True

        return False
    def checkHaveZombie(self):
        for plant in self.plants:
           plant.status=0
           x1, y1 = self.getIndexByPos(plant.pos)
           for zombie in self.zombies:
                x2, y2 = self.getIndexByPos((zombie.pos[0],zombie.pos[1]+50))
                if y2 == y1:
                   plant.status =1
                   break
        return

    def addPlant(self, plant_index, mouse_pos):
        x, y = self.getIndexByPos(mouse_pos)
        if x < 0 or x >= GRID_COUNT[0] or y < 0 or y >= GRID_COUNT[1]:
            return
        if self.sunshine < data_object.data[plant_index]['PRICE']:
            return
        if self.hasPlant[x][y] == 1:
            return False
        self.sunshine -= data_object.data[plant_index]['PRICE']
        self.menu_bar.updateSunshine(self.sunshine)  # 更新 menu_bar 中的阳光值
        if plant_index == 0:
            sound1 = py.mixer.Sound(PATH_PLANT)
            sound1.play()
            self.addSunFlower(x, y)
        elif plant_index == 1:
            sound1 = py.mixer.Sound(PATH_PLANT)
            sound1.play()
            self.addPeaShooter(x, y)
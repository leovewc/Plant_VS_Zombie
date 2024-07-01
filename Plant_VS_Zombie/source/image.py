import pygame as py
import data_object
from const import *
class Image(py.sprite.Sprite):
    def __init__(self, pathFmt, pathIndex, pos, size, pathIndexCount):
        self.pathFmt = pathFmt
        self.pathIndex = pathIndex
        self.size = size
        self.pathIndexCount = pathIndexCount
        self.pos = list(pos)
        self.updateImage()
    def getRect(self, collide_size=(0,0)):
        rect = self.image.get_rect()
        rect.x, rect.y = (self.pos[0], self.pos[1])
        rect.width, rect.height = collide_size
        return rect

    def updateImage(self):
        path = self.pathFmt
        if self.pathIndexCount !=0:
            path = path % self.pathIndex
        self.image = py.image.load(path)
        if self.size:
            self.image = py.transform.scale(self.image, self.size)

    def updateSize(self, size):
        self.size = size
        self.updateImage()
    def updateIndex(self, pathIndex):
        self.pathIndex = pathIndex
        self.updateImage()
    def draw(self, Win):
        Win.blit(self.image, self.getRect())

    def doLeft(self):
        self.pos[0] -= 0.1
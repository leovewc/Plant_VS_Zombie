import image
import time
import data_object
class ObjectBase(image.Image):
    def __init__(self, id, pos):
        self.id = id
        self.preIndexTime = 0
        self.prePositionTime = 0
        self.preSummonTime = 0
        self.hp = self.getData()['HP']
        self.atk = self.getData()['ATK']
        super(ObjectBase, self).__init__(
            self.getData()['PATH'],
            0,
            pos,
            self.getData()['SIZE'],
            self.getData()['IMAGE_INDEX_MAX']
        )
    def getData(self):
        return data_object.data[self.id]
    def update(self):
        self.checkSummon()
        self.checkImageIndex()
        self.checkPosition()
    def isCollide(self, other):
        if self.getRect().colliderect(other.getRect()):
            return True
    def getPositionCD(self):
        return self.getData()['POSITION_CD']
    def getSummonCD(self):
        return self.getData()['SUMMON_CD']
    def canPick(self):
        return self.getData()['CANPICK']
    def getPrice(self):
        return self.getData()['PRICE']
    def getIndexCD(self):
        return self.getData()['IMAGE_INDEX_CD']
    def getSpeed(self):
        return self.getData()['SPEED']

    def checkImageIndex(self):
        if time.time() - self.preIndexTime <= self.getIndexCD():
            return
        self.preIndexTime = time.time()

        index = self.pathIndex + 1
        if index >= self.pathIndexCount:
            index = 0
        self.updateIndex(index)

    def checkSummon(self):
        if time.time() - self.preSummonTime <= self.getSummonCD():
            return False
        self.preSummonTime = time.time()
        self.preSummon()

    def checkPosition(self):
        if time.time() - self.prePositionTime <= self.getPositionCD():
            return False
        self.prePositionTime = time.time()
        speed = self.getSpeed()
        self.pos = (self.pos[0] + speed[0], self.pos[1] + speed[1])
        return True

    def preSummon(self):
        pass
    def hasSummon(self):
        pass
    def doSummon(self):
        pass
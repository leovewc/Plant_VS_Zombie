import objectBase
import sunshine
import peaBullet
import time
class SunFlower(objectBase.ObjectBase):
    def __init__(self, id, pos):
        super(SunFlower, self).__init__(id, pos)
        self.sunShines = []
        self.hasSunshine = False
    def preSummon(self):

        self.hasSunshine = True
    def hasSummon(self):
        return self.hasSunshine
    def doSummon(self):
        if self.hasSunshine:
            self.hasSunshine = False
            return sunshine.Sunshine(2, (self.pos[0] + 20, self.pos[1] - 10))

    def update(self):
        super(SunFlower, self).update()
        for s1 in self.sunShines:
            s1.update()
    def draw(self, Win):
        super(SunFlower, self).draw(Win)
        for s1 in self.sunShines:
            s1.draw(Win)




class PeaShooter(objectBase.ObjectBase):
    def __init__(self, id, pos):
        super(PeaShooter, self).__init__(id, pos)
        self.hasShoot = False
        self.hasBullet = False
    def preSummon(self):
        self.pathIndex = 0
        self.hasBullet = True
    def hasSummon(self):
        return self.hasBullet
    def doSummon(self):
        if self.hasBullet:
            self.hasBullet = False
            return peaBullet.PeaBullet(0, (self.pos[0] + 3, self.pos[1]))

    def update(self):
        super(PeaShooter, self).update()

    def draw(self, Win):
        super(PeaShooter, self).draw(Win)
    def checkImageIndex(self):
        if time.time() - self.preIndexTime <= self.getIndexCD():
            return
        self.preIndexTime = time.time()

        index = self.pathIndex + 1
        if index == 5 and self.hasShoot:
            self.hasShoot = True
        if index >= self.pathIndexCount:
            index = 0
        self.updateIndex(index)
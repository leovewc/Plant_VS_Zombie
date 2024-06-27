import objectBase
import sunshine
import peaBullet
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
        self.sunShines = []
        self.hasBullet = False
    def preSummon(self):

        self.hasBullet = True
    def hasSummon(self):
        return self.hasBullet
    def doSummon(self):
        if self.hasBullet:
            self.hasBullet = False
            return peaBullet.PeaBullet(0, (self.pos[0] + 3, self.pos[1]))

    def update(self):
        super(PeaShooter, self).update()
        for s1 in self.sunShines:
            s1.update()
    def draw(self, Win):
        super(PeaShooter, self).draw(Win)
        for s1 in self.sunShines:
            s1.draw(Win)
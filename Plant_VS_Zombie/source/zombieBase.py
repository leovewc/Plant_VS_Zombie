import objectBase

class ZombieBase(objectBase.ObjectBase):
    # def __init__(self, pathFmt, pathIndex, pos, size = None, pathIndexCount = 0):
    #     super(ZombieBase, self).__init__(pathFmt, pathIndex, pos, size, pathIndexCount)
    #
    # def getIndexCD(self):
    #     return 0.1
    # def getPositionCD(self):
    #
    #     return 0.01
    # def checkPosition(self):
    #     b = super(ZombieBase, self).checkPosition()
    #     if b:
    #         self.pos[0] -= 0.1
    #     return b
    def fight(self, other):
        self.hp -= other.atk
        other.hp -= self.atk
        if self.hp <= 0:
            return True
        if other.hp <= 0:
            return False
        return
    pass
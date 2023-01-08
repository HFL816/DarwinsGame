import Organism as orgo
import random as rand
from WorldComponents import Food

class Enderman(orgo.Organism):
    character = "¡"

    moveTries = 8

    def __init__(self,board,r,c):
        super(Enderman, self).__init__(board,r,c)
        self.teleportEnergy = 2*self.getMoveEnergy()


    def act(self,life,death):
        self.updatePath(self.getCurrentTile())

        if self.energy <= 0 or self.getAge() > self.getAgeCapacity():
            self.die(death)
            self.lastMove = "Died"
            return

        if self.canReproduce():

            mate = self.findMate()
            if mate != None:
                self.reproduce(mate, life)
                self.lastMove = "Reproduced"

                return

        if self.canEat():
            self.eat()
            self.lastMove = "Ate"
            return

        tp = self.canTeleport()
        if tp is not None:
            self.teleport(tp)
            self.lastMove = "Teleported"

        if self.canMove():
            self.move()
            self.lastMove = "Moved"

        self.setEnergy(self.getEnergy() - self.getLivingCost())

        return

    def reproduce(self, mate,life):
        self.setEnergy(self.getEnergy() - self.getReproductionEnergy())
        mate.setEnergy(mate.getEnergy() - mate.getReproductionEnergy())

        options = self.getOptions()

        choice = rand.choice(list(options))

        dest = options[choice]

        life.append(Enderman(self.board, dest.getPosition()[0], dest.getPosition()[1]))

    def teleport(self,op):
        self.occupy(op)
        self.setEnergy(self.getEnergy() - self.getMoveEnergy())


    def canTeleport(self):
        if self.energy < self.getTeleportEnergy():
            return False

        for i in range(self.getMoveTries()):
            dest = (rand.randint(0,self.getBoard().getLength()-1),rand.randint(0,self.getBoard().getLength()-1))
            if not self.getBoard().getTileAt(dest).hasOrganism():
                return dest

        return None

    def getMoveTries(self):
        return self.moveTries

    def getTeleportEnergy(self):
        return self.teleportEnergy


class ChorusFruit(Food):
    character = "○"
    moveTries = 8

    def __init__(self,til,v):
        super(ChorusFruit, self).__init__(til,val=v)

    def activate(self,orgo):
        for i in range(self.getMoveTries()):
            dest = (rand.randint(0,orgo.getBoard().getLength()-1),rand.randint(0,orgo.getBoard().getLength()-1))
            if not orgo.getBoard().getTileAt(dest).hasOrganism():
                orgo.occupy(dest)
                return

    def getMoveTries(self):
        return self.moveTries

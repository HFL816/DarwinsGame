import Organism as orgo
import random as rand

class Carrier(orgo.Organism):

    character = "U"

    pocketEnergy = 0.1

    def __init__(self,board,r,c):
        super(Carrier, self).__init__(board,r,c)
        self.bag = None


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

        if self.canDrop():
            self.drop()
            self.lastMove = "Dropped"

        if self.canPocket():
            self.pocket()
            self.lastMove = "Pocketed"


        if self.canMove():
            self.move()
            self.lastMove = "Moved"

        self.setEnergy(self.getEnergy() - self.getLivingCost())

        return

    def reproduce(self, mate, life):

        self.setEnergy(self.getEnergy() - self.getReproductionEnergy())
        mate.setEnergy(mate.getEnergy() - mate.getReproductionEnergy())

        options = self.getOptions()

        choice = rand.choice(list(options))

        dest = options[choice]

        life.append(Carrier(self.board, dest.getPosition()[0], dest.getPosition()[1]))


    def pocket(self):
        self.bag = self.getCurrentTile().take()
        self.setEnergy(self.getEnergy() - self.pocketEnergy)


    def drop(self):

        options = self.getNoFoodTiles()
        choice = rand.choice(list(options))
        dest = options[choice]

        dest.give(self.emptyBag())

    def canDrop(self):
        return self.getBag() is not None and len(self.getNoFoodTiles()) > 0

    def canPocket(self):
        return self.getEnergy() > self.getFoodCapacity() and self.getCurrentTile().hasFood()

    def getBag(self):
        return self.pocket

    def emptyBag(self):
        res = self.getBag()
        self.bag = None
        return res


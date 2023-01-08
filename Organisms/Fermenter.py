import Organism as orgo
import WorldComponents as wc
import random as rand

class Fermenter(orgo.Organism):

    character = "Y"

    fermentedBonus = 1.1

    def __init__(self,board,r,c):
        super(Fermenter, self).__init__(board, r, c)

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

        if self.canFerment():
            self.ferment()
            self.lastMove = "Fermented"
            return

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

        life.append(Fermenter(self.board, dest.getPosition()[0], dest.getPosition()[1]))

    def eat(self):
        food = self.getCurrentTile().take()
        val = food.getValue()
        if food.getType() == "FermentedFood":
            val *= self.fermentedBonus

        food.activate(self)
        self.setEnergy(self.getEnergy() + val)

    def ferment(self):
        food = self.getCurrentTile().take()
        self.getCurrentTile().give(FermentedFood(self.getCurrentTile(),food.getValue()))


    def canFerment(self):
        return self.getCurrentTile().hasFood() and self.getCurrentTile().getHolding().getType() == "Food"


class FermentedFood(wc.Food):

    character = "v"
    detriment = 0.1

    def __init__(self,tile,val=1.0):
        super(FermentedFood, self).__init__(tile,val)

    def activate(self,orgo):
        if orgo.getType() != "Fermenter":
            orgo.decrementEnergy(self.getDetriment())

    def getDetriment(self):
        return self.detriment
import Organism as orgo
import WorldComponents as wc
import random as rand


class Bartolomeo(orgo.Organism):
    character = "<"

    def __init__(self, board, r, c):

        super(Bartolomeo, self).__init__(board, r, c)
        self.diet = super(Bartolomeo, self).getDiet() | {"CaniBody"}
        

    def reproduce(self, mate,life):

        self.setEnergy(self.getEnergy() - self.getReproductionEnergy())
        mate.setEnergy(mate.getEnergy() - mate.getReproductionEnergy())

        options = self.getOptions()

        choice = rand.choice(list(options))

        dest = options[choice]

        life.append(Bartolomeo(self.board, dest.getPosition()[0], dest.getPosition()[1]))

    def eat(self):
        food = self.getCurrentTile().getHolding()

        if food.getCharacter() == '^':
            self.setEnergy(self.getEnergy() + food.getBodyValue())
        else:
            self.setEnergy(self.getEnergy() + food.getValue())

        self.getCurrentTile().take()

    def die(self,death):

        if self.getCurrentTile().hasFood():
            self.getCurrentTile().take()

        self.getCurrentTile().give(CaniBody(self.getCurrentTile(), abs(self.getEnergy())))

        super().die(death)


class CaniBody(wc.Food):
    character = "^"

    def __init__(self, til, body_val):
        super(CaniBody, self).__init__(til, val=body_val)
        self.body_value = body_val

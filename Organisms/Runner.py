import Organism as orgo
import random as rand


class Runner(orgo.Organism):
    character = "$"
    move_gain = 0.07  # per 1 move
    move_number = 2

    def __init__(self, bord, r, c):
        super(Runner, self).__init__(bord, r, c)

    def reproduce(self, mate,life):
        self.setEnergy(self.getEnergy() - self.getReproductionEnergy())
        mate.setEnergy(mate.getEnergy() - mate.getReproductionEnergy())

        options = self.getOptions()

        choice = rand.choice(list(options))

        dest = options[choice]

        life.append(Runner(self.board, dest.getPosition()[0], dest.getPosition()[1]))

    def move(self):
        for i in range(self.getMoveNumber()):
            if self.canMove():
                super().move()

        self.setEnergy(self.getEnergy() + (self.getMoveGain() * self.getMoveNumber()) - self.getMoveEnergy())

    def getMoveGain(self):
        return self.move_gain

    def getMoveNumber(self):
        return self.move_number





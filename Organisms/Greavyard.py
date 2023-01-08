import Organism as orgo
import WorldComponents as wc
import random as rand


class Greavyard(orgo.Organism):

    character = "☎"
    reapValue = 0.1

    def __init__(self,board,r,c):
        super(Greavyard, self).__init__(board,r,c)

    def act(self,life,death):
        super(Greavyard, self).act(life,death)

        if self.canReap():
            self.reap()
            self.lastMove += "(Reaped)"

    def reproduce(self, mate,life):

        self.setEnergy(self.getEnergy() - self.getReproductionEnergy())
        mate.setEnergy(mate.getEnergy() - mate.getReproductionEnergy())

        options = self.getOptions()

        choice = rand.choice(list(options))

        dest = options[choice]

        life.append(Greavyard(self.board, dest.getPosition()[0], dest.getPosition()[1]))

    def reap(self):
        neighbors = self.getNeighboringOrganisms()

        for key in neighbors:
            toReap = min(self.getReapValue(),neighbors[key].getEnergy())
            self.incrementEnergy(toReap)
            neighbors[key].decrementEnergy(toReap)

    def canReap(self):
        return len(self.getNonOptions()) > 0

    def getReapValue(self):
        return self.reapValue
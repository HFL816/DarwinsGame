import Organism as orgo

class Solosis(orgo.Organism):

    splitCooldown = 4

    def __init__(self,board,r,c):
        super(Solosis, self).__init__(board,r,c)
        self.lastSplit = self.splitCooldown + 1

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

        if self.canPainSplit():
            self.painSplit()
            self.lastMove = "Pain Split"
            return

        if self.canMove():
            self.move()
            self.lastMove = "Moved"

        self.setEnergy(self.getEnergy() - self.getLivingCost())


    def painSplit(self):
        neighbors = self.getNeighboringSolosis()
        ne = 0
        for key in neighbors:
            ne += neighbors[key].getEnergy()

        ne/= len(neighbors)

        for key in neighbors:
            neighbors[key].setEnergy(ne)
            neighbors[key].resetPainSplitCooldown()

    def canPainSplit(self):
        return self.lastSplit > self.splitCooldown and len(self.getNeighboringSolosis()) > 0

    def resetPainSplitCooldown(self):
        self.lastSplit = 0

    def getNeighboringSolosis(self):
        possible_options = self.getNonOptions()
        options = {}

        for key in possible_options:
            n_orgo = possible_options[key].getOccupant()
            if n_orgo.getType() == "Solosis":
                options[key] = n_orgo

        return options
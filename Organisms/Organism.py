import random as rand

class Organism:
    character = "*"
    diet = {"Food", "FermentedFood"}
    reproduction_energy = 1.0
    age_capacity = 51
    food_capacity = 7.0
    move_energy = 0.2
    living_cost = 0.1

    def __init__(self, board, r, c):

        self.board = board
        self.r = r
        self.c = c
        self.energy=0.9
        self.path = []
        self.lastMove = "None"

        self.occupy((r,c))

    def __str__(self):

        ns = ("Type: " + self.getType() +
              "\nPosition: " + str(self.getPosition()) +
              "\nEnergy: " + str(self.energy) +
              "\nAge: " + str(self.getAge()) +
              "\nPath: " + self.getPathStr() +
              "\nLast Move: " + self.getLastMove() + "\n")

        return ns

    def act(self,life,death):

        self.updatePath(self.getCurrentTile())

        if self.energy <= 0 or self.getAge() > self.getAgeCapacity():
            self.die(death)
            self.lastMove = "Died"
            return

        if self.canReproduce():

            mate = self.findMate()
            if mate != None:
                self.reproduce(mate,life)
                self.lastMove = "Reproduced"

                return

        if self.canEat():
            self.eat()
            self.lastMove = "Ate"
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

        life.append(Organism(self.board, dest.getPosition()[0], dest.getPosition()[1]))


    def findMate(self):

        possible_options = self.getNeighboringOrganisms()
        options = []

        for key in possible_options:

            if possible_options[key].getType() == self.getType() and possible_options[key].canReproduce():
                options.append(possible_options[key])

        if (len(options) == 0):
            return None

        choice = rand.randint(0, len(options) - 1)

        return options[choice]

    def move(self):

        options = self.getOptions()

        choice = rand.choice(list(options))

        self.occupy(options[choice].getPosition())

        self.setEnergy(self.getEnergy() - self.getMoveEnergy())


    def occupy(self,op):
        self.getCurrentTile().setOccupant(None)
        self.setPosition(op)
        self.getCurrentTile().setOccupant(self)


    def eat(self):
        self.setEnergy(self.getEnergy() + self.getCurrentTile().take().getValue())

    def die(self,death):
        self.getCurrentTile().setOccupant(None)
        death.append(self)

    def getNeighboringOrganisms(self):
        possible_options = self.getNonOptions()
        options = {}

        for key in possible_options:
            options[key] = possible_options[key].getOccupant()

        return options

    def getOptions(self):

        possible_options = self.getCurrentTile().getNeighbors()
        options = {}

        for key in possible_options:

            if possible_options[key] != None:

                if not possible_options[key].hasOrganism():
                    options[key] = possible_options[key]

        return options

    def getNonOptions(self):
        possible_options = self.getCurrentTile().getNeighbors()
        options = {}

        for key in possible_options:

            if possible_options[key] != None:

                if possible_options[key].hasOrganism():
                    options[key] = possible_options[key]

        return options

    def getNoFoodTiles(self):
        neighbors = self.getCurrentTile().getNeighbors()
        options = {}

        for key in neighbors:
            if not neighbors[key].hasFood():
                options[key] = neighbors[key]

        return options

    def updatePath(self, tile):
        self.path.append(tile.getNumber())

    def canReproduce(self):

        return (self.energy >= self.getReproductionEnergy()) and (len(self.getOptions()) > 0)

    def canMove(self):

        return self.energy >= self.getMoveEnergy() and len(self.getOptions()) > 0

    def canEat(self):

        food = self.getCurrentTile().getHolding()
        if food is None:
            return False

        return (self.getEnergy() < self.getFoodCapacity()) and food.getType() in self.getDiet()

    def setEnergy(self, val):
        self.energy = val

    def setPosition(self, op):
        self.r = op[0]
        self.c = op[1]

    def getPosition(self):
        return (self.r, self.c)

    def row(self):
        return self.r
    def col(self):
        return self.c

    def getBoard(self):

        return self.board

    def getCurrentTile(self):

        return self.board.getTileAt(self.getPosition())

    def getPathStr(self):
        return self.path.__str__()

    def getPath(self):
        return self.path

    def getEnergy(self):
        return self.energy

    def getType(self):
        return self.__class__.__name__

    def getReproductionEnergy(self):
        return self.reproduction_energy

    def getLivingCost(self):
        return self.living_cost

    def getMoveEnergy(self):
        return self.move_energy

    def getLastMove(self):
        return self.lastMove

    def getAge(self):
        return len(self.path)

    def getAgeCapacity(self):
        return self.age_capacity

    def getFoodCapacity(self):
        return self.food_capacity

    def getCharacter(self):
        return self.character

    def getDiet(self):
        return self.diet

    def getType(self):
        return self.__class__.__name__

    def setReproductionEnergy(self, nv):
        self.reproduction_energy = nv

    def setLivingCost(self, nv):
        self.living_cost = nv

    def setMoveEnergy(self, nv):
        self.move_energy = nv

    def setAgeCapacity(self, nv):
        self.age_capacity = nv

    def setFoodCapacity(self, nv):
        self.food_capacity = nv




import random as rand

class Tile:
    character = "x"

    def __init__(self, n, b, pos):

        self.number = n
        self.parent = b
        self.neighbors = {"up": None, "down": None, "left": None, "right": None}
        self.row = pos[0]
        self.col = pos[1]
        self.occupant = None
        self.holding = None

    def __str__(self):
        nei_str = ""

        for key in self.neighbors:
            if self.neighbors[key] != None:
                nei_str += key + ": " + str(self.neighbors[key].number) + ", "

        return ("Tile #: " + str(self.number) + "\n" +
                "At Position: (" + str(self.row) + ", " + str(self.col) + ")\n" +
                "Neighbors: " + nei_str + "\n" +
                "Holding " + self.holding.__str__() + "\n" +
                "Has Occupant: " + str(self.hasOrganism()) + "\n\n")

    def setNeighbor(self, k, tile):  # k is for key

        if k in self.neighbors:
            self.neighbors[k] = tile
        else:
            print("\'" + k + "\' key is not in self.neighbors")

    def linkUp(self):

        if self.row > 0:
            self.neighbors["up"] = self.parent.board[self.row - 1][self.col]

        if self.row < self.parent.length-1:
            self.neighbors["down"] = self.parent.board[self.row + 1][self.col]

        if self.col > 0:
            self.neighbors["left"] = self.parent.board[self.row][self.col - 1]

        if self.col < self.parent.length - 1:
            self.neighbors["right"] = self.parent.board[self.row][self.col+1]

    def hasOrganism(self):
        return self.occupant is not None

    def give(self, obj):
        self.holding = obj

    def take(self):
        res = self.holding
        self.holding = None
        return res

    def hasFood(self):
        return not self.holding is None

    def getHolding(self):
        return self.holding

    def getOccupant(self):
        return self.occupant

    def getNeighbors(self):
        return self.neighbors

    def getPosition(self):
        return (self.row,self.col)

    def getNumber(self):
        return self.number

    def getCharacter(self):
        return self.character

    def setOccupant(self,orgo):
        self.occupant = orgo


class Board:

    def __init__(self, length=4):

        self.playing = False
        self.board = []
        self.population = set()

        self.length = length
        self.fillBoard()

    def __str__(self):

        ns = ""

        for i in range(len(self.board)):

            ns += "["

            for k in range(len(self.board[i])):

                current_tile = self.getTileAt((i,k))

                if current_tile.hasOrganism():
                    cd = current_tile.getOccupant().getCharacter()
                elif current_tile.hasFood():
                    cd = current_tile.getHolding().getCharacter()
                else:
                    cd = current_tile.getCharacter()

                ns+= cd + ","

            ns += "]\n"

        return ns

    def fillBoard(self):

        c=0

        for i in range(self.length):

            nar = []

            for k in range(self.length):
                nar.append(Tile(c,self,(i,k)))
                c+=1

            self.board.append(nar)

        for i in range(self.length):
            for k in range(self.length):
                self.board[i][k].linkUp()

    def live(self, show):

        dead = []
        born = []

        for organism in self.population:
            organism.act(born,dead)


        for orgo in dead:
            self.removeOrganism(orgo)

        for orgo in born:
            self.addOrganism(orgo)

        if show:
            self.showWorld()

    def hasOrganism(self,r,c):
        return self.getTileAt((r,c)).hasOrganism()

    def cleanup(self):

        for i in range(self.length):
            for k in range(self.length):
                self.board[i][k].take()

    def addFood(self, frq):  # frq has to be (0,1]

        if frq > 1 or frq < 0:
            print("Invalid frq: " + str(frq))
            return

        c = 0

        for i in range(self.length):
            for k in range(self.length):
                r = rand.random()

                if r <= frq:
                    self.board[i][k].give(Food(self.board[i][k], 1))  # food value can vary
                    c += 1

        # print("gave " + str(round(float(c)/self.getArea() * 100,4)) + "% food")

    def removeOrganism(self, orgo):

        self.population.remove(orgo)

    def regenFood(self, val):
        self.cleanup()
        self.addFood(val)

    def addOrganism(self, org):
        self.population.add(org)

    def clear(self):
        self.population.clear()
        self.cleanup()

    def printTiles(self):
        for i in range(len(self.board)):
            for k in range(len(self.board[i])):
                print(self.board[i][k])

    def showWorld(self):
        print(self)

        for organism in self.population:
            print(organism)

    def getPopulation(self):
        return self.population

    def getPopulationSize(self):
        return len(self.population)

    def getArea(self):
        return self.length ** 2

    def getOrganismAt(self,r,c):
        return self.getTileAt(r,c).getOccupant()

    def getTileAt(self,op):
        return self.board[op[0]][op[1]]

    def getTilePosition(self, tile):

        for i in range(len(self.board)):
            for k in range(len(self.board[i])):
                if tile == self.board[i][k]:
                    return (k, i)

        return (-1, -1)

    def numberToTilePosition(self, number):

        return (number / self.length, number % self.length)


    def numberToTile(self, number):
        return self.getTileAt((number / self.length, number % self.length))


class Food:
    character = "."

    def __init__(self, til, val=1.0):
        self.tile = til
        self.value = val

    def __str__(self):  # must be one line due to tile __str__
        return "Type=" + self.getType() + "Food Value=" + str(self.value) + " Parent = Tile " + str(self.tile.number)

    def activate(self,orgo):
        return

    def getValue(self):
        return self.value

    def getType(self):
        return self.__class__.__name__

    def getCharacter(self):
        return self.character
    
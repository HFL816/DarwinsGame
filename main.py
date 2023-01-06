import WorldComponents as wc
from Organisms import Organism as orgo
import matplotlib.pyplot as plt


def main():
    board = wc.Board(length=20)

    c = 0

    n = 10

    for i in range(n):
        board.addOrganism(orgo.Organism(board,i,i))

    for k in range(1000):

        if c % 50 == 0:
            board.regenFood(0.5)
            board.live(True)
            stall = input(str(k))
            continue

        board.live(False)
        c += 1

main()






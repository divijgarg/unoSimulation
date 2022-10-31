# coded by Divij Garg

import random
import copy
import statistics
import numpy as np
import matplotlib.pyplot as plt
import numpy.random

minPlayers = 0
maxPlayers = 0
minCards = 0
maxCards = 0
simulations = []
cardDeck = []


class OneTrialSimulation:

    def __init__(self, play, cards, mainDeck):
        self.moveCounter = 0
        self.numPlayers = play
        self.numCards = cards
        self.probabilities = []
        self.averageProb = 0
        self.playersDecks = []
        self.currentCard = []
        self.currentColor = -121
        self.cardsPlaced = []
        self.numberFail = 0
        self.currentPlayerIndex = 0
        self.reverse = 1
        self.moveCounter = 0
        self.cardDeck = []

    # runs one game
    def doSimulation(self):
        self.createCardDeck()
        self.setPlayersDecks()
        self.setCurrentCard()
        while not self.winning():
            self.doTurn(self.currentPlayerIndex)
            self.moveCounter += 1
            self.currentPlayerIndex = self.currentPlayerIndex % self.numPlayers
            while self.currentPlayerIndex < 0:
                self.currentPlayerIndex += self.numPlayers
            self.checkMainDeck()
            self.probabilities.append(1 - self.numberFail / self.moveCounter)
        self.averageProb = statistics.mean(self.probabilities)

    # Ensures Deck does not run out of cards
    def checkMainDeck(self):
        while len(self.cardDeck) < 6 and len(self.cardsPlaced) > 1:
            self.cardDeck.append(self.cardsPlaced[0])
            self.cardsPlaced.pop(0)

    # Selects an appropriate strategy based on many factors
    def doTurn(self, index):
        nextPlayerIndex = (self.currentPlayerIndex + self.reverse) % self.numPlayers
        if len(self.playersDecks[nextPlayerIndex]) <= 3:
            self.bigBrainMove(index)
        else:
            self.youngChildMove(index)

    def winning(self):
        for i in range(0, self.numPlayers):
            if len((self.playersDecks[i])) == 0:
                return True
        return False

    # initializes players decks by first creating the amount of player decks and then filling them with cards.
    def setPlayersDecks(self):
        for _ in range(0, self.numPlayers):
            self.playersDecks.append([])
        for _ in range(0, self.numCards):
            for i in range(0, self.numPlayers):
                card = self.cardDeck[0]
                self.cardDeck.pop(0)
                self.playersDecks[i].append(card)

    # sets the current card, makes sure it's a numeral one.
    def setCurrentCard(self):
        self.currentCard = self.cardDeck[0]
        self.cardDeck.pop(0)
        self.cardDeck.append(self.currentCard)
        self.currentColor = self.currentCard[1]

        while self.currentCard[0] > 10:
            self.cardDeck.pop(0)
            self.cardDeck.append(self.currentCard)
            self.currentCard = self.cardDeck[0]
            self.currentColor = self.currentCard[1]

        self.cardsPlaced.append(self.currentCard)

    # this algorithm preferences number cards over action cards
    def youngChildMove(self, index):
        play = []
        possibleActionCards = self.returnActionCards(self.playersDecks[index])
        possibleWildCards = self.returnWildCards(self.playersDecks[index])
        possibleNumberCards = self.returnNumberCards(self.playersDecks[index])

        if len(possibleNumberCards) > 0:
            play = possibleNumberCards[self.returnRandInt(0, len(possibleNumberCards) - 1)]
        elif len(possibleActionCards) > 0:
            play = possibleActionCards[self.returnRandInt(0, len(possibleActionCards) - 1)]
        elif len(possibleWildCards) > 0:
            play = possibleWildCards[self.returnRandInt(0, len(possibleWildCards) - 1)]

        if play == []:
            self.playersDecks[index].append(self.getNewCard())
            self.currentPlayerIndex += 1 * self.reverse
            self.numberFail += 1
        else:
            self.doPlay(play, index)

    # this algorithm preferences number cards over action cards
    def bigBrainMove(self, index):
        play = []
        possibleDrawTwos = self.returnGeneralCard(self.playersDecks[index], 10)
        possibleReverses = self.returnGeneralCard(self.playersDecks[index], 11)
        possibleSkips = self.returnGeneralCard(self.playersDecks[index], 12)
        possibleWilds = self.returnGeneralCard(self.playersDecks[index], 13)
        possibleDrawFours = self.returnGeneralCard(self.playersDecks[index], 14)
        possibleNumberCards = self.returnNumberCards(self.playersDecks[index])

        if len(possibleDrawTwos) > 0:
            play = possibleDrawTwos[self.returnRandInt(0, len(possibleDrawTwos) - 1)]
        elif len(possibleSkips) > 0:
            play = possibleSkips[self.returnRandInt(0, len(possibleSkips) - 1)]
        elif len(possibleReverses) > 0:
            play = possibleReverses[self.returnRandInt(0, len(possibleReverses) - 1)]
        elif len(possibleDrawFours) > 0:
            play = possibleDrawFours[self.returnRandInt(0, len(possibleDrawFours) - 1)]
        elif len(possibleWilds) > 0:
            play = possibleWilds[self.returnRandInt(0, len(possibleWilds) - 1)]
        elif len(possibleNumberCards) > 0:
            play = possibleNumberCards[self.returnRandInt(0, len(possibleNumberCards) - 1)]

        if play == []:
            self.playersDecks[index].append(self.getNewCard())
            self.currentPlayerIndex += 1 * self.reverse
            self.numberFail += 1
        else:
            self.doPlay(play, index)

    # returns amount of a certain card
    def returnGeneralCard(self, array, card):
        cards = []
        self.currentCard = self.cardsPlaced[len(self.cardsPlaced) - 1]
        for i in range(0, len(array)):
            if card <= array[i][0] <= card + 1:
                if array[i][0] == self.currentCard[0] or array[i][1] == self.currentColor:
                    cards.append(array[i])
        return cards

    # returns the action cards
    def returnActionCards(self, array):
        cards = []
        self.currentCard = self.cardsPlaced[len(self.cardsPlaced) - 1]
        for i in range(0, len(array)):
            if 10 <= array[i][0] <= 12:
                if array[i][0] == self.currentCard[0] or array[i][1] == self.currentColor:
                    cards.append(array[i])
        return cards

    # returns the wild cards
    def returnWildCards(self, array):
        cards = []
        for i in range(0, len(array)):
            if array[i][0] >= 13:
                cards.append(array[i])
        return cards

    # return number cards
    def returnNumberCards(self, array):
        cards = []
        self.currentCard = self.cardsPlaced[len(self.cardsPlaced) - 1]
        for i in range(0, len(array)):
            if 0 <= array[i][0] <= 9:
                if array[i][0] == self.currentCard[0] or array[i][1] == self.currentColor:
                    cards.append(array[i])
        return cards

    def returnRandInt(self, min, max):
        if min == max:
            return min
        return random.randint(min, max)

    # after a move choosing algorithm has been chosen, this function actually implements the effects of choosing that card
    def doPlay(self, play, index):
        self.cardsPlaced.append(play)
        self.currentColor = self.cardsPlaced[1][1]
        self.playersDecks[index].remove(play)
        if play[0] == 10:
            self.plusTwo(index)
        elif play[0] == 11:
            self.reverse *= (-1)
        elif play[0] == 12:
            self.currentPlayerIndex += 2 * self.reverse
        elif play[0] == 13:
            self.doWild(index, True)
        elif play[0] == 14:
            self.doDrawFour(index)
        else:
            self.currentPlayerIndex += 1 * self.reverse

    def doDrawFour(self, index):
        self.doWild(index, False)
        for _ in range(4):
            self.playersDecks[(index + self.reverse) % self.numPlayers].append(self.getNewCard())
        self.currentPlayerIndex += 2 * self.reverse

    # returnsNumberOfColor
    def returnNumberOfColor(self, index, color):
        amount = 0
        for i in range(0, len(self.playersDecks[index])):
            if self.playersDecks[index][i][1] == color:
                amount += 1
        return amount

    # does the logic for the draw two card
    def plusTwo(self, index):
        self.playersDecks[(index + self.reverse) % self.numPlayers].append(self.getNewCard())
        self.playersDecks[(index + self.reverse) % self.numPlayers].append(self.getNewCard())
        self.currentPlayerIndex += 2 * self.reverse

    # returns a new card from the card deck while removing it from the main deck
    def getNewCard(self):
        card = self.cardDeck[0]
        self.cardDeck.pop(0)
        return card

    # chooses the best color for the player
    def doWild(self, index, changeIndex):
        numberOfColor = [self.returnNumberOfColor(index, i) for i in range(0, 4)]
        index = 0
        for i in range(len(numberOfColor)):
            if numberOfColor[index] < numberOfColor[i]:
                index = i

        self.currentColor = index

        if changeIndex:
            self.currentPlayerIndex += self.reverse

    def createCardDeck(self):
        for i in range(0, 4):
            self.cardDeck.append([0, i])
            self.cardDeck.append([13, 5])
            self.cardDeck.append([14, 5])

        for i in range(1, 13):
            for j in range(0, 8):
                self.cardDeck.append([i, j % 4])

        np.random.shuffle(self.cardDeck)


# stores all trials with given players and cards
class Simulation:
    def __init__(self, numTrials, play, cards, mainDeck):
        self.trials = []
        self.numTrials = numTrials
        self.numPl = play
        self.numCa = cards
        self.meanNumberOfMoves = 0
        self.averageProb = 0
        self.deck = copy.deepcopy(mainDeck)

    # runs trials for given players and cards
    def runSimulations(self):
        for i in range(0, self.numTrials):
            trial = OneTrialSimulation(self.numPl, self.numCa, self.deck)
            trial.doSimulation()
            self.trials.append(trial)
        self.analyze()

    def analyze(self):
        meanArray = []
        probArray = []
        for i in range(0, len(self.trials)):
            meanArray.append(self.trials[i].moveCounter)
            probArray.append(self.trials[i].averageProb)
        self.meanNumberOfMoves = statistics.mean(meanArray)
        self.averageProb = statistics.mean(probArray)


def main():
    global maxCards, minCards, minPlayers, maxPlayers, cardDeck
    minPlayers = 3
    maxPLayers = 7
    minCards = 3
    maxCards = 14
    createCardDeck()
    for players in range(minPlayers, maxPLayers + 1):
        for cards in range(minCards, maxCards + 1):
            print(players + cards)
            numpy.random.shuffle(cardDeck)
            sim = Simulation(1000, players, cards, cardDeck)
            sim.runSimulations()
            simulations.append(sim)
    makeGraphs()

    # print(simulations)


def analyzeData():
    print("test")


# # makes graphs using the data collected
def makeGraphs():
    global simulations
    arr = []
    for i in range(minCards, maxCards + 1):
        arr.append(i)

    x = np.array(arr)  # X-axis points

    amt = maxCards - minCards + 1
    probabilites = []
    for i in range(0, amt):
        probabilites.append(simulations[i].meanNumberOfMoves)
    plt.plot(x, probabilites, label="3 Players")
    plt.legend(loc="upper left")

    probabilites = []
    for i in range(amt, amt * 2):
        probabilites.append(simulations[i].meanNumberOfMoves)

    plt.plot(x, probabilites, label="4 Players")

    probabilites = []
    for i in range(amt * 2, amt * 3):
        probabilites.append(simulations[i].meanNumberOfMoves)

    plt.plot(x, probabilites, label="5 Players")

    probabilites = []
    for i in range(amt * 3, amt * 4):
        probabilites.append(simulations[i].meanNumberOfMoves)

    plt.plot(x, probabilites, label="6 Players")

    probabilites = []
    for i in range(amt * 4, amt * 5):
        probabilites.append(simulations[i].meanNumberOfMoves)

    plt.plot(x, probabilites, label="7 Players")
    plt.legend(loc="upper left")

    plt.show()

    arr = []
    for i in range(minCards, maxCards + 1):
        arr.append(i)

    x = np.array(arr)  # X-axis points

    amt = maxCards - minCards + 1
    probabilites = []
    for i in range(0, amt):
        probabilites.append(simulations[i].averageProb)
    plt.plot(x, probabilites, label="3 Players")
    plt.legend(loc="upper left")

    probabilites = []
    for i in range(amt, amt * 2):
        probabilites.append(simulations[i].averageProb)

    plt.plot(x, probabilites, label="4 Players")

    probabilites = []
    for i in range(amt * 2, amt * 3):
        probabilites.append(simulations[i].averageProb)

    plt.plot(x, probabilites, label="5 Players")

    probabilites = []
    for i in range(amt * 3, amt * 4):
        probabilites.append(simulations[i].averageProb)

    plt.plot(x, probabilites, label="6 Players")

    probabilites = []
    for i in range(amt * 4, amt * 5):
        probabilites.append(simulations[i].averageProb)

    plt.plot(x, probabilites, label="7 Players")
    plt.legend(loc="upper left")

    plt.show()


def createCardDeck():
    global cardDeck
    for i in range(0, 4):
        cardDeck.append([0, i])
        cardDeck.append([13, 5])
        cardDeck.append([14, 5])

    for i in range(1, 13):
        for j in range(0, 8):
            cardDeck.append([i, j % 4])

    np.random.shuffle(cardDeck)


main()

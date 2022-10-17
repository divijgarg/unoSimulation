#coded by Divij Garg
# points of research: average number of turns for a game of uno to end
# average deck size of players
# assumptions/restrictions: no "uno" moment

import random
import numpy as np

cardDeck = []
numberOfPlayers = 0
playersDecks = []
cardsPlaced = []
currentColor = -6
reverse = 1
currentPlayerIndex = 0


def main():
    global numberOfPlayers, cardDeck, currentPlayerIndex
    createCardDeck()
    setPlayersDecks(3)
    setCurrentCard()
    while not winning():
        print(currentPlayerIndex)
        print(playersDecks)
        # print(cardDeck)
        print(currentColor)
        print(cardsPlaced)
        print("----------")
        doTurn(currentPlayerIndex)
        currentPlayerIndex = currentPlayerIndex % numberOfPlayers
        while currentPlayerIndex < 0:
            currentPlayerIndex + numberOfPlayers
        checkMainDeck()
        # print(playersDecks)


# Ensures Deck does not run out of cards
def checkMainDeck():
    global cardDeck, cardsPlaced

    while len(cardDeck) < 10:
        for i in range(0, 4):
            cardDeck.append(cardsPlaced[0])
            cardsPlaced.pop(0)


# Selects an appropriate strategy based on many factors
def doTurn(index):
    global playersDecks, numberOfPlayers
    youngChildMove(index)


def winning():
    global playersDecks, numberOfPlayers
    for i in range(0, numberOfPlayers):
        if len((playersDecks[i])) == 0:
            return True
    return False


# initializes players decks by first creating the amount of player decks and then filling them with cards.
def setPlayersDecks(amount):
    global numberOfPlayers, playersDecks, cardDeck
    numberOfPlayers = amount
    for _ in range(0, numberOfPlayers):
        playersDecks.append([])
    for _ in range(0, 7):
        for i in range(0, numberOfPlayers):
            card = cardDeck[0]
            cardDeck.pop(0)
            playersDecks[i].append(card)


# initializes the carddeck array by filling it with cards and shuffles the array. first index is number, second index is color
# 10=draw 2, 11=reverse, 12=skip,13=wild, 14= draw four
# 0=blue, 1=red, 2=green, 3=yellow
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
    # print(cardDeck)


# sets the current card, makes sure it's a numeral one.
def setCurrentCard():
    global cardsPlaced, cardDeck, currentColor
    currentCard = cardDeck[0]
    cardDeck.pop(0)
    cardDeck.append(currentCard)
    currentColor = currentCard[1]

    while currentCard[0] > 10:
        cardDeck.pop(0)
        cardDeck.append(currentCard)
        currentCard = cardDeck[0]
        currentColor = currentCard[1]

    cardsPlaced.append(currentCard)

    # print(currentCard)


# this algorithm preferences action cards over regular cards
def youngChildMove(index):
    global playersDecks, cardDeck, reverse, currentPlayerIndex
    play = []
    possibleActionCards = returnActionCards(playersDecks[index])
    possibleWildCards = returnWildCards(playersDecks[index])
    possibleNumberCards = returnNumberCards(playersDecks[index])

    if len(possibleNumberCards) > 0:
        play = possibleNumberCards[returnRandInt(0, len(possibleNumberCards) - 1)]
    elif len(possibleActionCards) > 0:
        play = possibleActionCards[returnRandInt(0, len(possibleActionCards) - 1)]
    elif len(possibleWildCards) > 0:
        play = possibleWildCards[returnRandInt(0, len(possibleWildCards) - 1)]
    # print(play)

    if play == []:
        playersDecks[index].append(getNewCard())
        currentPlayerIndex += 1 * reverse
    else:
        doPlay(play, index)
        # print(playersDecks[index])


# returns the action cards
def returnActionCards(array):
    global cardsPlaced, currentColor
    cards = []
    currentCard = cardsPlaced[len(cardsPlaced) - 1]
    for i in range(0, len(array)):
        if 10 <= array[i][0] <= 12:
            if array[i][0] == currentCard[0] or array[i][1] == currentColor:
                cards.append(array[i])
    return cards


# returns the wild cards
def returnWildCards(array):
    global cardsPlaced
    cards = []
    for i in range(0, len(array)):
        if array[i][0] >= 13:
            cards.append(array[i])
    return cards


# return number cards
def returnNumberCards(array):
    global cardsPlaced, currentColor
    cards = []
    currentCard = cardsPlaced[len(cardsPlaced) - 1]
    for i in range(0, len(array)):
        if 0 <= array[i][0] <= 9:
            if array[i][0] == currentCard[0] or array[i][1] == currentColor:
                cards.append(array[i])
    return cards


def returnRandInt(min, max):
    if min == max:
        return min
    return random.randint(min, max)


# after a move choosing algorithm has been chosen, this function actually implements the effects of choosing that card
def doPlay(play, index):
    global cardsPlaced, playersDecks, reverse, currentPlayerIndex, currentColor
    cardsPlaced.append(play)
    currentColor = cardsPlaced[1][1]
    playersDecks[index].remove(play)
    if play[0] == 10:
        plusTwo(index)
    elif play[0] == 11:
        reverse *= (-1)
    elif play[0] == 12:
        currentPlayerIndex += 2 * reverse
    elif play[0] == 13:
        doWild(index,True)
    elif play[0] == 14:
        doDrawFour(index)
    else:
        currentPlayerIndex += 1 * reverse


def doDrawFour(index):
    global numberOfPlayers, playersDecks, currentPlayerIndex, reverse
    doWild(index,False)
    for _ in range(4):
        playersDecks[(index + reverse) % numberOfPlayers].append(getNewCard())
    currentPlayerIndex += 2 * reverse


# chooses the best color for the player
def doWild(index, changeIndex):
    global currentColor, currentPlayerIndex, reverse
    numberOfColor = [returnNumberOfColor(index, i) for i in range(0, 4)]
    index = 0
    for i in range(len(numberOfColor)):
        if numberOfColor[index] < numberOfColor[i]:
            index = i

    currentColor = index

    if changeIndex:
        currentPlayerIndex += reverse


# returnsNumberOfColor
def returnNumberOfColor(index, color):
    global playersDecks
    amount = 0
    for i in range(0, len(playersDecks[index])):
        if playersDecks[index][i][1] == color:
            amount += 1
    return amount


# does the logic for the draw two card
def plusTwo(index):
    global playersDecks, numberOfPlayers, currentPlayerIndex, reverse
    playersDecks[(index + reverse) % numberOfPlayers].append(getNewCard())
    playersDecks[(index + reverse) % numberOfPlayers].append(getNewCard())
    currentPlayerIndex += 2 * reverse


# returns a new card from the card deck while removing it from the main deck
def getNewCard():
    global cardDeck
    card = cardDeck[0]
    cardDeck.pop(0)
    return card


main()

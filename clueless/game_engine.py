import random

from clueless.game_state import *


class CardDeck(object):
    """
    The CardDeck represents a deck of game cards
    """

    def __init__(self):

        #create a list of GameCard objects for the suspects
        self._suspects = [
            GameCard(item=item, item_type = SUSPECT) for item in SUSPECTS
        ]
        #create a list of GameCard objects for the weapons
        self._weapons = [
            GameCard(item=item, item_type = WEAPON) for item in WEAPONS
        ]
        #create a list of GameCard objects for the rooms
        self._rooms = [
            GameCard(item=item, item_type = ROOM) for item in ROOMS
        ]
        #create a full list of cards
        self._game_cards = self._suspects + self._weapons + self._rooms

        self._winning_cards = list()

    def draw_winning_cards(self):
        """
        randomly select winning suspect, weapon, and room and
        return a list of the winning cards
        """

        #select the winning cards by choosing a random integer for each index
        # in the list and selecting the game card at that index
        winning_suspect = self._suspects[
            random.choice(range(len(self._suspects)))]
        winning_weapon = self._weapons[
            random.choice(range(len(self._weapons)))]
        winning_room = self._rooms[
            random.choice(range(len(self._rooms)))]

        #assign the selected winners to a list
        self._winning_cards = [winning_suspect, winning_weapon, winning_room]

        #remove the winning cards from the deck
        self._game_cards = [
            game_card for game_card in self._game_cards
            if game_card not in self._winning_cards
        ]

        return self._winning_cards

    def get_shuffled_cards(self):
        """
        shuffles the game cards and returns the shuffled deck as a list
        """
        random.shuffle(self._game_cards)
        return self._game_cards

class Game(object):

    def __init__(self, players):
        self.players = players
        self.game_board = GameBoard()

        card_deck = CardDeck()

        #the case file contains the winning cards
        self.case_file = card_deck.draw_winning_cards()





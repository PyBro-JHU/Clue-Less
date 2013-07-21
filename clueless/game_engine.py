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

    def shuffle_cards(self):
        """
        shuffles the game cards
        """
        random.shuffle(self._game_cards)

    def deal_cards(self, num_hands):
        """
        deals the cards by taking the number of hands and return a list
        of lists that contain each seperate hand
        """
        return [self._game_cards[x::num_hands] for x in range(num_hands)]

class TurnController(object):
    def __init__(self, players):
        self.turn_list = list(players)
        self.current_player = self.turn_list[0]
        self.turn_status = AWAITING_MOVE

    def next_turn(self):
       turn_index = self.turn_list.index(self.current_player)
       if turn_index < (len(self.turn_list)-1):
           turn_index += 1
       else:
           turn_index = 0
       self.current_player = self.turn_list[turn_index]
       self.turn_status = AWAITING_MOVE


class Game(object):

    def __init__(self, players):
        self.players = players
        self.game_board = GameBoard()

        self.turn = TurnController(players)
        self.player_messages = list()

        card_deck = CardDeck()

        #poplate the case file with the winning cards
        self.case_file = card_deck.draw_winning_cards()

        #deal cards to the players
        num_players = len(self.players)
        hands = card_deck.deal_cards(num_players)
        for x in range(num_players):
            players[x].game_cards = hands[x]


    #Todo: Sgonzales complete player move operations
    def move_player(self, player, space_name):
        pass

    def _move_suspect(self):
        pass

    def _move_weapon(self):
        pass

    def player_suggestion(self, player, suspect, weapon, room):
        pass

    def player_suggestion_response(self, player, game_card):
        pass

    def process_accusation(self, player, suspect, weapon, room):
        pass

    def end_player_turn(self, player):
        pass

if __name__ == '__main__':
    card_deck = CardDeck()
    print len(card_deck._game_cards)
    #the case file contains the winning cards
    print card_deck.draw_winning_cards()
    print len(card_deck._game_cards)

    hands =  card_deck.deal_cards(4)

    print len(hands)
    for hand in hands:
        print hand

import random
from clueless.model import game_state
from clueless.server import errors


class CardDeck(object):
    """
    The CardDeck represents a deck of game cards
    """

    def __init__(self):

        #create a list of GameCard objects for the suspects
        self._suspects = [
            game_state.GameCard(item=item, item_type=game_state.SUSPECT)
            for item in game_state.SUSPECTS
        ]
        #create a list of GameCard objects for the weapons
        self._weapons = [
            game_state.GameCard(item=item, item_type=game_state.WEAPON)
            for item in game_state.WEAPONS
        ]
        #create a list of GameCard objects for the rooms
        self._rooms = [
            game_state.GameCard(item=item, item_type=game_state.ROOM)
            for item in game_state.ROOMS
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


class GameEngine(object):

    def __init__(self, players):
        self.players = players
        self.game = None

    def start_new_game(self):
        self.game = game_state.GameState(self.players)

        card_deck = CardDeck()

        #poplate the case file with the winning cards
        self.game.case_file = card_deck.draw_winning_cards()

        #deal cards to the players
        card_deck.shuffle_cards()
        num_players = len(self.players)
        hands = card_deck.deal_cards(num_players)
        for x in range(num_players):
            self.game.players[x].game_cards = hands[x]

    def load_game(self):
        pass

    def save_game(self):
        pass

    def handle_move(self, player_username, suspect, space_name):
        """
        Handle a players request to move their suspect to a new GameSpace
        and validates the components of the request.
        """

        #validate the move request
        self._validate_player(player_username)
        self._validate_player_turn(player_username)
        self._validate_suspect(suspect)
        self._validate_current_player_owns_suspect(suspect)
        self._validate_space(space_name)
        self._validate_space_available(space_name)

        #retreive the GameSpace objects and move the suspect
        current_space = self._get_suspect_current_space(suspect)
        new_space = self.game.game_board[space_name]
        self._move_suspect(suspect, current_space, new_space)

        #change the turn state
        self.game.turn_status = game_state.AWAITING_SUGGESTION

        #build notification message for the move, and add prepend to the
        #game_state's player_messages
        message = "{0} moved {1} moved into the {2}".format(
            player_username, suspect, new_space.name)
        self.game.player_messages.insert(0, message)

    def handle_suggestion(self, player, suspect, weapon, room):
        pass

    def handle_suggestion_response(self, player, game_card):
        pass

    def handle_accusation(self, player, suspect, weapon, room):
        pass

    def handle_end_turn(self, player):
        pass

    def _move_suspect(self, suspect, current_space, new_space):
        current_space.suspects.remove(suspect)
        new_space.suspects.append(suspect)

    def _move_weapon(self):
        pass

    def _next_turn(self):
        turn_index = self.game.turn_list.index(self.game.current_player)
        if turn_index < (len(self.game.turn_list)-1):
            turn_index += 1
        else:
            turn_index = 0
        self.game.current_player = self.game.turn_list[turn_index]
        self.game.turn_status = game_state.AWAITING_MOVE

    def _validate_player(self, username):
        """
        Validates that the username belongs to a valid player
        """
        for player in self.game.players:
            if username == player.username:
                return
        raise errors.PlayerInvalidException

    def _validate_player_turn(self, username):
        """
        validates that the username is that of the player whose turn it is
        """
        if username != self.game.current_player.username:
            raise errors.PlayerOperationOutOfTurnException

    def _validate_suspect(self, suspect):
        """
        Validates that a suspect is a valid suspect as
        defined in the game_state module
        """
        if suspect not in game_state.SUSPECTS:
            raise errors.SuspectInvalidException

    def _validate_current_player_owns_suspect(self, suspect):
        """
        Validates that the suspect belongs to the player whose turn it is
        """
        if suspect != self.game.current_player.suspect:
            raise errors.PlayerInvalidSuspectException

    def _validate_space(self, space_name):
        """
        Validates that a the space_name is a valid GameSpace that exists
        on the game_board
        """
        if not self.game.game_board[space_name]:
            raise errors.GameSpaceInvalidException

    def _validate_space_available(self, space_name):
        """
        Validates that a GameSpace is available for a suspect to move to
        """
        if not self.game.game_board["space_name"]:
            raise errors.GameSpaceInvalidException

    def _validate_connected_space(self, current_space, connected_space):
        """
        Validates that a GameSpace is in the list of
        connected_spaces of another GameSpace
        """
        if connected_space.name not in current_space.connected_spaces:
            raise errors.GameSpaceNotConnectedException

    def _get_suspect_current_space(self, suspect):
        """
        Returns the GameSpace object that the suspect currently occupies
        """
        for space in self.game.game_board:
            if suspect in self.game.game_board[space].suspects:
                return self.game.game_board[space]

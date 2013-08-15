import random
import uuid
from clueless import data
from clueless import log
from clueless.model import game_state
from clueless.server import errors

_LOG = log.get_logger(__name__)


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
        of lists that contain each separate hand
        """
        return [self._game_cards[x::num_hands] for x in range(num_hands)]


class GameEngine(object):

    def __init__(self):
        self.players = dict()
        self.game_id = None
        self.game = None
        self.db_handler = data.get_db_handler()

    def handle_register_player(self, username):
        """
        registers a new player with the GameEngine before the game starts
        """
        self.players[username] = game_state.Player(username)

    def handle_choose_suspect(self, username, suspect):
        """
        allows the player to choose their suspect before the game starts
        """
        self._validate_suspect(suspect)
        self.players[username].suspect = suspect

    def handle_start_new_game(self):
        """
        Starts a new game with all the registered players
        """
        self.game_id = str(uuid.uuid4())
        game_players = [self.players[key] for key in self.players]
        self.game = game_state.GameState(self.game_id, game_players)
        card_deck = CardDeck()

        #poplate the case file with the winning cards
        self.game.case_file = card_deck.draw_winning_cards()

        #deal cards to the players
        card_deck.shuffle_cards()
        num_players = len(self.players)
        hands = card_deck.deal_cards(num_players)
        for x in range(num_players):
            self.game.players[x].game_cards = hands[x]

        self.db_handler.insert_document(
            object_name='game', document=self.game.format())

        return self.game_id

    def destroy_game(self):
        """
        Destroys the current Game and deletes form datastore
        """
        self.game = None
        self.players = dict()
        self.db_handler.delete_document(
            object_name='game', query_filter={"game_id": self.game_id})

    def load_game(self, game_id):
        """
        Loads the specified GameState from the datastore
        """
        self.game_id = game_id
        game_dict = self.db_handler.get_document(
            object_name='game', query_filter={"game_id": self.game_id})

        game_builder = game_state.GameStateBuilder()
        self.game = game_builder.build_gamestate_from_dict(game_dict)

    def save_game(self):
        """
        Saves the GameState of the current game to the datastore
        """
        self.db_handler.update_document(
            object_name='game', document=self.game.format(),
            query_filter={"game_id": self.game_id}
        )

    def handle_move(self, player_username, suspect, space_name):
        """
        Handle a player's request to move their suspect to a new GameSpace
        and validates the components of the request.  A player can only move
        to a connected space, and the space must be available.
        """

        #validate the move request
        self._validate_player(player_username)
        self._validate_player_turn(player_username)
        self._validate_suspect(suspect)
        self._validate_current_player_owns_suspect(suspect)
        self._validate_space(space_name)
        self._validate_space_available(space_name)

        #retreive the GameSpace objects and
        current_space = self._get_suspect_current_space(suspect)
        new_space = self.game.game_board[space_name]
        self._validate_connected_space(current_space, new_space)

        #move the suspect
        self._move_suspect(suspect, new_space)

        #build notification message for the move, and prepend to the
        #game_state's player_messages
        message = "{0} moved {1} into the {2}".format(
            player_username, suspect, new_space.name)
        self._send_player_message(message)

        #change the turn state.  If the player has moved to a room
        #they must make a suggestion, otherwise they must make an
        # accusation or end their turn
        if isinstance(new_space, game_state.Room):
            self.game.turn_status = game_state.AWAITING_SUGGESTION
            message = "Player {0} must make a suggestion.".format(
                player_username)
            self._send_player_message(message)
        else:
            self.game.turn_status = game_state.AWAITING_ACCUSATION_OR_END_TURN
            message = "Player {0} must make an accusation " \
            "or end their turn.".format(
                player_username)
            self._send_player_message(message)

    def handle_suggestion(self, player_username, suspect, weapon, room):
        """
        Handle a player's suggestion.  A suggestion is made after a player
        enters a room
        """

        #validate the suggestion request
        self._validate_player(player_username)
        self._validate_player_turn(player_username)
        self._validate_suspect(suspect)
        self._validate_weapon(weapon)
        self._validate_room(room)
        self._validate_suggestion_turn_status()
        self._validate_suggestion_room(room)

        #When a suggestion is made bot the suspect and weapon must be
        #moved to the Room that the player is currently in
        suggestion_room = self.game.game_board[room]
        self._move_suspect(suspect, suggestion_room)
        self._move_weapon(weapon, suggestion_room)

        #create the suggestion:
        self.game.current_suggestion = game_state.Suggestion(
            suspect, weapon, room)

        message = "Player {0} suggests that the murder was committed by " \
            "{1} with the {2} in the {3}".format(
            player_username, suspect, weapon, room)
        self._send_player_message(message)

        #get the first player that can prove the suggestion false.
        # If one is found change the turn status to
        #AWAITING_SUGGESTION_RESPONSE, otherwise change the
        # turn status to AWAITING_ACCUSATION_OR_END_TURN
        response_player = self._get_suggestion_response_player()
        if response_player:
            self.game.suggestion_response_player = response_player
            self.game.turn_status = game_state.AWAITING_SUGGESTION_RESPONSE
            message = "Player {0} must prove the suggestion false.".format(
                response_player.username)
            self._send_player_message(message)
        else:
            self.game.turn_status = game_state.AWAITING_ACCUSATION_OR_END_TURN
            message = "There is no player that can prove the suggestion false."
            self._send_player_message(message)
            message = "Player {0} must make an accusation " \
                "or end their turn.".format(
                player_username)
            self._send_player_message(message)

    def handle_suggestion_response(self, player_username, gamecard_item):
        """
        Handles a suggestion response that will prove
        the current player's suggestion false
        """
        #validate request
        self._validate_player(player_username)
        self._validate_suggestion_response_player(player_username)
        self._validate_gamecard_item(gamecard_item)
        self._validate_suggestion_response_player_owns_card(gamecard_item)

        #show the current player the card
        self.game.current_player.card_items_seen.append(gamecard_item)

        message = "Player {0} has proven the suggestion false.".format(
            player_username)
        self._send_player_message(message)

        #update the turn status
        self.game.turn_status = game_state.AWAITING_ACCUSATION_OR_END_TURN
        message = "Player {0} must make an accusation " \
            "or end their turn.".format(
            self.game.current_player.username)
        self._send_player_message(message)

    def handle_accusation(self, player_username, suspect, weapon, room):
        """
        Handles player's accusation in attempt to win the game
        """
        self._validate_player(player_username)
        self._validate_player_turn(player_username)
        self._validate_suspect(suspect)
        self._validate_weapon(weapon)
        self._validate_room(room)

        message = "Player {0} has made the accusation that the murder was " \
            "committed by {1} with the {2} in the {3}".format(
            player_username, suspect, weapon, room)
        self._send_player_message(message)

        accusation_items = [suspect, weapon, room]
        winning_items = [card.item for card in self.game.case_file]

        #compare tha accusation to the winning items, if the accusation
        #is correct then end the game and mark the winner
        if set(accusation_items) == set(winning_items):
            self.game.game_active = False
            self.game.game_winner = self.game.current_player
            message = "Player {0} has won the game!!!".format(
                player_username)
            self._send_player_message(message)

        #if the accusation is false, remove the player form the turn list.
        #The player can still respond to suggestions but no longer has a turn,
        #and cannot win the game
        else:
            self.game.turn_list.remove(self.game.current_player)
            message = "Player {0} has made a false accusation and can no " \
                "longer win the game.  All future turns are forfeited, " \
                "but the player must make still prove suggestions false if " \
                "asked.".format(player_username)
            self._send_player_message(message)

    def handle_end_turn(self, player_username):
        """
        Handle a request made to end the current player's turn
        """

        #validate the request
        self._validate_player(player_username)
        self._validate_player_turn(player_username)
        self._validate_end_turn_status()

        message = "Player {0} has ended their turn.".format(
            player_username)
        self._send_player_message(message)

        #move the turn to the next player
        self._next_turn()

    def _move_suspect(self, suspect, new_space):
        """
        Move suspect from their current space to the selected space
        """
        current_space = self._get_suspect_current_space(suspect)
        current_space.suspects.remove(suspect)
        new_space.suspects.append(suspect)

    def _move_weapon(self, weapon, room):
        """
        Move weapon from its current room to the selected room
        """
        current_room = self._get_weapon_current_space(weapon)
        current_room.weapons.remove(weapon)
        room.weapons.append(weapon)

    def _next_turn(self):
        """
        update the game's current_player and turn status
        for the next player's turn
        """
        turn_index = self.game.turn_list.index(self.game.current_player)
        if turn_index < (len(self.game.turn_list)-1):
            turn_index += 1
        else:
            turn_index = 0
        self.game.current_player = self.game.turn_list[turn_index]
        self.game.turn_status = game_state.AWAITING_MOVE

        message = "Player {0} has begun their turn, now awaiting move.".format(
            self.game.current_player.username)
        self._send_player_message(message)

        #check if the new player has any moves available by
        #checking the connected_spaces
        current_space = self._get_suspect_current_space(
            self.game.current_player.suspect)

        move_available = False

        for space in current_space.connected_spaces:
            if self.game.game_board[space].is_available():
                move_available = True

        #If player has no available spaces to move to, they must make an
        #accusation or end their turn
        if not move_available:
            _LOG.exception("not available")
            self.turn_status = game_state.AWAITING_ACCUSATION_OR_END_TURN
            message = "Player {0} has no available spaces to move to. {1}."\
                .format(
                self.game.current_player.username,
                game_state.AWAITING_ACCUSATION_OR_END_TURN)
            self._send_player_message(message)

    def _get_next_player_index(self):
        """
        Get the index of the nex player in the turn list
        """
        turn_index = self.game.turn_list.index(self.game.current_player)
        if turn_index < (len(self.game.turn_list)-1):
            turn_index += 1
        else:
            turn_index = 0

        return turn_index

    def _get_suspect_current_space(self, suspect):
        """
        Returns the GameSpace object that the suspect currently occupies
        """
        for space in self.game.game_board:
            if suspect in self.game.game_board[space].suspects:
                return self.game.game_board[space]

    def _get_weapon_current_space(self, weapon):
        """
        Returns the GameSpace object that the weapon is currently in
        """
        game_board = self.game.game_board
        rooms = [
            room for room in [game_board[space]
            for space in game_board
            if isinstance(game_board[space], game_state.Room)]
        ]

        for room in rooms:

            if weapon in room.weapons:
                return room

    def _get_suggestion_response_player(self):
        """
        Returns the player that must respond to the suggestion, otherwise None.
        Suggestions are responded to by the next player in turn if they have
        a card that proves the suggestion false.  If the next player can not
        prove the suggestion false it moves to the next player until one is
        found.  If no players are found, the method returns None.
        """
        #create a list of all players except the player whose turn it is
        suggestion_players = [
            player for player in self.game.players
            if player is not self.game.current_player
        ]

        #create a list of the items in the suggestion
        suggestion_items = [
            self.game.current_suggestion.suspect,
            self.game.current_suggestion.weapon,
            self.game.current_suggestion.room
        ]

        #iterate through the list of the other players
        for player in suggestion_players:
            #create a list of the items in the player's game_cards list
            player_card_items = [
                card.item for card in player.game_cards
            ]
            #create a set intersection and test it as a conditional
            #to determine if the player has any of the cards in the suggestion.
            #if there is a match, return the player.
            if list(set(suggestion_items) & set(player_card_items)):
                return player

        #If none of the players had game_cards that can prove the
        # suggestion false, return None
        return None

    def _send_player_message(self, message):
        """
        Updates the list used to provide notifications to players by
        prepending the newest message to the list
        """
        self.game.player_messages.insert(0, message)

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

    def _validate_suggestion_response_player(self, username):
        """
        validates that the username is that of the player who is selected
        to prove the current suggestion false
        """
        if username != self.game.suggestion_response_player.username:
            raise errors.SuggestionResponsePlayerInvalidException

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
        if not self.game.game_board[space_name]:
            raise errors.GameSpaceInvalidException

    def _validate_connected_space(self, current_space, connected_space):
        """
        Validates that a GameSpace is in the list of
        connected_spaces of another GameSpace
        """
        if connected_space.name not in current_space.connected_spaces:
            raise errors.GameSpaceNotConnectedException

    def _validate_weapon(self, weapon):
        """
        Validates that a weapon is a valid weapon as
        defined in the game_state module
        """
        if weapon not in game_state.WEAPONS:
            raise errors.WeaponInvalidException

    def _validate_room(self, room):
        """
        Validates that a room is a valid room as
        defined in the game_state module
        """
        if room not in game_state.ROOMS:
            raise errors.RoomInvalidException

    def _validate_suggestion_turn_status(self):
        """
        Validate that the suggestion is being made only when when
        the turn_status is AWAITING_SUGGESTION
        """
        if self.game.turn_status != game_state.AWAITING_SUGGESTION:
            raise errors.SuggestionTurnStatusException

    def _validate_suggestion_room(self, room):
        """
        Validates that the player is currently in the Room that
        is used in the suggestion
        """
        suspect = self.game.current_player.suspect
        if suspect not in self.game.game_board[room].suspects:
            raise errors.SuggestionInvalidRoomException

    def _validate_gamecard_item(self, gamecard_item):
        """
        Validates that the gamecard item is a valid game_card
        """
        valid_items = game_state.SUSPECTS
        valid_items += game_state.WEAPONS
        valid_items += game_state.ROOMS

        if gamecard_item not in valid_items:
            raise errors.GameCardItemInvalidException

    def _validate_suggestion_response_player_owns_card(self, gamecard_item):
        cards = self.game.suggestion_response_player.game_cards
        player_items = [
            card.item for card in cards]
        if gamecard_item not in player_items:
            raise errors.PlayerInvalidGameCardException

    def _validate_end_turn_status(self):
        if self.game.turn_status != game_state.AWAITING_ACCUSATION_OR_END_TURN:
            raise errors.EndTurnStatusException

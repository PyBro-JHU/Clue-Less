"""
This module is a functional test of the game_server and game_client
interactions.  a game server is spun up in a seperate process space and bound
to localhost on port 5000.  The game client is then used to interact with
the game server.
"""

import unittest
from multiprocessing.process import Process
from clueless.client import errors
from clueless.client.game_play import GameClient
from clueless import log
from clueless.model import game_state
from clueless.server.app import start_server
import time

_LOG = log.get_logger(__name__)


class WhenFunctionalTestingGameClient(unittest.TestCase):

    def setUp(self):
        #setup game server to run on a seperate process
        self.game_server = Process(target=start_server)
        self.game_server.start()

        #create the game client
        self.client = GameClient(host="127.0.0.1", port="5000")

        self.player_one = "Arthur"
        self.player_one_suspect = game_state.PEACOCK
        self.player_two = "Steven"
        self.player_two_suspect = game_state.PLUM

    def test_game_client(self):
        try:
            #give the game server process a chance to start
            time.sleep(3)

            #test registering players and choosing suspects
            self.client.register_player(self.player_one)
            self.client.choose_suspect(
                self.player_one, self.player_one_suspect)
            self.client.register_player(
                self.player_two)
            self.client.choose_suspect(
                self.player_two, self.player_two_suspect)

            #retreive the registered players with the client and validate the
            #return values
            players = self.client.get_players()
            for player in players:
                self.assertIsInstance(player, game_state.Player)
            self.assertTrue(
                self.player_one in [player.username
                for player in players])
            self.assertTrue(
                self.player_two in [player.username
                for player in players])
            self.assertTrue(
                self.player_one_suspect in [player.suspect
                for player in players])
            self.assertTrue(
                self.player_two_suspect in [player.suspect
                for player in players])

            #start a new game with the client and validate a GameState object
            #is returned
            game = self.client.start_new_game()
            self.assertTrue(game, game_state.GameState)

            game = self.client.get_game_state(game.game_id)
            self.assertTrue(game, game_state.GameState)

            #move player 1  from start space to hallway
            player = game.current_player
            player_1_current_space = game.game_board[player.suspect]
            move_space = player_1_current_space.connected_spaces[0]
            game = self.client.move_player(
                player.username, player.suspect, move_space)
            self.assertEqual(
                game.turn_status, game_state.AWAITING_ACCUSATION_OR_END_TURN)
            game = self.client.end_turn(player.username)
            player_1_current_space = game.game_board[move_space]
            self.assertEqual(game.turn_status, game_state.AWAITING_MOVE)

            #move player 2  from start space to hallway
            player = game.current_player
            player_2_current_space = game.game_board[player.suspect]
            move_space = player_2_current_space.connected_spaces[0]
            game = self.client.move_player(
                player.username, player.suspect, move_space)
            self.assertEqual(
                game.turn_status, game_state.AWAITING_ACCUSATION_OR_END_TURN)
            game = self.client.end_turn(player.username)
            player_2_current_space = game.game_board[move_space]
            self.assertEqual(game.turn_status, game_state.AWAITING_MOVE)

            #move player 1  from hallway to room
            player = game.current_player
            move_space = player_1_current_space.connected_spaces[0]
            game = self.client.move_player(
                player.username, player.suspect, move_space)
            self.assertEqual(
                game.turn_status, game_state.AWAITING_SUGGESTION)
            #make suggestion based on room player is currently in
            game = self.client.make_suggestion(
                player.username, game_state.MUSTARD,
                game_state.REVOLVER,
                move_space
            )

            if game.suggestion_response_player:
                with self.assertRaises(errors.GameClientException):
                    game = self.client.move_player(
                        player.username, player.suspect, move_space)
                self.assertEqual(
                    game.turn_status, game_state.AWAITING_SUGGESTION_RESPONSE)

                response_player = game.suggestion_response_player
                suggestion = game.current_suggestion
                gamecard_item = list(
                    {suggestion.weapon, suggestion.room, suggestion.suspect}
                    &
                    set(card.item for card in response_player.game_cards))[0]
                game = self.client.make_suggestion_response(
                    response_player.username, gamecard_item)

            suspect = [
                card.item for card in game.case_file
                if card.type == game_state.SUSPECT
            ][0]
            weapon = [
                card.item for card in game.case_file
                if card.type == game_state.WEAPON
            ][0]
            room = [
                card.item for card in game.case_file
                if card.type == game_state.ROOM
            ][0]

            game = self.client.make_accusation(
                player.username, suspect, weapon, room)

            for message in  game.player_messages:
                print message

            self.client.destroy_game(game.game_id)

        finally:
            self.game_server.terminate()

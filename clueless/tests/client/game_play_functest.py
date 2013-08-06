"""
This module is a functional test of the game_server and game_client
interactions.  a game server is spun up in a seperate process space and bound
to localhost on port 5000.  The game client is then used to interact with
the game server.
"""

import unittest
from multiprocessing.process import Process
from clueless.client.game_play import GameClient
from clueless.model import game_state
from clueless.server.app import start_server
import time


class WhenFunctionalTestingGameClient(unittest.TestCase):

    def setUp(self):
        #setup game server to run on a seperate process
        self.game_server = Process(target=start_server)
        self.game_server.start()

        #create the game client
        self.client = GameClient(host="127.0.0.1", port="5000")

        self.player_one = "player1"
        self.player_one_suspect = game_state.PEACOCK
        self.player_two = "player2"
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
                self.player_one in player.username
                for player in players)
            self.assertTrue(
                self.player_two in player.username
                for player in players)
            self.assertTrue(
                self.player_one_suspect in player.suspect
                for player in players)
            self.assertTrue(
                self.player_two_suspect in player.suspect
                for player in players)

            #start a new game with the client and validate a GameState object
            #is returned
            game = self.client.start_new_game()
            self.assertTrue(game, game_state.GameState)

            game = self.client.get_game_state(game.game_id)
            self.assertTrue(game, game_state.GameState)

            self.client.destroy_game(game.game_id)

        finally:
            self.game_server.terminate()

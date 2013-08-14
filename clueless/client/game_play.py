import httplib
import json
import requests

from clueless.client import errors
from clueless.model import game_state


class GameClient(object):
    """
    The GameClient class allows a remote client to interact with the
    GameServer API by wrapping the functional of the restful API calls.
    """

    def __init__(self, host, port="80"):
        self.base_url = "http://{host}:{port}".format(host=host, port=port)

    def register_player(self, username):
        """
        Register a new player for upcoming game
        """
        url = "{base_url}/players".format(base_url=self.base_url)

        headers = {'Content-Type': "application/json"}
        payload = json.dumps({"username": username})

        response = requests.post(url=url, data=payload, headers=headers)

        if response.status_code != httplib.CREATED:
            raise errors.GameClientException(response.text)

    def get_players(self):
        """
        Get a list of all registered players
        """
        url = "{base_url}/players".format(base_url=self.base_url)
        response = requests.get(url=url)

        if response.status_code != httplib.OK:
            raise errors.GameClientException(response.text)

        body = response.json()
        return [
            game_state.Player(**player_dict)
            for player_dict in body["players"]
        ]

    def get_player(self, username):
        """
        Get a specified player
        """
        url = "{base_url}/players/{username}".format(
            base_url=self.base_url, username=username)

        response = requests.get(url=url)

        if response.status_code != httplib.OK:
            raise errors.GameClientException(response.text)

        body = response.json()

        return game_state.Player(**body["player"])

    def choose_suspect(self, username, suspect):
        """
        Register a new player for upcoming game
        """
        url = "{base_url}/players/{username}".format(
            base_url=self.base_url, username=username)
        headers = {'Content-Type': "application/json"}
        payload = json.dumps({"suspect": suspect})

        response = requests.put(url=url, data=payload, headers=headers)

        if response.status_code != httplib.OK:
            raise errors.GameClientException(response.text)

    def start_new_game(self):
        """
        Creates a new game and returns a GameState object
        """
        url = "{base_url}/games".format(base_url=self.base_url)
        response = requests.post(url=url)

        if response.status_code != httplib.CREATED:
            raise errors.GameClientException(response.text)

        body = response.json()

        game_dict = body["game_state"]
        builder = game_state.GameStateBuilder()
        game = builder.build_gamestate_from_dict(game_dict)
        return game

    def get_game_state(self, game_id):
        """
        Gets the current GameState object. Ideal for polling state
        """
        url = "{base_url}/games/game_id".format(
            base_url=self.base_url, game_id=game_id)
        response = requests.get(url=url)

        if response.status_code != httplib.OK:
            raise errors.GameClientException(response.text)

        body = response.json()
        game_dict = body["game_state"]

        builder = game_state.GameStateBuilder()
        game = builder.build_gamestate_from_dict(game_dict)
        return game

    def destroy_game(self, game_id):
        """
        Destroy the current game
        """
        url = "{base_url}/games/game_id".format(
            base_url=self.base_url, game_id=game_id)
        response = requests.delete(url=url)

        if response.status_code != httplib.OK:
            raise errors.GameClientException(response.text)

    def move_player(self, username, suspect, space_name):
        """
        Register a new player for upcoming game
        """
        url = "{base_url}/moveplayer".format(
            base_url=self.base_url)
        headers = {'Content-Type': "application/json"}
        payload = json.dumps(
            {
                "username": username,
                "suspect": suspect,
                "space_name": space_name
            }
        )

        response = requests.post(url=url, data=payload, headers=headers)

        if response.status_code != httplib.OK:
            raise errors.GameClientException(response.text)

        body = response.json()
        game_dict = body["game_state"]

        builder = game_state.GameStateBuilder()
        game = builder.build_gamestate_from_dict(game_dict)
        return game

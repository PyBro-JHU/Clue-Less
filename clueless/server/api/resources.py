import httplib
import json

from flask.ext import restful
from flask import request, make_response

from clueless.server.game_engine import GameEngine


engine = GameEngine()


class PlayersResource(restful.Resource):

    def post(self):
        """
        Register a new player with the GameEngine
        """
        username = request.json["username"]
        engine.handle_register_player(username)

        response = make_response()
        response.headers["location"] = "/players/{username}".format(
            username=username)
        response.status_code = httplib.CREATED

        return response

    def get(self):
        """
        Gets a list of all registered players
        """
        players = [
            engine.players[key].format() for key in engine.players
        ]
        return {"players": players}


class PlayerResource(restful.Resource):

    def get(self, username):
        """
        Get returns data for the requested player
        """

        return {"player": engine.players[username].format()}

    def put(self, username):
        """
        Put method assigns a suspect for the registered user
        """
        engine.handle_choose_suspect(username, request.json["suspect"])

        response = make_response()
        response.status_code = httplib.OK

        return response


class GamesResource(restful.Resource):

    def post(self):
        """
        Post starts a new game with the registered players
        """
        game_id = engine.handle_start_new_game()

        response = make_response(
            json.dumps({"game_state": engine.game.format()}))
        response.headers["location"] = "/games/{game_id}".format(
            game_id=game_id)
        response.status_code = httplib.CREATED
        return response


class GameResource(restful.Resource):

    def get(self, game_id):
        """
        Get returns the requested game_state
        """
        return {"game_state": engine.game.format()}

    def delete(self, game_id):
        """
        Delete destroys the current game
        """
        engine.destroy_game()
        response = make_response()
        response.status_code = httplib.OK
        return response

class MovePlayerResource(restful.Resource):

    def post(self):
        """
        Put method assigns a suspect for the registered user
        """
        request_data = request.json
        engine.handle_move(
            request_data['username'],
            request_data['suspect'],
            request_data['space_name']
        )
        response = make_response(
            json.dumps({"game_state": engine.game.format()}))
        response.status_code = httplib.OK
        return response
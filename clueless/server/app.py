from flask import Flask
from flask.ext import restful

from clueless import log
from clueless.server.api import resources

_LOG = log.get_logger(__name__)


def start_server():

    _LOG.info('Clueless server starting..')

    app = Flask(__name__)
    api = restful.Api(app)

    api.add_resource(resources.PlayersResource, '/players')
    api.add_resource(resources.PlayerResource, '/players/<string:username>')
    api.add_resource(resources.GamesResource, '/games')
    api.add_resource(resources.GameResource, '/games/<string:game_id>')
    api.add_resource(resources.MovePlayerResource, '/moveplayer')
    api.add_resource(resources.SuggestionResource, '/suggestion')
    api.add_resource(
        resources.SuggestionResponseResource, '/suggestionresponse')
    api.add_resource(resources.AccusationResource, '/accusation')
    api.add_resource(resources.EndTurnResource, '/endturn')

    app.run(host="0.0.0.0",debug=True)


if __name__ == '__main__':
    start_server()

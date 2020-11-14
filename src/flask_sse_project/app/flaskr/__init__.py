from .controller import Controller
from .badminton import Badminton
from .gameFactory import GameFactory

from flask import Flask

from flask_cors import CORS
from flask_sse import sse


def create_controller(sse):
    """
    Factory Method, which creates a new controller with the given sse object

    Defines a blueprint route to update the SSE Stream with a new counter under /updateCounter

    Parameters:

        sse (ServerSentEventsBlueprint): The Object which will be used to publish events
    """
    con = Controller('con', __name__, sse)

    @con.route('/updateCounter')
    def test():
        con.updateStream1()
        return 'Counter updated'

    return(con)

def create_app(test_config=None):
    """
    Factory Method, which creates a new flask app.

    Initiates CORS to be used. Registers the ServerSentEventsBlueprint and Controller.

    Parameters:

        test_config (Config): If a test config is provided, uses it for the app.
            Otherwise the config.DevConfig Object is used as the config.
    """
    app = Flask(__name__)
    CORS(app)

    if test_config is None:
        app.config.from_object('config.DevConfig')
    else:
        app.config.from_mapping(test_config)

    with app.app_context():
        app.register_blueprint(sse, url_prefix='/events')
        app.register_blueprint(create_controller(sse), url_prefix='/con')

    return app
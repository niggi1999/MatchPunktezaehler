from .controller import Controller
from .badminton import Badminton, ServePosition
from .gameFactory import GameFactory
from .tableModel import TableConfig, TableTestConfig, TableProdConfig, TableModel, TableFactory
from .bluetooth_controller import BluetoothController

from flask import Flask

from flask_cors import CORS
from flask_sse import sse


def create_controller(sse, testBluetoothController = BluetoothController()):
    """
    Factory Method, which creates a new controller with the given sse object

    Defines a blueprint route to update the SSE Stream with a new counter under /update

    Parameters:

        sse (ServerSentEventsBlueprint): The Object which will be used to publish events
    """
    con = Controller('con', __name__, sse, testBluetoothController)

    @con.route('/updateInitSite')
    def updateInitSite():
        con.updateInitSite()
        return 'Init site updated'

    @con.route('/updatePlayerMenuSite')
    def updatePlayerMenuSite():
        con.updatePlayerMenuSite()
        return 'PlayerMenu site updated'

    @con.route('/updateColorMenuSite')
    def updateColorMenuSite():
        con.updateColorMenuSite()
        return 'Name Menu site updated'

    @con.route('/updateGameMenuSite')
    def updateGameMenuSite():
        con.updateGameMenuSite()
        return 'Game Menu site updated'

    @con.route('/updateGameSite')
    def updateGameSite():
        con.updateGameSite()
        return 'Game site updated'

    

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
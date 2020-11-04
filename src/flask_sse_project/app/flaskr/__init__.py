from .controller import Controller
from .badminton import Badminton
from .gameFactory import GameFactory

from flask import Flask

from flask_cors import CORS
from flask_sse import sse


def construct_controller(sse):
    con = Controller('con', __name__, sse)

    @con.route('/test')
    def test():
        con.updateStream1()
        return 'Works'

    return(con)

def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)

    if test_config is None:
        app.config.from_object('config.DevConfig')
    else:
        app.config.from_mapping(test_config)

    with app.app_context():
        app.register_blueprint(sse, url_prefix='/events')
        app.register_blueprint(construct_controller(sse), url_prefix='/con')

    return app
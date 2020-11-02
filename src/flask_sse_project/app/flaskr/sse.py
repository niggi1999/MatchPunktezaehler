from flask import Flask, render_template
import random # Only needed for example
import time

from flask_sse import sse
from flask_cors import CORS

from controller import Controller #relativ

def get_data():
    data = {'counterTeam1': random.randrange(1, 100), 'counterTeam2': random.randrange(1, 100)}
    return data

#def createApp():
app = Flask(__name__)
CORS(app)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/events')

@app.route('/', defaults = {'path' : ''})
@app.route('/<path:path>')                  #Catch all
def index(path):
    return render_template("index.html")

@app.route('/hello')
def publish_hello():
    sse.publish(get_data(), type='updateData')
    return "Message sent!"


@app.route('/test')
def publishTest():
    sse.publish({"message": "Hello!"}, type='greeting')
    return "Message sent!"

if __name__ == '__main__':
    #app.run(debug = True)
    '''
    time.sleep(8)
    print(flask.current_app)
    with app.app_context():
        controller = Controller()
    '''
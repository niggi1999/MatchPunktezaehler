from flask import Flask, render_template
from flask_sse import sse
from flask_cors import CORS
import random # Onlx needed for example

def get_data():
    data = {'counterTeam1': random.randrange(1, 100), 'counterTeam2': random.randrange(1, 100)}
    return data

app = Flask(__name__)
CORS(app)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/events')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/hello')
def publish_hello():
    sse.publish(get_data(), type='updateData')
    return "Message sent!"








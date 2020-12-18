#!/bin/bash
sleep 10
cd /home/pi/MatchPunktezaehler/src
cd flask_sse_project/frontend
/usr/bin/screen -d -m sudo  serve -s -n build -l 3000 &
cd ..
cd app
source mpz/bin/activate
/usr/bin/screen -d -m sudo gunicorn "flaskr:create_app()" --worker-class gevent --bind 0.0.0.0:5000
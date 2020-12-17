#!/bin/bash
sleep 10
cd /home/pi/Matchcounter/src
touch starttest
cd flask_sse_project/app
source mpz/bin/activate
gunicorn "flaskr:create_app()" --worker-class gevent --bind 0.0.0.0:5000 &
cd ..
cd frontend
serve -s -n build -l 3000
#!/bin/bash
sleep 10
cd MatchPunktezaehler/
source mpz/bin/activate
cd src/flask_sse_project/app
gunicorn "flaskr:create_app()" --worker-class gevent --bind 0.0.0.0:5000 &
cd ..
cd frontend
npm start
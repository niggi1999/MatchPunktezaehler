Einmal ausführen:
    sudo apt install python3
    sudo apt install python3-pip
    sudo apt install python3-venv
    sudo apt install npm
    In Ordner über App oder höher
        python3 -m venv mpz
    in frontend
    	npm install


Immer ausführen:
    source mpz/bin/activate
    pip3 install -r requirements.txt
in app
    export FLASK_APP=sse.py
    gunicorn sse:app --worker-class gevent --bind 127.0.0.1:5000
in zweitem Terminal
    redis-server
drittes Terminal
	npm start


    export FLASK_APP=flaskr      Nur mit development server nötig(nicht mit gunicorn)
    Proxy Gunicorn from Webserver
    gunicorn "flaskr:create_app()" --worker-class gevent --bind 127.0.0.1:5000

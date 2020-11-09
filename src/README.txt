Einmal ausführen:
    sudo apt install python3
    sudo apt install python3-pip
    sudo apt install python3-venv
    sudo apt install npm
    In Ordner app
        Datei .env.example in .env umbenennen
        python3 -m venv mpz
        source mpz/bin/activate
        pip3 install -r requirements.txt
    in Ordner frontend
    	npm install
	npm install bootstrap react-bootstrap


Immer ausführen:
    erstes Terminal
        in app directory
            source mpz/bin/activate
            gunicorn "flaskr:create_app()" --worker-class gevent --bind 127.0.0.1:5000
    zweites Terminal
        redis-server
    drittes Terminal
        In frontend directory
	        npm start (dauert lange)

Browser:
    http://localhost:3000/






Raspberry:
    Static IP: 192.168.178.71
    In app:
        __init__.py
            app.config.from_object('config.DevConfig')
            ersetzen durch
                app.config.from_object('config.ProdConfig')

    Erstes Terminal:
        source mpz/bin/activate
        in app directory
            gunicorn "flaskr:create_app()" --worker-class gevent --bind 0.0.0.0:5000

    zweites Terminal
        In frontend directory
    	    npm start



    Auf Raspberry redis-server mit sudo apt-get install redis-server installieren

    export FLASK_APP=flaskr      Nur mit development server nötig(nicht mit gunicorn)
    Proxy Gunicorn from Webserver
    gunicorn "flaskr:create_app()" --worker-class gevent --bind 127.0.0.1:5000
    gunicorn "flaskr:create_app()" --worker-class gevent --bind 127.0.0.1:5000 --error-logfile gunicornLog.txt

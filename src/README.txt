sudo apt install python3
sudo apt install python3-pip
sudo apt install python3-venv
sudo apt install npm
In Ordner über App oder höher
    python3 -m venv mpz
    source mpz/bin/activate
    pip install -r requirements.txt 
in app
    export FLASK_APP=sse.py
    gunicorn sse:app --worker-class gevent --bind 127.0.0.1:5000
in zweitem Terminal
    redis-server
    
in frontend
	npm install
	npm start

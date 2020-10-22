sudo apt install python3
sudo apt install python3-pip
sudo apt install python3-venv
In Ordner über App oder höher
    python3 -m venv mpz
    source mpz/bin/activate
    pip install -r requirements.txt 
in app
    export FLASK_APP=sse.py
    gunicorn sse:app --worker-class gevent --bind 127.0.0.1:8000
in zweitem Terminal
    redis-server
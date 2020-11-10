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


Ad hoc Access Point auf Ubuntu Raspberrry:

DHCPD:
sudo apt install isc-dhcp-server

sudo nano /etc/default/isc-dhcp-server

INTERFACES="wlan0"

sudo nano /etc/dhcp/dhcpd.conf

default-lease-time 600;
max-lease-time 7200;

ddns-update-style none;

#option domain-name "example.org";
#option domain-name-servers ns1.example.org, ns2.example.org;

authoritative;

subnet 192.168.4.0 netmask 255.255.255.0 {
    range 192.168.4.10 192.168.4.254;
    option broadcast-address 192.168.4.255;
    option routers 192.168.4.1;
    default-lease-time 600;
    max-lease-time 7200;
 #   option domain-name "local";
#    option domain-name-servers 8.8.8.8, 8.8.4.4;
}

HOSTAPD:
sudo apt install hostapd

sudo nano /etc/default/hostapd

kontrollieren:
DAEMON_CONF=/etc/hostapd.conf

sudo nano /etc/hostapd.conf

interface=wlan0
driver=nl80211
ssid=Matchcounter
hw_mode=g
channel=6
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=123456789
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP

Interfaces:
Wechsel auf interfaces datei :
https://linuxconfig.org/how-to-switch-back-networking-to-etc-network-interfaces-on-ubuntu-20-04-focal-fossa-linux
$ sudo apt update
$ sudo apt install ifupdown net-tools

Vermutlich nicht nötig($ sudo dpkg -P cloud-init
$ sudo rm -fr /etc/cloud/)

$ sudo systemctl disable --now systemd-resolved

Interfaces konfigurieren:

sudo nano /etc/network/interfaces

auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
  address 192.168.178.72
  netmask 255.255.255.0
  network 192.168.178.0
  broadcast 192.168.178.255
  gateway 192.168.178.1
  dns-nameservers 8.8.8.8


allow-hotplug wlan0

iface wlan0 inet static
    address 192.168.4.1
    netmask 255.255.255.0

AP aktivieren:
sudo systemctl start isc-dhcp-server
sudo systemctl start hostapd
sudo reboot

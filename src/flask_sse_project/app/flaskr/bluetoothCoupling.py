import re
import subprocess
import sys
import pexpect
import time

def couple():
    subprocess.check_output("rfkill unblock bluetooth", shell = True)
    child = pexpect.spawn("bluetoothctl", echo= False)

    child.send("default-agent\n")
    child.send("power on\n")


    child.send("devices\n")
    isfailed = child.expect(["bluetooth", pexpect.EOF])
    out = child.buffer
    outl = out.decode("utf-8").split("\n")
    device_mac_name = re.compile("([0-9,:,A-F]{17}\sSmartRemote)")
    device_mac = re.compile("([0-9,:,A-F]{17})")
    for line in outl:
        device_names = device_mac_name.findall(line)
        for dev in device_names:
            if dev != "":
                mac = device_mac.findall(dev)[0]
                child.send("pair " + mac + "\n")
                time.sleep(2)
                child.send("trust " + mac + "\n")
                time.sleep(2)
import evdev

class BluetoothController:
    def __init__(self):
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        self.device = None
        for device in devices:
            if (device.name == "SmartRemote Consumer Control"):
                print("Device found")
                self.device = evdev.InputDevice(device.path)

    def readLoop(self):
        if(self.device):
            print(self.device)
            for event in self.device.read_loop():
                if (event.type == evdev.ecodes.EV_KEY):
                    """ print(evdev.categorize(event).scancode) # Ist Eventcode
                    print(evdev.categorize(event).keycode)  # Ist übersetzter Eventcode
                    print(event.type) """
                    scancode = evdev.categorize(event).scancode
                    if (evdev.categorize(event).keystate == 0):
                        if(scancode == 115):
                            print("up")
                        elif(scancode == 114):
                            print("down")
                        elif(scancode == 163):
                            print("right")
                        elif(scancode == 165):
                            print("left")
                        elif(scancode == 164):
                            print("ok")
                        else:
                            print("unknown")
        else:
            print("No Device found")

if __name__ == "__main__":
    bluetoothController = BluetoothController()
    bluetoothController.readLoop()

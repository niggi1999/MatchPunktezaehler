import evdev
import asyncio

class BluetoothController:
    def __init__(self):
        self.device = None
        self.findDevice()

    def findDevice(self):
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for device in devices:
            if (device.name == "SmartRemote Consumer Control"):
                print("Device found")
                self.device = evdev.InputDevice(device.path)
                print(device.path)

    '''
    def readLoop(self):
        if(self.device):
            print(self.device)
            for event in self.device.read_loop():
                if (event.type == evdev.ecodes.EV_KEY):
                    """ print(evdev.categorize(event).scancode) # Ist Eventcode
                    print(evdev.categorize(event).keycode)  # Ist übersetzter Eventcode
                    print(event.type) """
                    if (evdev.categorize(event).keystate == 0):
                        scancode = evdev.categorize(event).scancode
                        if(scancode == 115):
                            print("up")
                            return 'redo'
                        elif(scancode == 114):
                            print("down")
                            return 'undo'
                        elif(scancode == 163):
                            print("right")
                            return 'counter2'
                        elif(scancode == 165):
                            print("left")
                            return 'counter1'
                        elif(scancode == 164):
                            print("ok")
                        else:
                            print("unknown")
        else:
            print("No Device found")
    '''

    async def readBluetooth(self):
        if(self.device):
            #print(self.device)
            try:
                async for event in self.device.async_read_loop():  #device disconnect führt zu Fehler
                        if (evdev.ecodes.EV_KEY == event.type):
                            if (evdev.categorize(event).keystate == 0):
                                scancode = evdev.categorize(event).scancode
                                #print(scancode)
                                if(scancode == 115):
                                    print("up")
                                    return 'up'
                                elif(scancode == 114):
                                    print("down")
                                    return 'down'
                                elif(scancode == 163):
                                    print("right")
                                    return 'right'
                                elif(scancode == 165):
                                    print("left")
                                    return 'left'
                                elif(scancode == 164):
                                    print("ok")
                                else:
                                    print("unknown")
            except OSError as error:
                if (19 == error.errno):
                    self.device = None
                    print("device disconnected")
                    return
        else:
            print("No Device found")
            await asyncio.sleep(2)
            self.findDevice()


if __name__ == "__main__":
    bluetoothController = BluetoothController()
    #bluetoothController.readLoop()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bluetoothController.readAsync())
import evdev
import asyncio

class BluetoothController:
    def __init__(self):
        self.device = None
        self.findDevice()

    async def findDevice(self):
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
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

    async def readAsync(self):
        if(self.device):
            print(self.device)
            async for event in self.device.async_read_loop():
                    if (evdev.ecodes.EV_KEY == event.type):
                        if (evdev.categorize(event).keystate == 0):
                            scancode = evdev.categorize(event).scancode
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
            await asyncio.sleep(2)
            await self.findDevice()


if __name__ == "__main__":
    bluetoothController = BluetoothController()
    #bluetoothController.readLoop()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bluetoothController.readAsync())
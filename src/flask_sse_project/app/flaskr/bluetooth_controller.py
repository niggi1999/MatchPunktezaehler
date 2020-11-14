import evdev
import asyncio

class BluetoothController:
    """
    A class to create an Interface to a "SmartRemote Consumer Control" device

    Attributes:

        device (evdev.InputDevice): The connected Device, None if no device is connected

    Methods:

        findDevice(): Searches connected devices for "SmartRemote Consumer Control" and puts it in self.device
        readBluetooth(): Waits for events from the device and returns the pressed button
    """

    def __init__(self):
        """ Tries to find a device, if not successful device == None"""
        self.device = None
        self.findDevice()

    def findDevice(self):
        """
        Searches connected devices for "SmartRemote Consumer Control" and puts it in self.device

        If a device is found, prints "Device found" and the path to the device
        """
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for device in devices:
            if ("SmartRemote Consumer Control" == device.name):
                self.device = evdev.InputDevice(device.path)
                print("Device found")
                print(device.path)

    async def readBluetooth(self):
        """
        Waits for events from the device and returns the pressed button

        If no device is connected, then it sleeps for 2 seconds and after that tries to find a device

        If the device is disconnected while waiting for events, it prints:
        "device disconnected, trying to reconnect".
        If the reconnect succeeds prints: "reconnected"
        If the reconnect fails prints: "Reconnect failed"
        Returns regardless of the reconnects outcome

        Returns:

            buttonName (str): Name of the pressed button. Could be "up", "down", "right",
                "left" or "ok" if a valid Button was pressed. If no valid Button was pressed is "unknown"

            None: If there was a probleme with the device Connection
        """
        if(self.device):
            #print(self.device)
            try:
                async for event in self.device.async_read_loop():
                        if (evdev.ecodes.EV_KEY == event.type):
                            if (evdev.categorize(event).keystate == 0):
                                scancode = evdev.categorize(event).scancode
                                buttonName = "unknown"
                                if(115 == scancode):
                                    buttonName = "up"
                                elif(114 == scancode):
                                    buttonName ="down"
                                elif(163 == scancode):
                                    buttonName ="right"
                                elif(165 == scancode):
                                    buttonName ="left"
                                elif(164 == scancode):
                                    buttonName = "ok"

                                print(buttonName)
                                return buttonName
            except OSError as error:
                if (19 == error.errno):
                    self.device = None
                    print("device disconnected, trying to reconnect")
                    await asyncio.sleep(2)
                    self.findDevice()
                    if (self.device):
                        print("reconnected")
                    else:
                        print("Reconnect failed")
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
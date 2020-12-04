import evdev
import asyncio

class BluetoothController:
    """
    A class to create an Interface to a "SmartRemote Consumer Control" device

    Attributes:

        device (evdev.InputDevice): The connected Device, None if no device is connected.
        __observers (List): The observers for the number of connected devices.
        loop (AbstractEventLoop): The running event loop.

    Methods:

        findDevice(): Searches connected devices for "SmartRemote Consumer Control" and puts it in self.device
        readBluetooth(): Waits for events from the device and returns the pressed button
        attach(observer): Attaches a new Observer.
        remove(observer): Removes a Observer.
        notify(): Calls updateDeviceCount() for all observers
        deviceCount(): Returns the number of connected devices.
    """

    def __init__(self):
        """ Tries to find a device, if not successful device == None"""
        self.device = None
        self.__observers = []
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(self.findDevice())

    def attach(self, observer):
        """
        Attaches a new Observer.

        Calls notify().

        Parameters:

            observer (Controller): The observer to be attached.
        """
        self.__observers.append(observer)
        self.loop.run_until_complete(self.notify())

    def detach(self, observer):
        """
        Removes a Observer.

        Parameters:

            observer (Controller): The observer to be removed.
        """
        self.__observers.remove(observer)

    async def notify(self):
        """
        Calls updateDeviceCount() for all observers
        """
        from .controller import Controller #TODO: Test ob nötig
        for observer in self.__observers:
            await observer.updateDeviceCount()

    def deviceCount(self):
        """
        Returns the number of connected devices.
        """
        #return len(self.device)
        if (self.device):
            return 1
        else:
            return 0

    async def findDevice(self):
        """
        Searches connected devices for "SmartRemote Consumer Control" and puts it in self.device

        If a device is found, prints "Device found" and the path to the device
        """
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for device in devices:
            if ("SmartRemote Consumer Control" == device.name):
                self.device = evdev.InputDevice(device.path)
                print("Device found")
                await self.notify() #TODO: Notiy only when client connects, Device is found or Device disconnects (Needs frontend Server Proxy)

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
        if(self.device is not None):
            try:
                return await self.__pressedButton()
            except OSError as error:
                if (19 == error.errno):
                    await self.__handleDisconnect()
        else:
            print("No Device found")
            await self.__tryToConnectAfterTwoSeconds()

    async def __pressedButton(self):
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

    async def __handleDisconnect(self):
        self.device = None
        await self.notify()
        print("device disconnected, trying to reconnect")
        await self.__tryToConnectAfterTwoSeconds()
        if (self.device is not None):
            print("reconnected")
        else:
            print("Reconnect failed")

    async def __tryToConnectAfterTwoSeconds(self):
        await asyncio.sleep(2)
        await self.findDevice()


if __name__ == "__main__":
    bluetoothController = BluetoothController()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bluetoothController.readBluetooth())

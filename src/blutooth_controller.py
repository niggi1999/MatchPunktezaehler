import evdev

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
device_path = None
for device in devices:
  if (device.name == "SmartRemote Consumer Control"):
    print("Device found")
    device_path = device.path

if (not device_path):
  print("No Device found")

if(device_path):
  device = evdev.InputDevice(device_path)
  print(device)
  for event in device.read_loop():
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

print("Hello Word")
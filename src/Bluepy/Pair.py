from bluepy.btle import Scanner, DefaultDelegate, Peripheral, UUID
import binascii
import struct
import time

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print ("Discovered device", dev.addr)
        elif isNewData:
            print ("Received new data from", dev.addr)



class MyDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        # ... initialise here

    def handleNotification(self, cHandle, data):
        print("Notification with cHandle: %s and data: %s" %(cHandle, data))

# Init --------------
class BluetoothConnection():
    def scan(self, scanTime):
        scanner = Scanner().withDelegate(ScanDelegate())
        devices = scanner.scan(scanTime)
        if(len(devices)>0):
            rssilvl= -200
            for dev in devices:
                if(rssilvl<dev.rssi):
                    rssilvl = dev.rssi
            for dev in devices:
                if(rssilvl==dev.rssi):
                    return dev
        

bto = BluetoothConnection()

dev = bto.scan(2.0)

#for dev in devices:
  #  print ("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
   # for (adtype, desc, value) in dev.getScanData():
   #    print ("  %s = %s" % (desc, value))

p = Peripheral()
p.connect(dev)
p.withDelegate(MyDelegate())

dicti = p.getServices()

print(" Sevices:")
for item in dicti:
    print (str(item.uuid)) 
    print(item)

#human = p.getServiceByUUID(0x1812)
#chars = human.getCharacteristics(0x2a4d)

#for char in chars:
    #print(char)

if(False):
    characteristics = p.getCharacteristics()
    print ("Handle   UUID                                Properties")
    print ("-------------------------------------------------------") 
    for ch in characteristics:
        print ("  0x"+ format(ch.getHandle(),'02X')  +"   "+str(ch.uuid) +" " + ch.propertiesToString())

    descriptors=p.getDescriptors(1,0x00F)   #Bug if no limt is specified the function wil hang 
				                        # (go in a endless loop and not return anything)
    print("UUID                                  Handle UUID by name")
    for descriptor in descriptors:
        print ( " "+ str(descriptor.uuid) + "  0x" + format(descriptor.handle,"02X") +"   "+ str(descriptor) )

        #for desc in descriptors:
         #   hand=desc.handle()
         #   print ("Handle: "+str(hand)+" Inhalt: "+ format(p.readCharacteristic(hand)))

Name=p.readCharacteristic(0x07)
print(Name)

#try:
    #ch = human.getCharacteristics(0x2a4d)
    #for c in ch:
       # if (c.supportsRead()):
            #val = binascii.b2a_hex(c.read())
            #print ("0x" + str(val))
            #time.sleep(1)

#finally:
    #p.disconnect()

while(True):
    if(p.waitForNotifications(1)):
        print("True Note")
            
#while True:
    #if p.waitForNotifications(1.0):
        # handleNotification() was called
        #continue

    #print ("Waiting...")
import struct
import math
from enum import IntEnum

from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from dataclasses import dataclass, field
import asyncio
import sys

from client import MikrotikBT5

def on_scan(beacon, device):
    print("---------------------------")
    print(f"  {beacon.address} v: {beacon.version}  {beacon.rssi} dBm")
    print("---------------------------")

    if beacon.hasTemperature():
        print(f"  temperature:  {beacon.temperature:.2f} \u00b0C")
    print( "  acceleration:")
    print(f"      x:         {beacon.acceleration.x:.2f} m/s^2")
    print(f"      y:         {beacon.acceleration.y:.2f} m/s^2")
    print(f"      z:         {beacon.acceleration.z:.2f} m/s^2")
    print(f"  uptime:        {beacon.uptime}")
    print(f"  battery:       {beacon.battery} %")
    print()

async def main(argv):
    scanner = MikrotikBT5(on_scan)
    await scanner.start_scan()
    while (True): # Run forever
        await asyncio.sleep(1)
    await scanner.stop_scan()


if __name__== "__main__":
    try:
        asyncio.run(main(sys.argv[1:]))
    except KeyboardInterrupt:
        print("User interupted.")


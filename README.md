# UDPrix
An UDP tool for Grand Prix 4.
It sends UDP packets in F1 23 format from GP4 to compatible steering wheels thanks to the shared memory access in GPxPatch. 

# Installation

1. Extract UDPrix folder wherever you want in your PC.
2. Open "UDPrixconfig.ini" and make sure IP and PORT are the same of your steering wheel. There are also some extra optional settings to fine tune udp frequency and rpm lights.
3. Double-click on "UDPrix.exe"
4. Launch GPxPatch and make sure "Export" is enabled under Gpxcinfo settings (you must check it also in your mods if you are using CSM)
5. Start GPx and if everything is fine your dashboard should be on with neutral (N).
6. Start a race and enjoy 🙂

# Info data (read from GP4 and sent through UDP)
- Gear
- RPM
- Speed
- Water temperature
- Fuel laps remaining
- Position
- Laps
- Session Time
- Flags

# Notes
- Since in GP4 there is no concept of "fuel litres" and the maximum laps of fuel are 99 the fuel percentage is equal to the fuel remaining laps
- Current lap time is actually che current session time. There is no way to display the live current lap time without breaking everything after you switch to another car.
- If you close the game you don't need to restart the tool, it will be running until you will close it with Ctrl+C or X.

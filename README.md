# OctoPrint-Gpiofan

Takes M106 Snnn commands and mirrors the nnn (number) to a raspberry pi GPIO pin

This plugin expects your fan to be totally and completely controlled by ``M106``. 

That means ``M106 S1`` - ``S255`` to turn it on, and ``M106 S0`` to turn it off. 

It will NOT act upon any instances of ``M107``, so make sure your slicer uses ``M106 S0`` to turn off the fan.

## Setup

1. 
   * Log into the pi using SSH 
   * Install pigpio with ```sudo apt-get update && sudo apt-get install pigpio```
   * Set pigpiod to run on boot ```sudo systemctl enable pigpiod```
   * Start pigpiod ```sudo systemctl start pigpiod```

2. Install the plugin using this URL:

    https://github.com/ntoff/OctoPrint-Gpiofan/archive/master.zip



## Configuration

Set the GPIO pin number in the settings page. 

*Warning!: Pin numbers are* ***BROADCOM*** *pin numbers*, ***not*** *physical pin numbers*. *Not all pins are available for mirroring, for example some pins are permanently locked to +5v, +3.3v, or ground.*

## More Info

pigpio: http://abyz.me.uk/rpi/pigpio/index.html 

pin numbers: https://pinout.xyz/ (use the "BCM" number).

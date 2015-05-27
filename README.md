#StarTrack

monitor old Rainstars


##Disclaimer

This is my very first Python project and my first project on GitHub.
I'm trying to advance in both as this project progresses.


##Description

Monitoring of piston driven reel irrigation systems (eg. Bauer Rainstar 1975-1995) with a RaspberryPi


##Goals

Software

- [ ] measure the current retraction speed
  - [ ] calculate the remaining irrigation time
  - [ ] calculate current water / area
- [ ] communicate over 3G
  - [ ] alert when retraction is finished / has stopped
  - [ ] post status to a server (every half hour ?)

Hardware

- [ ] load battery
  - [ ] with photovoltaic cell
  - [ ] with generator driven by the exhausted water from the piston drive
- [ ] regulate retraction speed


##Hardware

My hardware:

- 1x Bauer Rainstar (90-400 ? from ~1985)
- 1x RaspberryPi Model B (512 MB Ram)
- 2x Inductive proximity sensor Omron E2B-M12KS04-WP-B2 2M
- 1x HD44780 compatible 20x4 character LCD
- 1x 3G Stick Huawei E156G


##Dependencies

###Operating system

I'm running Debian Wheezy (Raspbian image from 05.05.2015). Additional packages installed:

- git
- python-pip (python3-pip)
- python-dev (python3-dev)
- python-smbus (python3-smbus) req. for Adafruit_CharLCD
- build-essential

For 3G connectivity:

- ppp
- wvdial
- sakis3g: http://www.sakis3g.com/ - copy to /usr/bin/


###Python modules

- Adafruit_CharLCD: Original: https://github.com/adafruit/Adafruit_Python_CharLCD / Python3: https://github.com/matthw/Adafruit_Python_CharLCD
- RPi.GPIO (comes with Raspbian)
- subprocess32


##Licence

I'm doing this in my spare time and I don't want to consume it with studying different types of licences. Do what you want with this on your own risk.

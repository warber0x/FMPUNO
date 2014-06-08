Arduino Flash Memory Programmer --AFMP--
========================================
- Author: Samir Radouane.
- Nickname: Warber0x.
- Nickname in arduino forum: BlackSharp.
- Country: Morocco - casablanca
- Date of the first release: 12/24/2013.
- Date Github publish: 06/05/2014.
- E-mail: Sam.Rad@Hotmail.fr


This project is a Flash memory programmer based on Arduino UNO.

The main reason of creating this project is to be able to program a chip for gameboy cartridge and play any game I want. Unfortunately the commercial programmer is expensive and creating your own is fun and easy instead.

Here you will find the graphic scheme of the project as JPEG format and also in Fritzing format.

I suggest to everyone who like to create the same thing to respect the wiring done in the project to ensure that the code works. The diagram is not perfect (Not enough time) but I'll try to increase it gradually.

Some resistors are not added in the diagram because I done it quickly. However, don't forget the resistors for every input in arduino and in the shift registers (The floating state values main problem if it doesn't work). All of the resistors in the project are in 10Kohms.

Adding to this, I have programmed a Python GUI app to make a chip programming more easier for the following chip:

- Amic A29040.
- AMD AM29F040.
- AMD AM29F010.

The app is in beta version. You are free to add or customize the code ;) 

REQUIREMENTS:
- Computer with linux/Windows 7. Linux is recommanded.
- Wx.python library o execute the python program.
- Arduino IDE with the Flash_memory_programmer Sketch.
- Circuit
- Chip AM29F010-40, A29F010-40




Arduino Flash Memory Programmer --AFMP--
========================================
- Author: Samir Radouane.
- Nickname: Warber0x.
- Nickname in arduino forum: BlackSharp.
- Country: Morocco - casablanca
- Date of the first release: 12/24/2013.
- Date of the release in GitHub: 06/05/2014.
- E-mail: Sam.Rad@Hotmail.fr


This project is a Flash memory programmer based on Arduino UNO.

The main reason of creating this project is to be able to program a chip for gameboy cartridge and play any game you want. Unfortunately the commercial programmer is expensive and creating your own is more fun.

Here you will find the graphic scheme of the project as JPEG format and in Fritzing format.

I suggest to everyone who like to create the same thing to respect the wiring done in the project to be sure that the code works. The scheme is not yet perfect (Not enough time) but I'll try to increase it gradually.

Some resistors are not added in the scheme because I done it quickly. However, don't forget the resistors for every input in arduino, and in the shift registers to avoid the floating state values (Main problem if it doesn't work). All of the resistors in the project are in 10Kohms.

Adding to this, I have programmed a Python GUI app to make a chip programming more easier for the following chip:

- Amic A29F040.
- AMD AM29F040.
- AMD AM29F010.

The app bugs sometimes, but you are free to add or customize the code ;) 

REQUIREMENTS:
- Computer with linux/Windows 7. Linux is recommanded.
- Wx.python library o execute the python program.
- Arduino IDE with the Flash_memory_programmer Sketch.
- Circuit
- Chip AM29F010-40, A29F010-40




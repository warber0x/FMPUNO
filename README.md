Arduino Flash Memory Programmer --AFMP--
========================================
- Author: Samir Radouane.
- Nickname: Warber0x.
- Nickname in arduino forum: BlackSharp.
- Country: Morocco - casablanca
- Date of the first release: 12/24/2013.
- Date Github publish: 06/05/2014.
- E-mail: Sam.Rad@Hotmail.fr
- Video link: https://www.youtube.com/watch?v=7V1QDSTN65g&nohtml5=False

===================================================
IMPORTANT NOTICE: The wiring has an issue.
===================================================
PIN 32 -> VCC
PIN 16 -> Ground
===================================================


This project is a Flash memory programmer based on Arduino UNO.

The main reason of creating this project is to be able to program a chip for gameboy cartridge and play any game I want. Unfortunately the commercial programmer is expensive and creating your own is fun and easy instead.

Here you will find the graphic scheme of the project as JPEG format and also in Fritzing format.

I suggest to everyone who like to create the same thing to respect the wiring done in the project to ensure that the code works. The diagram is not perfect (Not enough time) but I'll try to increase it gradually.

Some resistors are not added in the diagram because I done it quickly. Therefore, don't forget to add resistor for every input in arduino and in the shift registers (The floating state values is the main problem if it doesn't work). All of the resistors in the project are in 10Kohms.

Adding to this, I have programmed a Python GUI app to make a chip programming more easier for the following chip:

- Amic A29040.
- AMD AM29F040.
- AMD AM29F010.

The app is in beta version. It crashes sometimes when the upload is finished. You are free to increase or customize the code (But keep my name plz).

REQUIREMENTS:
- Computer with linux/Windows 7. Linux is recommanded.
- Wx.python library o execute the python program.
- Arduino IDE with the Flash_memory_programmer Sketch.
- Circuit & Diagram
- Chip AM29F010-40, A29010-40




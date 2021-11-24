FMPUNO Is now compatible with python3 and wxpython
=======================================================
- Author: Samir Radouane.
- Nickname in arduino forum: BlackSharp (to search through the arduino forum discussion)
- Country: Morocco - casablanca
- Date of the first release: 12/24/2013.
- Date of last release: 24/11/2021
- Date Github publish: 06/05/2014.
- Video link: https://www.youtube.com/watch?v=7V1QDSTN65g&nohtml5=False

IMPORTANT NOTICE: The wiring has an issue
* PIN 32 -> VCC
* PIN 16 -> Ground

This project is a Flash memory programmer based on Arduino UNO.

The main reason for creating this project is to be able to program a flash memory, put it in gameboy cartidge and play any game you want. The commercial programmer is expensive and creating your own is fun ...

In this repo you'll find the graphic scheme of the project in JPEG format as well as in Fritzing format.

I would to tell to anyone who wants to create the same thing, just respect the wiring and everything will be okay. The diagram is not perfect I know but it helps ...

Some resistors are not added in the diagram. Therefore, don't forget to add resistor for every input especially for Adresses and Data chip pins, the same for arduino and the shift registers (The floating state values is the main problem if it doesn't work). All of the resistors in the project are in 10Kohms.

You must have a gameboy cartidge that has a flash instead of ROM chip

Adding to this, I have programmed a Python GUI software to make a chip programming more easier. The supported chips are:

- Amic A29040.
- AMD AM29F040.
- AMD AM29F010.

The app works with python3. It crashes sometimes when the upload is finished. You are free to increase or customize the code (But keep my name plz).

REQUIREMENTS:
- Computer with linux/Windows 7. Linux is recommanded.
- Tested with python3 (There were major bugs in python2)
- Wxpython library
- Pubsub lib
- Arduino IDE with the Flash_memory_programmer Sketch.
- Circuit & Diagram
- Chip AM29F010-40, A29010-40




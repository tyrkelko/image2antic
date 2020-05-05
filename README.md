# image2antic
Image Convert As CC65 Atari 8-Bit Code To Display Image On Atari 8-Bit Micro Computers 

image2antic.py is a tkinter GUI python application.
Tested on Ubuntu 16.04 and Windows 10, but, should easily work on any compatible station that can run Python with PIL/Pillow (Python Imaging Library).

To start the app, 
1. run image2antic.py
2. Browse for an image you'd like to convert. This version supports height up to 96 in multiples of 8, width up to 160 in multiples of 8 and up to 4 colors. Currently the script doesn't validate anything, so, any image that doesn't comply might not work as expected.
3. Once image was selected, some properties will be printed on the dialog including width, height and colors A8 palette.
4. Select antic mode 4 or 5.
5. Clicking "Process" will print CC65 compatible code that includes multiple charsets and screen data required to display the image on an Atari 8-Bit Micro Computer.

Requirements:
python 3.x (tested with 3.7.2 on Windows 10 and Ubuntu 16.04)
PIL/Pillow (Python Imaging Library/PIL fork)
- PIL is installed by default on most linux python installations
- To install you need to run the following, you might need some priviliges for that:
python -m pip install --upgrade pip
python -m pip install --upgrade Pil

For image background you will also need ImageTK from PIL. To install on Ubuntu use:
sudo apt-get install python3-pil python3-pil.imagetk

Optional requirements:
CC65 cross compiler
Altirra or any other emulator for the Atari 8-Bit computer (tested with Altirra on a PAL Atari 800XL ROM)

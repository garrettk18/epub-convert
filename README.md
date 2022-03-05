# epub-convert: Convert EPUB Files for Reading on Various Braille Displays and E-Readers

## What Is It?

This is a python script that converts a directory full of .epub files into either HTML or text files. This allows the reading of books in nEPUB on devices such as:

* The Brailliant BI series by Humanware (e.g., [BI 40x](https://store.humanware.com/hus/brailliant-bi-40x-braille-display.html)
* The [Victor Reader Stream](https://www.humanware.com/microsite/stream/index.html)/Trek series by Humanware
* The Braille Edge by Himms
* Anything else that supports HTML or ASCII text files

## Setup

### Windows

1. Download and install Python for Windows, at this time version [3.10.2](https://www.python.org/ftp/python/3.10.2/python-3.10.2-amd64.exe)
2. Download and install [Pandoc](https://github.com/jgm/pandoc/releases/download/2.17.1.1/pandoc-2.17.1.1-windows-x86_64.msi) 
3. Open an administrator PowerShell (WINDOWS+x, followed by the letter a. Answer "yes" to the UAC prompt.)
4. Type py -3 -m pip install pypandoc
5. Move the script into a directory of EPUB files
6. Run epub-convert.py
7. Look in the `html conversions` directory for your yummy books!

### Linux (Debian, Ubuntu)
1. `sudo apt install python3-pip pandoc`
2. `sudo pip3 install pypandoc`
3. See steps 5-7 above, and enjoy!

##Command line options

* -T: Conver to text files instead of HTML
* -i: Input directory
* -o: output directory

## Credits
Thanks to @thunderdrop for implementing the conversion progress support. @ultrasound1372 has also been invaluable with his suggestions for improvement.


Marks: 30/40

ANDROID EXPLORER README AND INSTALLATION NOTES

COMPATIBILITY
This project was developed under Microsoft Windows 8 and Ubuntu 12.04,
using Python 2.7.5. Backwards compatibility with versions of Python earlier
than 2.7.5 is not guaranteed. This project is meant for Windows and Unix-like 
systems.

LIBRARIES & DEPENDENCIES
This application requires:
Python Imaging Library (PIL)
Dropbox Core SDK for Python
SendKeys (for Windows)
xdotool (for Linux)(not a python library, but a Linux tool)

This application also assumes that the user has properly setup Android Debugging 
Bridge. More infomation here: http://developer.android.com/tools/help/adb.html

INSTALLATION
Simply extract the contents of this ZIP file to a directory, making sure to
maintain the directory structure of the ZIP file.

HOW TO RUN
To run the application, run the file run.pyw with Python. For command line inferfaces, 
run cli_drpbx.py or cli_target.py with Python within a console.
Note: Do not try to run the files through IDLE as IDLE has some issues with the 
__file__ variable which is used extensively in this application.

LICENSE
This project is released under the following modified version of the MIT
License:

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
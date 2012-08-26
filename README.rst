README for Falcon Flight Hours Tracker
======================================

Thanks for checking out Falcon! So far I haven't had the chance to get much
feedback on how well this program works on other people's machines, so please
try it out and let me know what happens (good or bad!). Here's the bare bones
you need to know to try to get it working on your computer...

Pre-built executable
--------------------

This is the simplest way to install on Windows.

- Download `falcon-win32.zip <https://github.com/downloads/futurulus/falcon/falcon-win32.zip>`_.
  (If you don't like that link, it's on the
  `Downloads <https://github.com/futurulus/falcon/downloads>`_ page, which you
  can also get to by clicking a nondescript tab up in the top right of this
  page.) 
- Unzip (Extract All...) the package somewhere where you'll remember it.
- Go into the resulting folder and double-click falcon.exe.

If it works...hooray! If it doesn't, let me know what happened instead, and
I'll see what can be done to fix it.

Installing from source
----------------------

This is the more difficult route, and requires a bit of preparation before
you can run the program. You'll need to download these pieces first:

- Python (http://python.org/download/)
- wxPython (http://wxpython.org/download.php#stable)

Then, download the `source <https://github.com/futurulus/falcon/zipball/master>`_
(you can also click the "ZIP" cloud icon, top left |--| ish), extract it
somewhere, and double-click main.pyw. If nothing happens at all, try running
it from the command line/terminal::

  (On Windows)
  > C:\Python27\python main.pyw
  (On Mac/Linux)
  > python main.pyw

This can be a pain to get working correctly, especially if you're on
Windows and you've never run a Python program from source before. However,
this is the only way to get the program running on Mac or Linux.

My test setup
-------------

- Windows 7 and Ubuntu Oneiric
- Python 2.7, wxPython 2.8.12 (32-bit)

So if your computer looks like that, there's something seriously wrong if it
doesn't work for you. Still, it wouldn't surprise me if there are things still
seriously wrong with the program |---| let me know what your results are, so I
can make things less wrong. 

Disclaimers 'n' Stuff
---------------------

This program is for convenience only and is not a substitute for careful
attention; government-, company-, and union-endorsed software; or other
official means of verifying compliance with regulations.  It is the pilot's
responsibility to ensure that he/she is in accordance with all applicable
regulations and safety procedures when operating an aircraft.  I make no
guarantees of accuracy or completeness of the output of this program.

(In short: this is a silly hobby project.  There will be
`bugs <https://github.com/futurulus/falcon/issues>`_ in it.  Don't
make people's lives depend on its correctness.)

Falcon is distributed under a BSD-style license.  See the file COPYING for
license conditions.

.. |--| unicode:: U+02013 .. en dash
   :trim:
.. |---| unicode:: U+02014 .. em dash
   :trim:
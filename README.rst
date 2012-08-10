README for Falcon Flight Hours Tracker
======================================

I'll put some real README material up once I have some real functionality in
this thing.  Until then, here's the bare bones for anyone who cares enough to
try to get it working on their machine...

Pre-built executable
--------------------

This is the simplest way to install on Windows.

- Click on the Downloads link above. (It's on the right, about a thumb's
  length from the top of the page. I wish Github would make it a bit
  more enticing...)
- Download falcon-win32.zip.
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

Then, click on ZIP (the cloud icon, top left |--| ish), extract it somewhere,
and double-click main.pyw. If nothing happens at all, try running it from the
command line/terminal::

  (On Windows)
  > C:\Python27\python main.pyw
  (On Linux)
  > python main.pyw

This can be a pain to get working correctly, especially if you're on
Windows and you've never run a Python program from source before. On the
other hand, as a reward, the program will look
`much nicer <https://github.com/futurulus/falcon/issues/10>`_ if you do this.
Also, this is the only way to get the program running on Mac or Linux.

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
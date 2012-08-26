'''Build an executable.'''
from distutils.core import setup
import os
import py2exe


def add_pytz_files():
    '''
    Modified from
        http://code.google.com/p/googletransitdatafeed/source/browse/trunk/
        python/setup.py
    by way of
        http://stackoverflow.com/questions/9158846/unknowntimezoneerror-
        exception-raised-with-python-application-compiled-with-py2e

    Copyright (C) 2007 Google Inc.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this section except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0
    '''
    import pytz
    import zipfile
    zipfile_path = os.path.join('dist', 'library.zip')
    with zipfile.ZipFile(zipfile_path, 'a') as library_zip:
        zoneinfo_dir = os.path.join(os.path.dirname(pytz.__file__), 'zoneinfo')
        disk_basedir = os.path.dirname(os.path.dirname(pytz.__file__))
        for abs_dir, _directories, filenames in os.walk(zoneinfo_dir):
            assert abs_dir.startswith(disk_basedir), (abs_dir, disk_basedir)
            zip_dir = abs_dir[len(disk_basedir):]
            for filename in filenames:
                library_zip.write(os.path.join(abs_dir, filename),
                                  os.path.join(zip_dir, filename))

setup(windows=[
          {'script': 'main.pyw',
           'icon_resources': [(1, 'falcon.ico')],
           'other_resources': [(24, 1, open('MANIFEST', 'r').read())]}
      ],
      data_files=[
          ('', ['falcon.ico'])
      ],
      options={'py2exe': {
          #'compressed': 1,
          #'optimize': 2,
          'bundle_files': 1,
          'packages': ['pytz'],
      }})

add_pytz_files()

os.rename('dist/main.exe', 'dist/falcon.exe')

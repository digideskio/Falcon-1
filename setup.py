'''Build an executable.'''
from distutils.core import setup
import py2exe

setup(windows=[
          {'script': 'main.pyw',
           'icon_resources': [(1, 'falcon.ico')]}
      ],
      data_files=[
          ('', ['falcon.ico'])
      ]
)

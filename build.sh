rm -rf dist falcon-win32.zip
/c/Python27/python setup.py py2exe
mv dist falcon-win32
zip -r falcon-win32.zip falcon-win32/
mv falcon-win32 dist

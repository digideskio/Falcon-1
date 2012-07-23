#! /usr/bin/env python
'''
Uploads Windows binary zip files to github.

Major thanks to Scott Chacon (https://github.com/schacon), who wrote this
file in a more general form in Ruby. The original is at
    https://github.com/schacon/git_osx_installer/
            blob/master/upload-to-github.rb
'''

import json
import os
import re
import subprocess


USER = 'futurulus'
REPO = 'falcon'
FILES = {
    'falcon-win32.zip': 'Windows binary files',
}


def output_of(cmd):
    cmd = cmd.strip().replace('\n', ' ')
    print(cmd)
    output = subprocess.check_output(cmd, shell=True)
    print(output)
    return output


def upload(filename, desc):
    args = {
        'filename': filename,
        'fullname': os.path.abspath(filename),
        'size': os.path.getsize(filename),
        'desc': desc,
        'user': USER,
        'url': "https://api.github.com/repos/%s/%s/downloads" % (USER, REPO),
    }

    # create entry
    create_cmd = '''
        curl -s -XPOST
             -d '{"name":"%(filename)s",
                  "size":%(size)d,
                  "description":"%(desc)s"}'
             -u "%(user)s"
             %(url)s
    ''' % args

    data = json.loads(output_of(create_cmd))
    data['filename'] = filename

    # upload filename to bucket
    upload_cmd = '''
        curl -s
             -F "key=%(path)s"
             -F "acl=%(acl)s"
             -F "success_action_status=201"
             -F "Filename=%(name)s"
             -F "AWSAccessKeyId=%(accesskeyid)s"
             -F "Policy=%(policy)s"
             -F "Signature=%(signature)s"
             -F "Content-Type=%(mime_type)s"
             -F "file=@%(filename)s"
             https://github.s3.amazonaws.com/
    ''' % data

    xml = output_of(upload_cmd)

    match = re.match(r'\<Location\>(.*)\<\/Location\>', xml)
    if match is not None:
        # not sure i want to fully URL
        # decode this, but these will not do
        print("Uploaded to: %s" % match.group(1).replace('%2F', '/'))
    else:
        raise IOError("Upload of %s failed. Response is:\n\n %s" %
                      (filename, xml))


if __name__ == '__main__':
    try:
        for path in FILES:
            upload(path, FILES[path])
    except IOError, err:
        print(err)

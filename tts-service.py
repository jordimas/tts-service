#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2016 Jordi Mas i Hernandez <jmas@softcatala.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.

from flask import Flask, request, Response, send_file
import subprocess
import tempfile
import hashlib
import datetime
import os
import json
from usage import Usage

app = Flask(__name__)


def getMD5(text):
    m = hashlib.md5()
    m.update(text.encode('utf-8'))
    s = m.hexdigest()[:8].lower()
    return s


@app.route('/speak/', methods=['GET'])
def voice_api():
    text = request.args.get('text')
    token = request.args.get('token')

    if token is None or getMD5(text) != token.lower():
        return ("Forbidden", 403)

    iconv = '/usr/bin/iconv'
    txt2wave = '/usr/bin/text2wave'
    lame = '/usr/bin/lame'

    with tempfile.NamedTemporaryFile() as text_file,\
         tempfile.NamedTemporaryFile() as encoded_file,\
         tempfile.NamedTemporaryFile() as wave_file,\
         tempfile.NamedTemporaryFile() as mp3_file:

        f = open(text_file.name, 'w', encoding='utf8')
        f.write(text)
        f.close()

        cmd = '{0} -f utf8 -t ISO-8859-15//TRANSLIT {1} > {2}'.\
              format(iconv, text_file.name, encoded_file.name)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        p.wait()

        cmd = '{0} -o {1} {2} -eval cfg.txt'.\
              format(txt2wave, wave_file.name, encoded_file.name)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        p.wait()

        cmd = '{0} {1} {2}'.\
              format(lame, wave_file.name, mp3_file.name)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        p.wait()

        usage = Usage()
        usage.log()
        return send_file(mp3_file.name, mimetype="audio/mp3",
                        as_attachment=False, attachment_filename=mp3_file.name)

@app.route('/speak/stats/', methods=['GET'])
def stats():
    requested = request.args.get('date')
    date_requested = datetime.datetime.strptime(requested, '%Y-%m-%d')
    usage = Usage()
    calls = usage.get_stats(date_requested)

    result = {}
    result['calls'] = calls
    return json_answer(json.dumps(result, indent=4, separators=(',', ': ')))

def json_answer(data):
    resp = Response(data, mimetype='application/json')
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == '__main__':
    app.debug = True
    app.run()

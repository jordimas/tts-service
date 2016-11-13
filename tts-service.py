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

from flask import Flask, request, Response
from flask import send_file
import subprocess

app = Flask(__name__)


@app.route('/api/voice/', methods=['GET'])
def voice_api():
    text = request.args.get('text')
    
    f = open('voice.txt','w', encoding='utf8')
    f.write(text)
    f.close()

    p = subprocess.Popen('/usr/bin/iconv -f utf8 -t ISO-8859-15//TRANSLIT voice.txt > voice.8859',shell=True, stdout=subprocess.PIPE)
    p.wait()

    p = subprocess.Popen('/usr/bin/text2wave -o text.wav voice.8859 -eval cfg.txt',shell=True, stdout=subprocess.PIPE)
    p.wait()   

    p = subprocess.Popen('/usr/bin/lame text.wav text.mp3',shell=True, stdout=subprocess.PIPE)
    p.wait()

 
    return send_file('text.mp3', mimetype="audio/mp3", as_attachment=False, attachment_filename="text.mp3") 

if __name__ == '__main__':
    app.debug = True
    app.run()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import request

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/calEnergy')
def calEnergy():
    jindu = request.args.get('jindu')
    weidu = request.args.get('weidu')
    return "jindu =" + jindu +", weidu =" + weidu

if __name__ == '__main__':
    app.run()
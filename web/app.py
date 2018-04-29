#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
import sys
sys.path.append("..")

import forecast_main

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/calEnergy')
def calEnergy():
    start = request.args.get('start')
    end = request.args.get('end')
    return "start =" + start +", end =" + end

if __name__ == '__main__':
    app.run()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
import forecast_main
import json

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/calEnergy')
def calEnergy():
    start = request.args.get('start')
    end = request.args.get('end')

    dSOCInJam,dSOCNoJam = forecast_main.powerConsumptionEstn(start, end)
    print(str(dSOCInJam) + "," + str(dSOCNoJam))
    res = {'dSOCInJam':dSOCInJam, 'dSOCNoJam':dSOCNoJam}
    return json.dumps(res)

if __name__ == '__main__':
    app.run()
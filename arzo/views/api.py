# -*- coding: utf-8 -*-

from flask import request
from arzo import app, services

import json


@app.route('/api/elevation')
def api_elevation():
    return services.get_elevation(request.args.get('latitude', ''), request.args.get('longitude', ''))


@app.route('/api/weather')
def api_weather():
    data = services.get_weather(request.args.get('latitude', ''), request.args.get('longitude', ''))
    return json.dumps(data)

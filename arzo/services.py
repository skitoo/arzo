# -*- coding: utf-8 -*-

from arzo import cache, logger
from arzo.settings import GOOGLE_API_KEY

import requests
import arrow


@cache.memoize()
def get_elevation(latitude, longitude):
    logger.debug('get_elevation call')
    locations = '%s,%s' % (latitude, longitude)
    response = requests.get(
        'https://maps.googleapis.com/maps/api/elevation/json',
        params={'locations': locations, 'key': GOOGLE_API_KEY, 'sensor': 'false'}
    )
    data = response.json()
    return str(data['results'][0]['elevation'])


@cache.memoize()
def get_timezone(latitude, longitude):
    logger.debug('get_timezone call')
    location = '%s,%s' % (latitude, longitude)
    response = requests.get(
        'https://maps.googleapis.com/maps/api/timezone/json',
        params={'location': location, 'key': GOOGLE_API_KEY, 'sensor': 'false', 'timestamp': arrow.utcnow().timestamp}
    )
    logger.debug(response.json())
    return response.json()['timeZoneId']


def get_local_time(latitude, longitude):
    timezone = get_timezone(latitude, longitude)
    return arrow.utcnow().to(timezone).timestamp


@cache.memoize(60 * 5)  # cached for 5 minutes
def get_weather(latitude, longitude):
    logger.debug('get_weather call')
    response = requests.get(
        'http://api.openweathermap.org/data/2.5/weather',
        params={'lat': latitude, 'lon': longitude, 'lang': 'fr'}
    )
    data = response.json()
    return {
        'temp': '%.1f' % (data['main']['temp'] - 273.15),
        'wind_speed': '%.2f' % (data['wind']['speed'] * 3.6),
        'humidity': '%d' % (data['main']['humidity']),
        'weather': data['weather'][0]['main'].lower(),
        'description': data['weather'][0]['description'].title()
    }

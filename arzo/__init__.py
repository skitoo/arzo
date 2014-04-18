# -*- coding: utf-8 -*-

from __future__ import division

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.cache import Cache
from arzo import settings


app = Flask(__name__)
app.config.from_object(settings)
cache = Cache(app, config=settings.CACHE_CONFIG)
db = SQLAlchemy(app)
logger = app.logger


import arzo.forms # noqa
import arzo.models # noqa
import arzo.views # noqa

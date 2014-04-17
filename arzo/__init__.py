# -*- coding: utf-8 -*-

from __future__ import division

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from arzo import settings


app = Flask(__name__)
app.config.from_object(settings)
db = SQLAlchemy(app)


import arzo.forms # noqa
import arzo.models # noqa
import arzo.views # noqa

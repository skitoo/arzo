# -*- coding: utf-8 -*-

from __future__ import division

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


# -------
# Models
# -------

class Observatory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    altitude = db.Column(db.Integer)
    longitude = db.Column(db.Integer)
    latitude = db.Column(db.Integer)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, onupdate=datetime.now)


class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, onupdate=datetime.now)


class Eyepiece(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    focal = db.Column(db.Integer, nullable=False)
    field_of_view = db.Column(db.Integer, nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, onupdate=datetime.now)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    brand = db.relationship('Brand', backref=db.backref('eyepieces', lazy='dynamic'))


class TelescopeCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, onupdate=datetime.now)


class Telescope(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    aperture = db.Column(db.Integer, nullable=False)
    focal = db.Column(db.Integer, nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now)
    update_at = db.Column(db.DateTime, onupdate=datetime.now)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    brand = db.relationship('Brand', backref=db.backref('eyepieces', lazy='dynamic'))
    telescope_category_id = db.Column(db.Integer, db.ForeignKey('telescope_category.id'))
    telescope_category = db.relationship('TelescopeCategory', backref=db.backref('telescopes', lazy='dynamic'))

    @property
    def focal_ratio(self):
        return self.aperture / self.focal


# -------
# Views
# -------

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

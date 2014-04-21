# -*- coding: utf-8 -*-

from arzo import db
from datetime import datetime


class Observatory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, info={'label': 'Nom'})
    description = db.Column(db.Text, info={'label': 'Description'})
    altitude = db.Column(db.Integer, info={'label': 'Altitude', 'info': 'En mètre'})
    longitude = db.Column(db.Float, nullable=False, info={'label': 'Longitude'})
    latitude = db.Column(db.Float, nullable=False, info={'label': 'Latitude'})
    timezone = db.Column(db.String, nullable=False, info={'label': 'Fuseau horaire'})
    create_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    update_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    selected = db.Column(db.Boolean, nullable=False, default=False, index=True, info={'label': u'Sélectionner'})

    def __str__(self):
        return '<Observatory #%d - %s>' % (self.id, self.name)

    def __repr__(self):
        return str(self)


class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, info={'label': u'Nom'})
    create_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    update_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def count_eyepieces(self):
        return self.eyepieces.count()

    def count_opticalaids(self):
        return self.opticalaids.count()

    def count_telescopes(self):
        return self.telescopes.count()

    def __str__(self):
        return '<Brand #%d - %s>' % (self.id, self.name)

    def __repr__(self):
        return str(self)


class Eyepiece(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    focal = db.Column(db.Integer, nullable=False)
    field_of_view = db.Column(db.Integer, nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    update_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    brand = db.relationship('Brand', backref=db.backref('eyepieces', lazy='dynamic'))


class OpticalAid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    update_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    brand = db.relationship('Brand', backref=db.backref('opticalaids', lazy='dynamic'))


class TelescopeCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    update_at = db.Column(db.DateTime, onupdate=datetime.utcnow)


class Telescope(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    aperture = db.Column(db.Integer, nullable=False)
    focal = db.Column(db.Integer, nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    update_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    brand = db.relationship('Brand', backref=db.backref('telescopes', lazy='dynamic'))
    telescope_category_id = db.Column(db.Integer, db.ForeignKey('telescope_category.id'))
    telescope_category = db.relationship('TelescopeCategory', backref=db.backref('telescopes', lazy='dynamic'))

    @property
    def focal_ratio(self):
        return self.aperture / self.focal


class Observation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)
    create_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    update_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    telescope_id = db.Column(db.Integer, db.ForeignKey('telescope.id'))
    telescope = db.relationship('Telescope')
    eyepiece_id = db.Column(db.Integer, db.ForeignKey('eyepiece.id'))
    eyepiece = db.relationship('Eyepiece')
    observatory_id = db.Column(db.Integer, db.ForeignKey('observatory.id'))
    observatory = db.relationship('Observatory')

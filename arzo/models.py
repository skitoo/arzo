# -*- coding: utf-8 -*-

from arzo import db
from datetime import datetime


DIAMETERS_EYEPIECE_LIST = (
    (31.75, '31.75 mm'),
    (50.8, '50.8 mm'),
)

TELESCOPE_CATEGORY_LIST = (
    (1, 'Lunette'),
    (2, 'Newton'),
    (3, 'Schmidt-Cassegrain'),
    (4, 'Ritchey-Chrétien'),
    (5, 'Maksutov-Cassegrain'),
    (6, 'Dobson'),
)


class Observatory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, info={'label': 'Nom'})
    description = db.Column(db.Text, info={'label': 'Description'})
    altitude = db.Column(db.Integer, info={'label': 'Altitude', 'info': 'En mètre'})
    longitude = db.Column(db.Float, nullable=False, default=0, info={'label': 'Longitude'})
    latitude = db.Column(db.Float, nullable=False, default=0, info={'label': 'Latitude'})
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
        return Eyepiece.query.filter(Eyepiece.brand_id == self.id).count()

    def count_opticalaids(self):
        return OpticalAid.query.filter(OpticalAid.brand_id == self.id).count()

    def count_telescopes(self):
        return Telescope.query.filter(Telescope.brand_id == self.id).count()

    def __str__(self):
        return '<Brand #%d - %s>' % (self.id, self.name)

    def __repr__(self):
        return str(self)


class Eyepiece(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False, info={'label': u'Nom'})
    focal = db.Column(db.Integer, nullable=False, info={'label': u'Longueur focale'})
    field_of_view = db.Column(db.Integer, nullable=False, info={'label': u'Champ de vision'})
    diameter = db.Column(db.Float, nullable=False, info={'label': u'Diamètre', 'choices': DIAMETERS_EYEPIECE_LIST})
    create_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    update_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    brand = db.relationship(Brand, backref=db.backref('eyepieces'))

    def __str__(self):
        return u'<Eyepiece #%d - %s>' % (self.id if self.id else 0, self.name)

    def __repr__(self):
        return str(self)


class OpticalAid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    update_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    brand = db.relationship('Brand', backref=db.backref('opticalaids', lazy='dynamic'))


class Telescope(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    aperture = db.Column(db.Integer, nullable=False)
    focal = db.Column(db.Integer, nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    update_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    brand = db.relationship('Brand', backref=db.backref('telescopes', lazy='dynamic'))
    category = db.Column(db.Integer, nullable=False, info={'label': u'Catégorie', 'choices': TELESCOPE_CATEGORY_LIST})

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

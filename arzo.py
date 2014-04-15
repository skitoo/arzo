# -*- coding: utf-8 -*-

from __future__ import division

from flask import Flask, render_template, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms_alchemy import model_form_factory
from datetime import datetime


ModelForm = model_form_factory(Form)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://arzo:arzo-mdp@localhost/arzo'
app.config['SECRET_KEY'] = 'test'
app.config['MAIN_MENU'] = [
    {'target': 'index', 'label': 'Tableau de bord', 'icon': 'fa fa-dashboard', 'activate': ['index']},
    {'target': 'observatories', 'label': 'Observatoires', 'icon': 'fa fa-globe', 'activate': ['observatory', 'observatories', 'new_observatory']}
]
db = SQLAlchemy(app)


# -------
# Models
# -------

class Observatory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, info={'label': 'Nom'})
    description = db.Column(db.Text, info={'label': 'Description'})
    altitude = db.Column(db.Integer, info={'label': 'Altitude', 'info': 'En mètre'})
    longitude = db.Column(db.Float, info={'label': 'Longitude'})
    latitude = db.Column(db.Float, info={'label': 'Latitude'})
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    update_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    selected = db.Column(db.Boolean)

    def __str__(self):
        return '<Observatory #%d - %s>' % (self.id, self.name)

    def __repr__(self):
        return str(self)


class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    update_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return '<Brand #%d - %s>' % (self.id, self.name)

    def __repr__(self):
        return str(self)


class Eyepiece(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    focal = db.Column(db.Integer, nullable=False)
    field_of_view = db.Column(db.Integer, nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    update_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    brand = db.relationship('Brand', backref=db.backref('eyepieces', lazy='dynamic'))


class OpticalAid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    update_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    brand = db.relationship('Brand', backref=db.backref('opticalaids', lazy='dynamic'))


class TelescopeCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    update_at = db.Column(db.DateTime, onupdate=datetime.utcnow)


class Telescope(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    aperture = db.Column(db.Integer, nullable=False)
    focal = db.Column(db.Integer, nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
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
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    update_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    telescope_id = db.Column(db.Integer, db.ForeignKey('telescope.id'))
    telescope = db.relationship('Telescope')
    eyepiece_id = db.Column(db.Integer, db.ForeignKey('eyepiece.id'))
    eyepiece = db.relationship('Eyepiece')
    observatory_id = db.Column(db.Integer, db.ForeignKey('observatory.id'))
    observatory = db.relationship('Observatory')


# -------
# Forms
# -------

class ObservatoryForm(ModelForm):
    class Meta:
        model = Observatory
        exclude = ['update_at']

# -------
# Views
# -------


@app.route('/')
def index():
    return render_template(
        'index.html',
        breadcrumb=[
            (url_for('index'), 'Accueil')
        ]
    )


@app.route('/observatories')
def observatories():
    observatories = Observatory.query.all()
    return render_template(
        'observatories.html',
        observatories=observatories,
        title='Observatoires',
        breadcrumb=[
            (url_for('index'), 'Accueil'),
            (url_for('observatories'), 'Observatoires'),
        ]
    )


@app.route('/observatory/<int:observatory_id>', methods=('GET', 'POST'))
def observatory(observatory_id):
    observatory = Observatory.query.get_or_404(observatory_id)
    form = ObservatoryForm(obj=observatory)
    if form.validate_on_submit():
        form.populate_obj(observatory)
        db.session.merge(observatory)
        db.session.commit()
    return render_template(
        'edit_observatory.html',
        form=form,
        title='Observatoire - %s' % observatory.name,
        breadcrumb=[
            (url_for('index'), 'Accueil'),
            (url_for('observatories'), 'Observatoires'),
            (url_for('observatory', observatory_id=observatory_id), observatory.name),
        ]
    )


@app.route('/observatory', methods=('GET', 'POST'))
def new_observatory():
    form = ObservatoryForm()
    if form.validate_on_submit():
        observatory = Observatory()
        form.populate_obj(observatory)
        db.session.add(observatory)
        db.session.commit()
        return redirect(url_for('observatories'))
    return render_template(
        'edit_observatory.html',
        form=form,
        title='Nouvel observatoire',
        breadcrumb=[
            (url_for('index'), 'Accueil'),
            (url_for('observatories'), 'Observatoires'),
            (url_for('new_observatory'), 'Nouvel observatoire'),
        ]
    )


@app.route('/delete-observatory', methods=('POST'))
def delete_observatory(observatory_id):
    return ''


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')

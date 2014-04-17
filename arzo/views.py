# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, flash, request
from arzo import app, db, cache
from arzo.models import Observatory
from arzo.forms import ObservatoryForm
from arzo.settings import GOOGLE_API_KEY

import requests
import json


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
        if observatory.selected:
            Observatory.query.filter(Observatory.id != observatory.id).update({Observatory.selected: False})
        db.session.commit()
        flash(u'Observatoire sauvegardé avec succès', 'success')
        return redirect(url_for('observatories'))
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
        if observatory.selected:
            Observatory.query.filter(Observatory.id != observatory.id).update({Observatory.selected: False})
        db.session.commit()
        flash(u'Observatoire sauvegardé avec succès', 'success')
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


@app.route('/observatory/<int:observatory_id>/delete')
def delete_observatory(observatory_id):
    observatory = Observatory.query.get_or_404(observatory_id)
    db.session.delete(observatory)
    db.session.commit()
    flash(u'Observatoire supprimé avec succès', 'success')
    return redirect(url_for('observatories'))


@app.route('/api/elevation')
def api_elevation():
    locations = '%s,%s' % (request.args.get('latitude', ''), request.args.get('longitude', ''))
    cached = cache.get('api_elevation#%s' % locations)
    if cached:
        return cached
    else:
        response = requests.get('https://maps.googleapis.com/maps/api/elevation/json', params={'locations': locations, 'key': GOOGLE_API_KEY, 'sensor': 'true'})
        data = response.json()
        data = str(data['results'][0]['elevation'])
        cache.set('api_elevation#%s' % locations, data)
    return data


@app.route('/api/weather')
def api_weather():
    lat, lon = request.args.get('latitude', ''), request.args.get('longitude', '')
    response = requests.get('http://api.openweathermap.org/data/2.5/weather', params={'lat': lat, 'lon': lon, 'lang': 'fr'})
    data = response.json()
    data = {
        'temp': '%.1f' % (data['main']['temp'] - 273.15),
        'wind_speed': '%.2f' % (data['wind']['speed'] * 3.6),
        'humidity': '%d' % (data['main']['humidity']),
        'weather': data['weather'][0]['main'].lower(),
        'description': data['weather'][0]['description'].title()
    }
    return json.dumps(data)

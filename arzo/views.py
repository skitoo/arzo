# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, flash, request
from arzo import app, db
from arzo.models import Observatory, Brand
from arzo.forms import ObservatoryForm, BrandForm
from arzo import services

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


@app.route('/brands')
def brands():
    brands = Brand.query.all()
    return render_template(
        'brand/index.html',
        brands=brands,
        title='Marques',
        breadcrumb=[
            (url_for('index'), 'Accueil'),
            (url_for('brands'), 'Marques'),
        ]
    )


@app.route('/brand', methods=('GET', 'POST'))
def new_brand():
    form = BrandForm()
    if form.validate_on_submit():
        brand = Brand()
        form.populate_obj(brand)
        db.session.add(brand)
        db.session.commit()
        flash(u'Marque sauvegardée avec succès', 'success')
        return redirect(url_for('brands'))
    return render_template(
        'brand/edit.html',
        form=form,
        breadcrumb=[
            (url_for('index'), 'Accueil'),
            (url_for('brands'), 'Marques'),
            (url_for('new_brand'), 'Nouvelle marque'),
        ]
    )


@app.route('/brand/<int:brand_id>/edit', methods=('GET', 'POST'))
def edit_brand(brand_id):
    brand = Brand.query.get_or_404(brand_id)
    form = BrandForm(obj=brand)
    if form.validate_on_submit():
        form.populate_obj(brand)
        db.session.merge(brand)
        db.session.commit()
        flash(u'Marque sauvegardée avec succès', 'success')
        return redirect(url_for('brands'))
    return render_template(
        'brand/edit.html',
        form=form,
        title='Marques - %s' % brand.name,
        breadcrumb=[
            (url_for('index'), 'Accueil'),
            (url_for('brands'), 'Marques'),
            (url_for('show_brand', brand_id=brand_id), brand.name),
        ]
    )


@app.route('/brand/<int:brand_id>')
def show_brand(brand_id):
    brand = Brand.query.get_or_404(brand_id)
    return render_template(
        'brand/show.html',
        brand=brand,
        title='Marques - %s' % brand.name,
        breadcrumb=[
            (url_for('index'), 'Accueil'),
            (url_for('brands'), 'Marques'),
            (url_for('show_brand', brand_id=brand_id), brand.name),
        ]
    )


@app.route('/brand/<int:brand_id>/delete')
def delete_brand(brand_id):
    brand = Brand.query.get_or_404(brand_id)
    db.session.delete(brand)
    db.session.commit()
    flash(u'Marque supprimée avec succès', 'success')
    return redirect(url_for('brands'))


@app.route('/api/elevation')
def api_elevation():
    return services.get_elevation(request.args.get('latitude', ''), request.args.get('longitude', ''))


@app.route('/api/weather')
def api_weather():
    data = services.get_weather(request.args.get('latitude', ''), request.args.get('longitude', ''))
    return json.dumps(data)

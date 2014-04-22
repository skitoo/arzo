# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, flash, request
from arzo import app, db
from arzo.models import Observatory
from arzo.forms import ObservatoryForm


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


@app.route('/observatory/<int:observatory_id>')
def show_observatory(observatory_id):
    observatory = Observatory.query.get_or_404(observatory_id)
    return render_template(
        'show_observatory.html',
        observatory=observatory,
        title='Observatoire - %s' % observatory.name,
        breadcrumb=[
            (url_for('index'), 'Accueil'),
            (url_for('observatories'), 'Observatoires'),
            (url_for('edit_observatory', observatory_id=observatory_id), observatory.name),
        ]
    )


@app.route('/observatory/<int:observatory_id>/edit', methods=('GET', 'POST'))
def edit_observatory(observatory_id):
    observatory = Observatory.query.get_or_404(observatory_id)
    form = ObservatoryForm(obj=observatory)
    if form.validate_on_submit():
        form.populate_obj(observatory)
        observatory.altitude = services.get_elevation(observatory.latitude, observatory.longitude)
        observatory.timezone = services.get_timezone(observatory.latitude, observatory.longitude)
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
            (url_for('show_observatory', observatory_id=observatory_id), observatory.name),
            (None, u'Édition')
        ]
    )


@app.route('/observatory', methods=('GET', 'POST'))
def new_observatory():
    form = ObservatoryForm()
    if form.validate_on_submit():
        observatory = Observatory()
        form.populate_obj(observatory)
        observatory.altitude = services.get_elevation(observatory.latitude, observatory.longitude)
        observatory.timezone = services.get_timezone(observatory.latitude, observatory.longitude)
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

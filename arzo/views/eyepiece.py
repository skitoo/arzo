# -*- coding: utf-8 -*-

from flask import render_template, url_for, redirect, flash
from arzo import app, db, logger
from arzo.models import Eyepiece
from arzo.forms import EyepieceForm


@app.route('/eyepieces')
def eyepieces():
    eyepieces = Eyepiece.query.all()
    return render_template(
        'eyepiece/index.html',
        eyepieces=eyepieces,
        title='Occulaires',
        breadcrumb=[
            (url_for('index'), 'Accueil'),
            (url_for('eyepieces'), 'Occulaires'),
        ]
    )


@app.route('/eyepiece/<int:eyepiece_id>')
def show_eyepiece(eyepiece_id):
    eyepiece = Eyepiece.query.get_or_404(eyepiece_id)
    return render_template(
        'eyepiece/show.html',
        eyepiece=eyepiece,
        title='Occulaire - %s' % eyepiece.name,
        breadcrumb=[
            (url_for('index'), 'Accueil'),
            (url_for('eyepieces'), 'Occulaires'),
            (url_for('edit_eyepiece', eyepiece_id=eyepiece_id), eyepiece.name),
        ]
    )


@app.route('/eyepiece', methods=('GET', 'POST'))
def new_eyepiece():
    form = EyepieceForm()
    if form.validate_on_submit():
        eyepiece = Eyepiece()
        form.populate_obj(eyepiece)
        db.session.add(eyepiece)
        db.session.commit()
        return redirect(url_for('eyepieces'))
    return render_template(
        'eyepiece/edit.html',
        form=form,
        title='Occulaires',
        breadcrumb=[
            (url_for('index'), 'Accueil'),
            (url_for('eyepieces'), 'Occulaires'),
            (url_for('new_brand'), 'Nouvel occulaire'),
        ]
    )


@app.route('/eyepiece/<int:eyepiece_id>/edit', methods=('GET', 'POST'))
def edit_eyepiece(eyepiece_id):
    eyepiece = Eyepiece.query.get_or_404(eyepiece_id)
    form = EyepieceForm(obj=eyepiece)
    if form.validate_on_submit():
        form.populate_obj(eyepiece)
        db.session.merge(eyepiece)
        db.session.commit()
        flash(u'Occulaire sauvegardé avec succès', 'success')
        return redirect(url_for('eyepieces'))
    return render_template(
        'eyepiece/edit.html',
        form=form,
        title='Occulaire - %s' % eyepiece.name,
        breadcrumb=[
            (url_for('index'), 'Accueil'),
            (url_for('eyepieces'), 'Occulaires'),
            (url_for('show_eyepiece', eyepiece_id=eyepiece_id), eyepiece.name),
            (None, u'Édition')
        ]
    )


@app.route('/eyepiece/<int:eyepiece_id>/delete')
def delete_eyepiece(eyepiece_id):
    eyepiece = Eyepiece.query.get_or_404(eyepiece_id)
    db.session.delete(eyepiece)
    db.session.commit()
    flash(u'Occulaire supprimé avec succès', 'success')
    return redirect(url_for('eyepieces'))

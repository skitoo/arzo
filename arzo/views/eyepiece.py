# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, flash, request
from arzo import app, db
from arzo.models import Eyepiece
#from arzo.forms import ObservatoryForm


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

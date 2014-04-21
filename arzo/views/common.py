# -*- coding: utf-8 -*-

from flask import render_template, url_for
from arzo import app


@app.route('/')
def index():
    return render_template(
        'index.html',
        breadcrumb=[
            (url_for('index'), 'Accueil')
        ]
    )

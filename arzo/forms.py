# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms_alchemy import model_form_factory
from arzo.models import Observatory, Brand, Eyepiece
from arzo import db


ModelForm = model_form_factory(Form)


class ObservatoryForm(ModelForm):
    class Meta:
        model = Observatory
        exclude = ['update_at', 'timezone', 'altitude']


class BrandForm(ModelForm):
    class Meta:
        model = Brand
        exlude = ['update_at']


class EyepieceForm(ModelForm):
    class Meta:
        model = Eyepiece
        exclude = ['update_at']
    brand = QuerySelectField(get_label='name', query_factory=lambda: db.session.query(Brand))

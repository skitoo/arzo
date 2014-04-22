# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms_alchemy import model_form_factory
from arzo.models import Observatory, Brand

ModelForm = model_form_factory(Form)


class ObservatoryForm(ModelForm):
    class Meta:
        model = Observatory
        exclude = ['update_at', 'timezone', 'altitude']



class BrandForm(ModelForm):
    class Meta:
        model = Brand
        exlude = ['update_at']

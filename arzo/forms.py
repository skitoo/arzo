# -*- coding: utf-8 -*-

from flask.ext.wtf import Form
from wtforms_alchemy import model_form_factory
from arzo.models import Observatory

ModelForm = model_form_factory(Form)


class ObservatoryForm(ModelForm):
    class Meta:
        model = Observatory
        exclude = ['update_at']


# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, flash, request
from arzo import app, db
from arzo.models import Observatory, Brand
from arzo.forms import ObservatoryForm, BrandForm


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

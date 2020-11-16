from flask import Flask
from app import app
from app import db
from app.models import Commander, RecsText

import json
from flask import render_template
from flask import request, redirect, url_for
from flask_bootstrap import Bootstrap 
from markupsafe import escape
from app.forms import ChooseForm, CommanderForm
from app.com_data import RECS, NOMBRES, COMS

from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#Bootstrap(app)

@app.route("/recomendaciones/<string:commander>", methods=["GET", "POST"])
def com_recoms(commander):
    for i in RECS:
        if i["commander"] == commander:
            recoms = i["recomendaciones"]
    for i in COMS:
        if i["name"] == commander:
            try:
                pic_commander = i["image_uris"]["normal"]
            except:
                pic_commander = ""
    return render_template(
        "recomendaciones.html",
        commander=commander,
        recoms=recoms,
        pic_commander=pic_commander
    )


@app.route("/", methods=["GET", "POST"])
def comandante():
    com_form = ChooseForm()
    if com_form.validate_on_submit() and com_form.submit:
        commander = com_form.commander.data
        return redirect(url_for("com_recoms", commander=commander))
    return render_template(
        "index.html",
        com_form=com_form
    )

@app.route("/prueba/", methods=["GET", "POST"])
def prueba():
    com_form = CommanderForm()
    comando = Commander.query.all()

    if com_form.validate_on_submit() and com_form.submit:
        commander = com_form.commander.data
        return redirect(url_for("rec_prueba", commander=commander))
    return render_template(
        "prueba.html",
        com_form=com_form,
        comando=comando
    )

@app.route("/rec-prueba/<string:commander>", methods=["GET", "POST"])
def rec_prueba(commander):
    commander_data = Commander.query.filter_by(card_id=commander).first_or_404()
    recomendaciones = RecsText.query.join(Commander).filter(RecsText.card_id == commander).all()

    return render_template(
        "rec-prueba.html", 
        commander_data=commander_data,
        recomendaciones=recomendaciones
    )

import json
from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
from flask_bootstrap import Bootstrap 
from markupsafe import escape
from forms import ChooseForm
from com_data import RECS, NOMBRES, COMS


app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = "cv9ubvwern4856dfgnb34jnc43m90kvdf890dsfauzd"


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


if __name__ == "__main__":
    app.run()

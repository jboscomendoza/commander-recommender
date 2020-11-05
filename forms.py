from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length
import json


with open('recomendaciones.json') as json_file:
    RECS = json.load(json_file, encoding="utf-8")


NOMBRES = [i["commander"] for i in RECS]


class ChooseForm(FlaskForm):
    commander = SelectField(u"Commander", choices=NOMBRES)
    submit = SubmitField("Mostrar recomendaciones")


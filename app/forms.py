from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length
import json
from app.com_data import NOMBRES

from app import db
from app.models import Commander

commander_results = Commander.query.all()
COMANCHES = []
for i in commander_results:
    COMANCHES.append((i.card_id, i.card_name))


class ChooseForm(FlaskForm):
    commander = SelectField(u"Commander", choices=NOMBRES)
    submit = SubmitField("Mostrar recomendaciones")

class CommanderForm(FlaskForm):
    commander = SelectField(u"Commander", choices=COMANCHES)
    submit = SubmitField("Mostrar recomendaciones")
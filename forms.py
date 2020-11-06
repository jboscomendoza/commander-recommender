from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired, Email, Length
import json
from com_data import NOMBRES

class ChooseForm(FlaskForm):
    commander = SelectField(u"Commander", choices=NOMBRES)
    submit = SubmitField("Mostrar recomendaciones")


from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SubmitField, TimeField
from wtforms.validators import DataRequired
from wtforms.widgets.html5 import NumberInput, TimeInput, DateInput, DateTimeInput

from datetime import time, date, timedelta, datetime

class PlotForm(FlaskForm):
    date = DateField(label='Date', default=datetime.utcnow()-timedelta(days=1), widget=DateInput(), validators=[DataRequired(message='enter date')])#, render_kw={'type': 'date'})
    time = TimeField(label='Time', default=time(hour=0, minute=0), widget=TimeInput(), validators=[DataRequired(message='enter time')], description='TEST')
    length = StringField(label='Length', default=24,widget=NumberInput(min=1, max=24), validators=[DataRequired(message='enter length')], render_kw={'size':1})
    plot = SubmitField()
    download = SubmitField()
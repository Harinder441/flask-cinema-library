from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,IntegerField,DecimalField
from wtforms.validators import DataRequired,url


class AddMovie(FlaskForm):
    title = StringField('Movie title', validators=[DataRequired()])
    submit = SubmitField("Search")


class RateMovie(FlaskForm):
    rating = DecimalField('Rating', validators=[DataRequired()])
    review = StringField(' Review')
    submit = SubmitField("Add")

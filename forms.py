from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4)])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4)])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Register')

class BeritaForm(FlaskForm):
    judul = StringField('Judul', validators=[InputRequired()])
    isi = TextAreaField('Isi', validators=[InputRequired()])
    submit = SubmitField('Simpan')

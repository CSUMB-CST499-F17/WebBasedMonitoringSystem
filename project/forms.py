#project/forms.py
#class for future account creation and login form

from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email
 
 
class RegisterForm(Form):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=64)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=1, max=18)])
    confirm = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])

class LoginForm(Form):
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=64)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=1, max=18)])

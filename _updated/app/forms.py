from flask_wtf import Form
from wtforms import TextField, PasswordField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length


class RegisterForm(Form):
    name = TextField(
        'Location', validators=[DataRequired(), Length(min=6, max=40)]
    )
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
        EqualTo('password', message='Passwords must match')]
    )
    track = TextField(
        'Select Track', validators
    )


class LoginForm(Form):
    name = TextField('Location', [DataRequired()])
    password = TextField('Number of Hours', [DataRequired()])
    track = SelectField('Select Track', choices = ['Buildings and Structures', 'Gardens', 'Historic and Protected Sites', 'Monuments and Memorials', 'Natural', 'Parks', 'Pub Crawl', 'Clubbing'])


class ForgotForm(Form):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )

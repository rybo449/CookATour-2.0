from flask_wtf import Form
from wtforms import TextField, PasswordField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length

# Set your classes here.


class RegisterForm(Form):
    name = TextField(
        'Username', validators=[DataRequired(), Length(min=6, max=25)]
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


class LoginForm(Form):
    name = TextField('Select Start Location', [DataRequired()])
    hours = TextField('How many hours do you have', [DataRequired()])
    #track = SelectField('Select Track', choices = [(0,'Buildings and Structures'), (1,'Gardens'), (2,'Historic and Protected Sites'), (3,'Monuments and Memorials'), (4,'Natural'), (5,'Parks'), (6,'Pub Crawl'), (7,'Clubbing')])
    track = SelectField('Select Track', choices = [(0,'Buildings and Structures'), (1,'Gardens'), (2,'Historic and Protected Sites'), (3,'Monuments and Memorials'), (4,'Natural'), (5,'Parks'), (6,'Pub Crawl'), (7,'Clubbing')])

    transport = SelectField('Select Mode of Transport', choices = [('driving','driving'), ('walking','walking'), ('bicycling','bicycling'), ('transit','transit')])


class ForgotForm(Form):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )

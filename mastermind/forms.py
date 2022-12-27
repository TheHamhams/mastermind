from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class UserLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField('Submit')
    
class UserSignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(max=15)])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit_button = SubmitField('Submit')
    
class UserEmailUpdate(FlaskForm):
    email = StringField('Email', validators=[Email(), DataRequired()])
    submit_button = SubmitField('Update Email')
    
class UserUsernameUpdate(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=15)])
    submit_button = SubmitField('Update Username')
    
class UserPasswordUpdate(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit_button = SubmitField('Update Password')
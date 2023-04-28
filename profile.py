from flask import Flask, render_template, redirect, request
import datetime
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, EmailField, StringField, IntegerField
from wtforms import SelectMultipleField, DateTimeField, SelectField
from wtforms.validators import DataRequiredl

app = Flask(__name__)


@app.route('/profile')
def profile():
    # if current_user.is_authenticated:
    #     user = current_user()
    #     name = user.name
    #     surname = user.surname
    #     email = user.email
    # else:
    #     pass
    # return render_template('profile.html', form=form, name=name, surname=surname, email=email)
    user = User()
    name = user.name
    surname = user.surname
    email = user.surname
    # return render_template('profile.html', name='name', surname='surname', email='email')
    return render_template('profile.html', name=name, surname=surname, email=email)

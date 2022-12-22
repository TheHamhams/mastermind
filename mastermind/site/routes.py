from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
# from models import db
import json



site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/', methods=['GET', 'POST'])
# @login_required
def home():

    return render_template('home.html', title="Home", user=current_user)
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from mastermind.models import User, db, check_password_hash, users_schema

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from mastermind.forms import UserLoginForm, UserSignupForm

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/admin')
def admin():
    users = User.query.all()
    
    result = users_schema.dump(users)
    return jsonify(result)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    
    form = UserLoginForm()
    
    
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            
            user = User.query.filter(User.email == email).first()
           
            if user and check_password_hash(user.password, password):
                login_user(user)
            
                flash(f'You have successfully logged in {email}', 'auth-success')
                return redirect(url_for('site.home'))
            else:
                flash('User info not found', 'auth-failed')
                return redirect(url_for('auth.login'))
    except:
        raise Exception('Invalid form data: Please check your form')
    return render_template('login.html', title="Login", form=form, user=current_user)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserSignupForm()
    
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            password_confirm = form.password_confirm.data
            
            if password != password_confirm:
                flash('Passwords do not match')
                return redirect(url_for('auth.signup'))
            
            user = User.query.filter_by(email=email).first()
            
            if user:
                flash('Email already exists', 'auth-failed')
                return redirect(url_for('auth.signup'))

            user = User(email=email, username=username, password=password)
            
            db.session.add(user)
            db.session.commit()
            
            flash(f"You have successfully created a user account for { email }", 'success')
            return redirect(url_for('auth.login'))
        
    except:
        raise Exception('Invalid form data: Please check your form')
    
    return render_template('signup.html', title="Sign Up", form=form, user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))
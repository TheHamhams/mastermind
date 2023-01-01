from flask import Blueprint, render_template, request, flash, redirect, url_for
from mastermind.models import User, db, check_password_hash

from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from mastermind.forms import UserLoginForm, UserSignupForm, UserEmailUpdate, UserUsernameUpdate, UserPasswordUpdate

auth = Blueprint('auth', __name__, template_folder='auth_templates')

# Profile page
@auth.route('/profile', methods=['GET', 'POST'])
def profile():
    # Forms for updating profile info
    email_form = UserEmailUpdate()
    username_form = UserUsernameUpdate()
    password_form = UserPasswordUpdate()

    user = User.query.filter_by(email=current_user.email).first()

    # Variables
    score = user.high_score
    username = user.username
    email = user.email
    current_streak = user.current_streak
    highest_streak = user.highest_streak

    # Check if email form was submitted
    if request.method == 'POST' and email_form.validate_on_submit():
        new_email = email_form.email.data

        # Check if email already exists in database
        check_email = User.query.filter(User.email == new_email).first()
        if check_email:
            flash('Email already exists', category='error')

        # Update email
        else:
            user.email = new_email
            db.session.commit()

        return redirect(url_for('auth.profile'))

    # Check if username form was submitted
    if request.method == 'POST' and username_form.validate_on_submit():
        new_username = username_form.username.data

        # Check if username already exists in database
        check_username = User.query.filter(User.username == new_username).first()
        if check_username:
            flash('Username already exists', category='error')
        # Update username
        else:
            user.username = new_username
            db.session.commit()
            return redirect(url_for('auth.profile'))

    # Check if password form was submitted
    if request.method == 'POST' and password_form.validate_on_submit():
        new_password = password_form.password.data

        # Check if password and password confirm match
        if new_password != password_form.password_confirm.data:
            flash('Passwords do not match', category='error')
            return redirect(url_for('auth.profile'))

        # Update password
        else:
            user.password = generate_password_hash(new_password)
            db.session.commit()
            return redirect(url_for('auth.profile'))

    return render_template('profile.html', title='Profile', score=score, username=username, email=email, current_streak=current_streak, highest_streak=highest_streak, email_form=email_form, username_form=username_form, password_form=password_form)

# Login page
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = UserLoginForm()

    if form.validate_on_submit():
        # Form data
        email = form.email.data
        password = form.password.data

        user = User.query.filter(User.email == email).first()

        # validate user password and login user
        if user and check_password_hash(user.password, password):
            login_user(user)

            flash(f'You have successfully logged in {email}', category='success')
            return redirect(url_for('site.home'))
        else:
            flash('Incorrect login infromation, please try again', category='error')
            return redirect(url_for('auth.login'))


    return render_template('login.html', title="Login", form=form, user=current_user)

# Signup page
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserSignupForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            # Form data
            email = form.email.data
            username = form.username.data
            password = form.password.data
            password_confirm = form.password_confirm.data

            # Check if passwords match
            if password != password_confirm:
                flash('Passwords do not match', category='error')
                return redirect(url_for('auth.signup'))

            # Check if email is already in database
            email_check = User.query.filter_by(email=email).first()
            if email_check:
                flash('Email already exists', category='error')
                return redirect(url_for('auth.signup'))

            # Check if username is already in database
            username_check = User.query.filter_by(username=username).first()
            if username_check:
                flash('Username already exists', category='error')
                return redirect(url_for('auth.signup'))

            # Add user to database
            user = User(email=email, username=username, password=password)

            db.session.add(user)
            db.session.commit()

            flash(f"You have successfully created a user account for { email }", 'success')
            return redirect(url_for('auth.login'))

    except:
        flash('Invalid form data: Please check your form')

    return render_template('signup.html', title="Sign Up", form=form, user=current_user)

# Logout
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))
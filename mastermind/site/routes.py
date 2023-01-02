from flask import Blueprint, render_template
from flask_login import current_user
from mastermind.game.routes import create_leaderboard, create_streakboard

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/', methods=['GET', 'POST'])
def home():
    home_leaderboard = create_leaderboard()
    home_streakboard = create_streakboard()

    return render_template('home.html', title="Home", user=current_user, leaderboard=home_leaderboard, streakboard=home_streakboard)


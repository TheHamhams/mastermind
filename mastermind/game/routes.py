from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from mastermind.models import User, Scores, Streaks, db
import requests
import dataset
import secrets

game = Blueprint('game', __name__, template_folder='game_templates')

# Global variables
guesses = 10
solution = []
token = ''
attempts = []
leaderboard = []
streakboard = []

# Global functions
def reset():
    '''
    Create a new game state by resetting global variables
    '''
    global solution, guesses, attempts, token
    guesses = 10
    solution = []
    token = ''
    attempts = []

def create_leaderboard():
    '''
    Generate and return updated leaderboard
    '''
    global leaderboard
    leaderboard = []
    con = dataset.connect('sqlite:///instance/site.db')
    scores = con.query('SELECT username, score, id FROM scores ORDER BY score DESC')

    for row in scores:
        leaderboard.append([row['username'], row['score'], row['id']])

    return leaderboard

def create_streakboard():
    '''
    Generate and return updated streakboard
    '''
    global streakboard
    streakboard = []
    con = dataset.connect('sqlite:///instance/site.db')
    scores = con.query('SELECT username, streak, id FROM streaks ORDER BY streak DESC')

    for row in scores:
        streakboard.append([row['username'], row['streak'], row['id']])

    return streakboard

@game.route('/start', methods=['GET', 'POST'])
@login_required
def start():
    global solution, guesses, attempts
    reset()

    return render_template('start.html', title='Start', user=current_user)

# Run game based on difficulty
@game.route('/game/<int:num>', methods=['GET', 'POST'])
@login_required
def run(num):
    global solution, token, guesses, attempts
    nums = 0
    spots = 0

    # Create solution
    if solution == []:
        r = requests.get(f'https://www.random.org/integers/?num={num}&min=0&max=7&col=1&base=10&format=plain&rnd=new')
        data = r.text

        solution = data.split('\n')
        solution.pop()

        for idx in range(len(solution)):
            solution[idx] = int(solution[idx])

        # Create verification token for win page
        token = secrets.token_urlsafe(16)

    # Game functionality
    if request.method == "POST":
        guesses -= 1

        # Create guess list
        guess = [int(request.form.get('num1')), int(request.form.get('num2')), int(request.form.get('num3'))]
        if num > 3:
            guess.append(int(request.form.get('num4')))
        if num > 4:
            guess.append(int(request.form.get('num5')))

        # Check for correct solution
        if guess == solution:
            score = guesses * num
            return redirect(url_for('game.win', score=score, verify=token))

        # Check for correct locations
        for idx in range(len(guess)):
            if guess[idx] == solution[idx]:
                spots += 1

        # Check for correct numbers
        temp = solution.copy()
        for number in guess:
            if number in temp:
                nums += 1
                temp.remove(number)

        # Create feedback
        if nums == 0 and spots == 0:
            feedback = "all incorrect"
        else:
            feedback = f"{nums} correct number(s) and {spots} correct location(s)"
        attempts.insert(0, f'{guess} {feedback}')

        nums = 0
        spots = 0

        # Loss condition
        if guesses == 0:
            return redirect(url_for('game.lose'))

    return render_template('run.html', title='Game', user=current_user, solution=solution, guesses=guesses, attempts=attempts, nums=nums, spots=spots, num=num)

# Win condition
@game.route('/win/<int:score>/<string:verify>')
@login_required
def win(score, verify):
    global solution, token, guesses, leaderboard
    # Check for cheating
    if verify != token or token == '':
        reset()
        return redirect(url_for('game.cheat'))

    # Variables
    new_high_score = False
    new_high_streak = False
    new_personal_high = False
    new_score_id = 0
    user = User.query.filter_by(email=current_user.email).first()

    # Add to current streak
    user.current_streak += 1
    db.session.commit()
    current_streak = user.current_streak

    # Create leaderboard
    create_leaderboard()

    # Check is current streak is higher than highest streak
    if user.current_streak > user.highest_streak:
        # Replace highest_streak with streak
        user.highest_streak = user.current_streak
        new_high_streak = True

    # Check for user high score
    if score > user.high_score:
        user.high_score=score
        db.session.commit()
        new_personal_high=True

    # Check if there is room on the leaderboard
    if len(leaderboard) < 5:
        new = Scores(username=user.username, user_id=user.id, score=score)
        db.session.add(new)
        db.session.commit()
        new_high_score = True
        new_score_id = new.id

        # Insert user score into leaderboard
        leaderboard.append([user.username, score, new_score_id])
        leaderboard.sort(key=lambda x: x[1], reverse=True)

    # Check leaderboard if it is full
    else:

        # Remove lowest leaderboard score if user score is larger
        if score > leaderboard[-1][1]:
            removed = leaderboard.pop()

            # Add new score to db and remove lowest score
            new_leaderboard_score = Scores(user.username, user.id, score)
            db.session.add(new_leaderboard_score)
            leaderboard_score_to_remove = Scores.query.get(removed[2])
            db.session.delete(leaderboard_score_to_remove)
            db.session.commit()
            new_score_id = new_leaderboard_score.id
            new_high_score=True

            # Insert user score into leaderboard
            leaderboard.append([user.username, score, new_score_id])
            leaderboard.sort(key=lambda x: x[1], reverse=True)

    # Determine total guesses for front end
    count = 10 - guesses
    reset()

    return render_template('win.html', user=current_user, title='WINNER', count=count, score=score, new_high_score=new_high_score, leaderboard=leaderboard, new_personal_high=new_personal_high, new_score_id=new_score_id, current_streak=current_streak, new_high_streak=new_high_streak)

# Loss condition
@game.route('/lose')
@login_required
def lose():
    # Variables
    global solution, streakboard
    user = User.query.filter_by(email=current_user.email).first()
    new_high_streak = False
    streak = user.current_streak

    # Create streakboard
    create_streakboard()

    # Check is current streak is higher than highest streak
    if streak > user.highest_streak:
        # Replace highest_streak with streak
        user.highest_streak = streak
        new_high_streak = True

    # Check if there is room on the streakboard
    if len(streakboard) < 5:
        new = Streaks(username=user.username, user_id=user.id, streak = streak)
        db.session.add(new)
        db.session.commit()
        new_streak_id = new.id

        # Insert user streak into streakboard
        streakboard.append([user.username, streak, new_streak_id])
        streakboard.sort(key=lambda x: x[1], reverse=True)

    else:
        # Remove lowest streakboard score if user score is larger
        if streak > streakboard[-1][1]:
            removed = streakboard.pop()

            # Add new streak to db and remove lowest score
            new_streakboard_score = Streaks(user.username, user.id, streak)
            db.session.add(new_streakboard_score)
            streakboard_score_to_remove = Streaks.query.get(removed[2])
            db.session.delete(streakboard_score_to_remove)
            db.session.commit()
            new_streak_id = new_streakboard_score.id

            # Insert user score into streakboard
            streakboard.append([user.username, streak, new_streak_id])
            streakboard.sort(key=lambda x: x[1], reverse=True)

    # Reset user streak
    user.current_streak = 0
    db.session.commit()

    return render_template('lose.html', title='Loser', user=current_user, solution=solution, streak = streak, new_high_streak=new_high_streak, new_streak_id=new_streak_id, streakboard=streakboard)

# Cheat page
@game.route('/cheat')
def cheat():
    return render_template('cheat.html', title='Cheat')
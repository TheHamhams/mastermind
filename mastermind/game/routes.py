from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from mastermind.models import User, Scores, db, scores_schema
from sqlalchemy import func
import requests
import json
import dataset
# from stuf import stuf

game = Blueprint('game', __name__, template_folder='game_templates')

# Global variables
guesses = 10
solution = []
attempts = []
leaderboard = []

# Global functions
def reset():
    global solution, guesses, attempts
    guesses = 10
    solution = []
    attempts = []
    
def create_leaderboard():
    global leaderboard
    leaderboard = []
    con = dataset.connect('sqlite:///instance\site.db')
    scores = con.query('SELECT username, score, id FROM scores ORDER BY score DESC')
    for row in scores:
        leaderboard.append([row['username'], row['score'], row['id']])
    return leaderboard

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
    global solution, guesses, attempts
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
            return redirect(url_for('game.win', score=score))
        
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
@game.route('/win/<int:score>')
@login_required
def win(score):
    global guesses, leaderboard
    new_high_score = False
    new_personal_high = False
    new_score_id = 0
    user = User.query.filter_by(email=current_user.email).first()
    create_leaderboard()
    
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
            for idx in range(4):
                if score > leaderboard[idx][1]:
                    leaderboard.insert(idx, [user.username, score, new_score_id])
            
    # Determine total guesses for front end
    count = 10 - guesses
    
    return render_template('win.html', user=current_user, title='WINNER', count=count, score=score, new_high_score=new_high_score, leaderboard=leaderboard, new_personal_high=new_personal_high, new_score_id=new_score_id)

# Loss condition
@game.route('/lose')
@login_required
def lose():
    global solution
    return render_template('lose.html', title='Loser', user=current_user, solution=solution)
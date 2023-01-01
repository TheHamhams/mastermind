from flask import Blueprint, jsonify
from mastermind.models import db, Scores, User, Streaks
from mastermind.helpers import secret_key_required

api = Blueprint('api', __name__, url_prefix='/admin')

# DELETE score
@api.route('/scores/<int:id>', methods=['DELETE'])
@secret_key_required
def delete_score(current_secret_key, id):
    score = Scores.query.get(id)

    db.session.delete(score)
    db.session.commit()

    return jsonify({})

# DELETE streak
@api.route('/streaks/<int:id>', methods=['DELETE'])
@secret_key_required
def delete_streak(current_secret_key, id):
    streak = Streaks.query.get(id)

    db.session.delete(streak)
    db.session.commit()

    return jsonify({})

# DELETE user
@api.route('/<string:username>', methods=['DELETE'])
@secret_key_required
def delete(current_secret_key, username):
    user = User.query.filter_by(username = username).first()

    db.session.delete(user)
    db.session.commit()

    return jsonify({})
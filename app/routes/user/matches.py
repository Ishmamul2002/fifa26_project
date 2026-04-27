from flask import Blueprint, render_template

user_matches_bp = Blueprint('user_matches', __name__, url_prefix='/user/matches')

@user_matches_bp.route('/list')
def list():
    return render_template('user/matches/list.html')
from flask import Blueprint, render_template

user_statistics_bp = Blueprint('user_statistics', __name__, url_prefix='/user')

@user_statistics_bp.route('/statistics')
def statistics():
    return render_template('user/statistics.html')
from flask import Blueprint, render_template
from flask_login import login_required

user_analytics_bp = Blueprint('user_analytics', __name__, url_prefix='/user/analytics')

@user_analytics_bp.route('/')
@login_required
def analytics():
    return render_template('user/analytics.html')
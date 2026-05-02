from flask import Blueprint, render_template
from flask_login import login_required

analytics_bp = Blueprint('analytics', __name__, url_prefix='/user')

@analytics_bp.route('/analytics')
@login_required
def analytics():
    from app.models import LiveMatchAnalytics
    live_data = LiveMatchAnalytics.query.all()
    return render_template('user/analytics.html', live_data=live_data)
from flask import Blueprint, render_template
from flask_login import login_required

user_reports_bp = Blueprint('user_reports', __name__, url_prefix='/user/reports')

@user_reports_bp.route('/')
@login_required
def reports():
    return render_template('user/reports.html')
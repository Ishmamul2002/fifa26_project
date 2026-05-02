from flask import Blueprint, redirect, url_for
from flask_login import current_user

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Force show login page first"""
    return redirect(url_for('auth.login')) # This line is important
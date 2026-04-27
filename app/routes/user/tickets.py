from flask import Blueprint, render_template

user_tickets_bp = Blueprint('user_tickets', __name__, url_prefix='/user/tickets')

@user_tickets_bp.route('/booking')
def booking():
    return render_template('user/tickets/booking.html')
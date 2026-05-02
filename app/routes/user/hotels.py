from flask import Blueprint, render_template

user_hotels_bp = Blueprint('user_hotels', __name__, url_prefix='/user/hotels')

@user_hotels_bp.route('/booking')
def booking():
    return render_template('user/hotels/booking.html')
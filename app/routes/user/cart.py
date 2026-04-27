from flask import Blueprint, render_template

user_cart_bp = Blueprint('user_cart', __name__, url_prefix='/user')

@user_cart_bp.route('/cart')
def cart():
    return render_template('user/cart.html')
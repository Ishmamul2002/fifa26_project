from flask import Blueprint, render_template, redirect, url_for
from ...models import Match

user_tickets_bp = Blueprint('user_tickets', __name__, url_prefix='/user')

@user_tickets_bp.route('/tickets')
def user_tickets():
    return redirect(url_for('main.upcoming_matches'))


@user_tickets_bp.route('/book-ticket/<int:match_id>')
def book_ticket(match_id):
    match = Match.query.get_or_404(match_id)
    return render_template('public/book_ticket.html', match=match)
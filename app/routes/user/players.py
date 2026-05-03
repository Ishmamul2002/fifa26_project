from flask import Blueprint, render_template, request
from flask_login import login_required
from ...models import Player, Team

players_bp = Blueprint('players', __name__, url_prefix='/user')

@players_bp.route('/players')
@login_required
def explore_players():
    """Player Cards List"""
    search = request.args.get('search')
    team_id = request.args.get('team_id', type=int)
    position = request.args.get('position')

    query = Player.query

    if search:
        query = query.filter(Player.name.ilike(f'%{search}%'))
    if team_id:
        query = query.filter_by(team_id=team_id)
    if position:
        query = query.filter_by(position=position)

    players = query.order_by(Player.name).all()
    teams = Team.query.all()

    return render_template('user/players/explore.html', 
                           players=players, 
                           teams=teams,
                           search=search)


@players_bp.route('/player/<int:player_id>')
@login_required
def player_detail(player_id):
    """Single Player Profile"""
    player = Player.query.get_or_404(player_id)
    return render_template('user/players/detail.html', player=player)
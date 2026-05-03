from flask import Blueprint, render_template
from ..models import Team, Player

fanzone_bp = Blueprint('fanzone', __name__, url_prefix='/fanzone')

@fanzone_bp.route('/')
def index():
    popular_teams = Team.query.order_by(Team.ranking.asc()).limit(8).all()
    popular_players = Player.query.order_by(Player.goals_scored.desc()).limit(8).all()
    
    return render_template('fanzone/index.html',
                         popular_teams=popular_teams,
                         popular_players=popular_players)
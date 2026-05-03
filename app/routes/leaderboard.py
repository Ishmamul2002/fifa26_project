from flask import Blueprint, render_template
from ..models import Team, Player
from sqlalchemy import func

leaderboard_bp = Blueprint('leaderboard', __name__, url_prefix='/user/leaderboard')

@leaderboard_bp.route('/')
def leaderboard_index():
    """Main Leaderboard Page"""
    
    # Group Standings
    all_teams = Team.query.order_by(Team.group_name, Team.ranking.asc()).all()
    groups = {}
    for team in all_teams:
        if team.group_name not in groups:
            groups[team.group_name] = []
        groups[team.group_name].append(team)

    # Top 16 Ranked Teams
    top_teams = Team.query.order_by(Team.ranking.asc()).limit(16).all()

    # Top Scorers from Players Table
    top_scorers = Player.query.order_by(Player.goals_scored.desc())\
                             .limit(10).all()

    return render_template('leaderboard/index.html',
                         groups=groups,
                         top_teams=top_teams,
                         top_scorers=top_scorers)
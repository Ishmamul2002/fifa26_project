# app/routes/user/teams.py
from flask import Blueprint, render_template, request
from flask_login import login_required
from ...models import Team, Match
from ... import db

teams_bp = Blueprint('teams', __name__, url_prefix='/user')

@teams_bp.route('/teams')
@login_required
def explore_teams():
    """Team Hub - Explore All Teams"""
    group = request.args.get('group')
    search = request.args.get('search')

    query = Team.query

    if group:
        query = query.filter_by(group_name=group.upper())
    if search:
        query = query.filter(
            Team.name.ilike(f'%{search}%') | 
            Team.country.ilike(f'%{search}%')
        )

    teams = query.order_by(Team.name).all()

    # Get unique groups for filter
    groups = [g[0] for g in db.session.query(Team.group_name).distinct().all() if g[0]]

    featured_teams = Team.query.limit(6).all()

    return render_template('user/teams/explore.html', 
                           teams=teams,
                           featured_teams=featured_teams,
                           groups=groups,
                           selected_group=group,
                           search=search)


@teams_bp.route('/team/<int:team_id>')
@login_required
def team_detail(team_id):
    """Single Team Detail Page"""
    team = Team.query.get_or_404(team_id)
    
    upcoming_matches = Match.query.filter(
        (Match.team_a_id == team_id) | (Match.team_b_id == team_id)
    ).order_by(Match.date.asc()).limit(6).all()

    return render_template('user/teams/detail.html', 
                           team=team, 
                           upcoming_matches=upcoming_matches)
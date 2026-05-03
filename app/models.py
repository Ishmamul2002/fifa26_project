from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# ========================= USER MODEL =========================
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    phone = db.Column(db.String(20))
    country = db.Column(db.String(60))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # IMPORTANT: Add this method
    def get_id(self):
        return str(self.user_id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin_user(self):
        return self.is_admin
    
# ========================= OTHER MODELS =========================
class Team(db.Model):
    __tablename__ = 'teams'   
    team_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(60), nullable=False)
    # logo = db.Column(db.String(255))   # Comment this out if column doesn't exist
    group_name = db.Column(db.String(1))

class Stadium(db.Model):
    __tablename__ = 'stadiums'
    stadium_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    capacity = db.Column(db.Integer)
    location = db.Column(db.String(150))
    image = db.Column(db.String(255))

class Match(db.Model):
    __tablename__ = 'matches'
    
    match_id = db.Column(db.Integer, primary_key=True)
    date = db.Column('match_date', db.Date, nullable=False)
    time = db.Column('match_time', db.Time, nullable=False)
    team_a_id = db.Column('team1_id', db.Integer, db.ForeignKey('teams.team_id'))
    team_b_id = db.Column('team2_id', db.Integer, db.ForeignKey('teams.team_id'))    
    stadium_id = db.Column(db.Integer, db.ForeignKey('stadiums.stadium_id'))
    venue = db.Column(db.String(255))
    status = db.Column(db.String(50), default='scheduled')
    # Relationships (optional but useful)
    team_a = db.relationship('Team', foreign_keys=[team_a_id])
    team_b = db.relationship('Team', foreign_keys=[team_b_id])
    stadium = db.relationship('Stadium')


class Ticket(db.Model):
    __tablename__ = 'tickets'
    __table_args__ = {'extend_existing': True}

    ticket_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.match_id'), nullable=False)
    
    ticket_type = db.Column(db.String(50), nullable=True)
    price = db.Column(db.Float, nullable=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)     # ← Must have this
    seat_number = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(20), default='active')
    qr_code = db.Column(db.String(255), nullable=True)

    # Relationships
    match = db.relationship('Match', backref='tickets')

class Cart(db.Model):
    __tablename__ = 'cart'
    
    cart_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    item_type = db.Column(db.String(50), nullable=True)
    item_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    price_per_ticket = db.Column(db.Float, nullable=True)
    total_price = db.Column(db.Float, nullable=True)

class Booking(db.Model):
    __tablename__ = 'bookings'
    booking_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.ticket_id'), nullable=True)
    room_booking_id = db.Column(db.Integer, db.ForeignKey('room_bookings.room_booking_id'), nullable=True)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')

class Payment(db.Model):
    __tablename__ = 'payments'
    
    payment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.ticket_id'), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='completed')
    transaction_id = db.Column(db.String(100), nullable=True)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='payments')
    ticket = db.relationship('Ticket', backref='payment')


class LiveMatchAnalytics(db.Model):
    __tablename__ = 'live_match_analytics'
    
    analytics_id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.match_id'))
    current_minute = db.Column(db.Integer)
    possession_team1 = db.Column(db.Integer)
    possession_team2 = db.Column(db.Integer)
    team1_score = db.Column(db.Integer)
    team2_score = db.Column(db.Integer)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)







print("✅ All models loaded successfully!")
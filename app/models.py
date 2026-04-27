from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# ========================= USER MODEL =========================
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(60))
    phone = db.Column(db.String(20))
    role = db.Column(db.String(20), default='user')
    total_purchases = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'

# ========================= OTHER MODELS =========================
class Team(db.Model):
    __tablename__ = 'teams'
    team_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(60), nullable=False)
    logo = db.Column(db.String(255))
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
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    team_a_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'))
    team_b_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'))
    stadium_id = db.Column(db.Integer, db.ForeignKey('stadiums.stadium_id'))
    tournament_id = db.Column(db.Integer)
    winner_id = db.Column(db.Integer, db.ForeignKey('teams.team_id'))

class Ticket(db.Model):
    __tablename__ = 'tickets'
    ticket_id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.match_id'))
    seat_number = db.Column(db.String(20))
    ticket_type = db.Column(db.String(20))
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='available')

class Hotel(db.Model):
    __tablename__ = 'hotels'
    hotel_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    price_per_night = db.Column(db.Float, nullable=False)
    distance_from_stadium = db.Column(db.Float)
    availability = db.Column(db.Integer, default=100)
    rating = db.Column(db.Float, default=4.5)
    image = db.Column(db.String(255))

class Cart(db.Model):
    __tablename__ = 'cart'
    cart_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    item_type = db.Column(db.String(20), nullable=False)   # 'ticket' or 'hotel'
    item_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, default=1)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

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
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.booking_id'))
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(50))  # card, bkash, nagad, cash, paypal
    status = db.Column(db.String(20), default='pending')
    transaction_id = db.Column(db.String(100))



print("✅ All models loaded successfully!")
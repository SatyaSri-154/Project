# models1.py

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, time

db = SQLAlchemy()

class Users_info(db.Model):
    username = db.Column(db.String(80),primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contact=db.Column(db.String(200),unique=True,nullable=False)
    address=db.Column(db.String(200),unique=True,nullable=False)
    password = db.Column(db.String(200), nullable=False)


    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)



class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(120), nullable=False)
    services = db.Column(db.String(120), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    __table_args__ = (db.UniqueConstraint('date', 'time', name='_date_time_uc'),)

    def __repr__(self):
        return f'<Appointment {self.id} for user {self.user_id}>'



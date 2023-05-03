from . import db
from flask_login import UserMixin


class Blacklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    number = db.Column(db.Integer)


class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year_id = db.Column(db.Integer, db.ForeignKey('year.id'))
    signup = db.relationship('Signup', backref='events')
    name = db.Column(db.String(300))
    date  = db.Column(db.Date)
    temp_id = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    mail_temp = db.Column(db.String(1000))
    

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    signup_id = db.Column(db.Integer, db.ForeignKey('signup.id'))
    is_verified = db.Column(db.Boolean, default=False)
    is_contact = db.Column(db.Boolean, default=True)
    name = db.Column(db.String(300))
    email = db.Column(db.String(300))
    adress = db.Column(db.String(300))
    year = db.Column(db.Integer)
    telNum = db.Column(db.Integer)
    selectSize = db.Column(db.String(10))
    weight = db.Column(db.Integer)
    height = db.Column(db.Integer)
   

class Signup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    date  = db.Column(db.DateTime)
    person = db.relationship('Person', backref='signup')
    basic = db.relationship('Basic', backref='signup')
    winter = db.relationship('Winter', backref='signup')
    turnament = db.relationship('Turnament', backref='signup')
    older = db.relationship('Older', backref='signup')


class Basic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    signup_id = db.Column(db.Integer, db.ForeignKey('signup.id'))
    howMany = db.Column(db.Integer)
    whereKnew = db.Column(db.String(300))
    intro = db.Column(db.String(500))


class Winter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    signup_id = db.Column(db.Integer, db.ForeignKey('signup.id'))
    skiEver = db.Column(db.Boolean)
    skiSkill = db.Column(db.String(500))
    skiInst = db.Column(db.Boolean)
    passBuy = db.Column(db.String(500))
    isLent = db.Column(db.Boolean)
    skiLent = db.Column(db.String(500))


class Turnament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    signup_id = db.Column(db.Integer, db.ForeignKey('signup.id'))
    ageCat = db.Column(db.String(300))
    teamName = db.Column(db.String(300))
    teamFrom = db.Column(db.String(300))
    teamNum = db.Column(db.Integer)
    peopleNum = db.Column(db.Integer)
    say = db.Column(db.String(300))


class Older(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    signup_id = db.Column(db.Integer, db.ForeignKey('signup.id'))
    isBike = db.Column(db.Boolean)
    attrac = db.Column(db.String(300))
    pray = db.Column(db.String(300))
    freeTime = db.Column(db.String(300))


class Year(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    event_num = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    first_add = db.Column(db.Boolean, default=False, nullable=False)
    events = db.relationship('Events', backref='year')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

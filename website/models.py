from . import db
from flask_login import UserMixin


class Blacklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    number = db.Column(db.Integer)


#class Events(db.Model):
 #   id = db.Column(db.Integer, primary_key=True)
  #  name = db.Column(db.String(300))


class EventsNew(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    template = db.Column(db.Integer)


class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    temp_id = db.Column(db.Integer)
    template1 = db.relationship('Template1', backref='events')
    template2 = db.relationship('Template2', backref='events')
    template3 = db.relationship('Template3', backref='events')
    year_id = db.Column(db.Integer, db.ForeignKey('year.id'))


class Template1(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temp_name = db.Column(db.String(300))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    name = db.Column(db.String(300))
    email = db.Column(db.String(300))

class Template2(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temp_name = db.Column(db.String(300))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    name = db.Column(db.String(300))
    email = db.Column(db.String(300))
    adress = db.Column(db.String(300))

class Template3(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temp_name = db.Column(db.String(300))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    name = db.Column(db.String(300))
    number = db.Column(db.Integer)


class Year(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    event_num = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    events = db.relationship('Events', backref='year')


class SignUpData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    selectEvent = db.Column(db.String(300))
    name = db.Column(db.String(300))
    email = db.Column(db.String(300))
    adress = db.Column(db.String(300))
    year = db.Column(db.Integer)
    telNum = db.Column(db.Integer)
    howMany = db.Column(db.Integer)
    whereKnew = db.Column(db.String(300))
    intro = db.Column(db.String(500))
    selectSize = db.Column(db.String(10))

    #def __repr__(self):
     #   return f'Element numer: {self.id}, nazwisko: {self.name}, email: {self.email}'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

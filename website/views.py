from flask import Blueprint, render_template, flash, request, jsonify
from modules.check_module import email_is_valid, check_vals
from modules.servis_html import get_form_val, db_add_new_sigup
from .models import SignUpData, EventsNew, Events, Blacklist
from . import db
import json

views = Blueprint('views', __name__)

#--------> Templates paterns
temp1 = ['selectEvent', 'name', 'email', 
            'adress', 'year', 'telNum', 'howMany', 'whereKnew', 'intro', 'selectSize']



#--------> For client
@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        event = EventsNew.query.filter_by(name=request.form.get('selectEvent')).first()
        if event:
            if event.template == 1:
                dic = get_form_val(temp1)

                if check_vals(dic, event.template):
                    db_add_new_sigup(dic, event.template)
            else:
                flash(f'ziomek to nie ten event, wybrales {event.template}', category='error')
            return render_template('home.html', ev=event, test=SignUpData.query.all(), events=EventsNew.query.all())
        else:
            flash(f'ziomek tu nie ma eventow, wybrales', category='error')
            return render_template('home.html')
    else:
        return render_template('home.html', test=SignUpData.query.all(), events=EventsNew.query.all())



@views.route('/aftersignup')
def after_sign_up():
    return render_template('aftersignup.html')


#--------> For admin
@views.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        eventName = request.form.get('eventName')
        template = request.form.get('template')
        new_event = EventsNew(name=eventName, template=template)
        db.session.add(new_event)
        db.session.commit()
    return render_template('test.html', signup=SignUpData.query.all(), events=EventsNew.query.all())

#----------> delete items

@views.route('/delete-event', methods=['POST'])
def delete_event():
    event = json.loads(request.data)
    eventID = event['itemID']
    event = EventsNew.query.get(eventID)
    if event:
        db.session.delete(event)
        db.session.commit()
    return jsonify({})

@views.route('/delete-bl', methods=['POST'])
def delete_bl():
    item = json.loads(request.data)
    itemID = item['itemID']
    item = Blacklist.query.get(itemID)
    if item:
        db.session.delete(item)
        db.session.commit()
    return jsonify({})

@views.route('/delete-year', methods=['POST'])
def delete_year():
    item = json.loads(request.data)
    itemID = item['itemID']
    item = YearEvents.query.get(itemID)
    if item:
        db.session.delete(item)
        db.session.commit()
    return jsonify({})   

#----------> end delete items


@views.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@views.route('/dashboard/signup')
def admin_sign_up():
    return render_template('adminsignup.html')

@views.route('/dashboard/events', methods=['GET', 'POST'])
def admin_events():
    if request.method == 'POST':
        eventName = request.form.get('eventName')

        new_event = Events(name=eventName)
        db.session.add(new_event)
        db.session.commit()
    return render_template('adminevents.html',test=Events.query.all()) 

@views.route('/dashboard/blacklist', methods=['GET', 'POST'])
def admin_blacklist():
    if request.method == 'POST':
        email = request.form.get('email')
        number = request.form.get('number')
        items = Blacklist.query.all()
        if email and number:
            for item in items:
                if item.email == email:
                    flash(f'Podanej email już jest w bazie pod numerem {item.id}.', category='error')
                if item.number == number:
                    flash(f'Podanej numer telefonu już jest w bazie pod numerem {item.id}.', category='error') 
            new_item = Blacklist(email=email, number=number)
            db.session.add(new_item)
            db.session.commit()
            flash('Dodano do czarnej listy', category='success')
        else:
            flash('Najpierw wprowadź dane', category='error')
    return render_template('adminblacklist.html', blacklist=Blacklist.query.all())


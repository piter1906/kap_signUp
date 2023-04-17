from flask import Blueprint, render_template, flash, request, jsonify, redirect, url_for
from modules.check_module import *
from modules.servis_html import *
from .models import SignUpData, EventsNew, Events, Blacklist, Year, Template1, Template2, Template3
from . import db
import json

views = Blueprint('views', __name__)

#--------> Templates paterns
temp1 = ['selectEvent', 'name', 'email', 
            'adress', 'year', 'telNum', 'howMany', 'whereKnew', 'intro', 'selectSize']

nextt = True

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
        flash(f'Element {item.email} {item.number} usunięty z czarnej listy')
    return jsonify({})

@views.route('/delete-year', methods=['POST'])
def delete_year():
    item = json.loads(request.data)
    itemID = item['itemID']
    item = Year.query.get(itemID)
    if item:
        db.session.delete(item)
        db.session.commit()
        flash(f'Element {item.name} {item.is_active} usunięty lat')
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
    return render_template('adminevents.html')
      

@views.route('/dashboard/addyear', methods=['GET', 'POST'])
def add_year():
    if request.method == 'POST':
        name = request.form.get('name')
        event_num = request.form.get('event_number')
        years = Year.query.all()
        db_add_year(name, event_num, years)
        return redirect(url_for('views.add_events'))

    return render_template('addyear.html')

@views.route('/dashboard/edityear', methods=['GET', 'POST'])
def edit_year():
    years = Year.query.all()
    if years:
        for item in years:
            if item.is_active:
                year = item
            else:
                year = 0
        return render_template('edityear.html', years=Year.query.all(), year=year)
    return render_template('edityear.html') 

@views.route('/dashboard/addevents', methods=['GET', 'POST'])
def add_events():
    years = Year.query.all()
    if years:
        for item in years:
            if item.is_active:
                year = item
        if request.method == 'POST':
            db_add_event(year)
            return redirect(url_for('views.dashboard'))
        return render_template('addevents.html', year=year)
    flash('Nie masz bezpośredniego dostępu do tej strony', category='error')
    return redirect(url_for('views.dashboard'))   

@views.route('/dashboard/blacklist', methods=['GET', 'POST'])
def admin_blacklist():
    if request.method == 'POST':
        email = request.form.get('email')
        number = request.form.get('number')
        if check_bl(email, number):
            db_add_new_blacklist(email, number)

    return render_template('adminblacklist.html', blacklist=Blacklist.query.all())


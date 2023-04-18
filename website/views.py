from flask import Blueprint, render_template, flash, request, jsonify, redirect, url_for
from modules.check_module import *
from modules.servis_html import *
from .models import SignUpData, EventsNew, Events, Blacklist, Year, Template1, Template2, Template3
from . import db
import json

views = Blueprint('views', __name__)

#--------> Templates paterns
temp1_schem = ['name', 'email']

nextt = True

#--------> For client
@views.route('/', methods=['GET', 'POST'])
def home():
    years = Year.query.all()
    if years:
        for yr in years:
            if yr.is_active:
                year = yr
        if request.method == 'POST':
            event_name = request.form.get('selectEvent')
            for item in year.events:
                if item.name == event_name:
                    event = item
            if event.temp_id == 1:
                return redirect(url_for('views.temp1', event_id=event.id))
            elif event.temp_id == 2:
                return f'jestem w template{event.temp_id}'
            elif event.temp_id == 3:
                return f'jestem w template{event.temp_id}'
        return render_template('home.html', year=year)

    return render_template('home.html')
"""if request.method == 'POST':
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
        return render_template('home.html', test=SignUpData.query.all(), events=EventsNew.query.all())"""

@views.route('/temp1', methods=['GET','POST'])
def temp1():
    event_id = request.args.get('event_id', None)
    event = Events.query.get(event_id)
    if request.method == 'POST':
        dic = get_form_val(temp1_schem)
        if check_vals(dic, event.temp_id):
            db_add_new_sigup(dic, event)
        return redirect(url_for('views.home'))

    return render_template('temp1.html', event=event)
    
@views.route('/user', methods=['GET','POST'])
def user_page():
    event_id = request.args.get('event_id', None)
    numer_id = 'number' + event_id
    number = request.form.get(numer_id)
    return f'{event_id} {number}'

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

@views.route('/delete-bl/<int:itemID>', methods=['GET','POST'])
def delete_bl(itemID):
    item = Blacklist.query.get(itemID)
    if item:
        db.session.delete(item)
        db.session.commit()
        flash(f'Element {item.email} {item.number} usunięty z czarnej listy')
    return redirect(url_for('views.admin_blacklist'))

@views.route('/delete-year/<int:itemID>', methods=['GET','POST'])
def delete_year(itemID):
    item = Year.query.get(itemID)
    if item:
        db.session.delete(item)
        db.session.commit()
        flash(f'Element {item.name} {item.is_active} usunięty lat')
    return redirect(url_for('views.edit_year'))  

#----------> end delete items

#----------> get event

@views.route('/get-event', methods=['POST'])
def get_event():
    event = json.loads(request.data)
    eventID = event['itemID']
    event = EventsNew.query.get(eventID)
    if event:
        db.session.delete(event)
        db.session.commit()
    return jsonify({})

#----------> end get event

@views.route('/form', methods=['GET','POST'])
def form():
    years = Year.query.all()
    return render_template('form.html', years=years)


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


from flask import Blueprint, render_template, flash, request, jsonify, redirect, url_for, make_response, send_file
from flask_login import login_required, current_user
from modules.check_module import *
from modules.servis_html import *
from .models import Blacklist, User, Events, Year, Signup, Basic, Older, Winter, Person, Turnament 
from . import db
import json
from . import mail


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
        lst_events = year.events
        lst_events = sorted(lst_events, key=lambda event: event.date)
        date_stop = datetime.date.today()
        if request.method == 'POST':
            event_n = request.form.get('selectEvent')
            event_name = event_n[11:]
            for item in lst_events:
                if item.is_active:
                    if item.name == event_name:
                        event = item
            if event.temp_id == 1:
                return redirect(url_for('views.temp1', event_id=event.id))
            elif event.temp_id == 2:
                return f'jestem w template{event.temp_id}'
            elif event.temp_id == 3:
                return f'jestem w template{event.temp_id}'
        return render_template('home.html', year=year, user=current_user, lst_events=lst_events, date_stop=date_stop)

    return render_template('home.html', user=current_user)
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

#-----------------> templates

@views.route('/temp1', methods=['GET','POST'])
def temp1():
    event_id = request.args.get('event_id', None)
    event = Events.query.get(event_id)
    if request.method == 'POST':
        dic = get_form_val(temp1_schem)
        if check_vals(dic, event.temp_id):
            db_add_new_sigup(dic, event)
        else:
            return redirect(url_for('views.temp1', event_id=event.id))
        return redirect(url_for('views.home'))

    return render_template('temp1.html', event=event, user=current_user)

@views.route('/temp2', methods=['GET','POST'])
def temp2():
    event_id = request.args.get('event_id', None)
    event = Events.query.get(event_id)
    if request.method == 'POST':
        dic = get_form_val(temp1_schem)
        if check_vals(dic, event.temp_id):
            db_add_new_sigup(dic, event)
        else:
            return redirect(url_for('views.temp2', event_id=event.id))
        return redirect(url_for('views.home'))

    return render_template('temp2.html', event=event, user=current_user)


#-----------------------------------> end templates
  
@views.route('/user', methods=['GET','POST'])
def user_page():
    event_id = request.args.get('event_id', None)
    numer_id = 'number' + event_id
    number = request.form.get(numer_id)
    return render_template('body.html')

@views.route('/aftersignup')
def after_sign_up():
    return render_template('aftersignup.html', user=current_user)


#--------> For admin
@views.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        eventName = request.form.get('eventName')
        template = request.form.get('template')
        new_event = EventsNew(name=eventName, template=template)
        db.session.add(new_event)
        db.session.commit()
    return render_template('test.html', signup=SignUpData.query.all(), events=EventsNew.query.all(), user=current_user)

#----------> delete items

@views.route('/delete-event', methods=['POST'])
@login_required
def delete_event():
    event = json.loads(request.data)
    eventID = event['itemID']
    event = EventsNew.query.get(eventID)
    if event:
        db.session.delete(event)
        db.session.commit()
    return jsonify({})


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
    return render_template('form.html', years=years, user=current_user)


@views.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@views.route('/dashboard/signup')
@login_required
def admin_sign_up():
    return render_template('adminsignup.html', user=current_user)

@views.route('/dashboard/events', methods=['GET', 'POST'])
@login_required
def admin_events():
    return render_template('adminevents.html', user=current_user)
      

@views.route('/dashboard/addyear', methods=['GET', 'POST'])
@login_required
def add_year():
    if request.method == 'POST':
        name = request.form.get('name')
        event_num = request.form.get('event_number')
        years = Year.query.all()
        if check_year(name, event_num):
            db_add_year(name, event_num, years)
            return redirect(url_for('views.add_events'))
        else:
            return render_template('addyear.html', user=current_user)

    return render_template('addyear.html', user=current_user)

@views.route('/dashboard/edityear', methods=['GET', 'POST'])
@login_required
def edit_year():
    years = Year.query.all()
    if years:
        for item in years:
            if item.is_active:
                year = item
        if year.is_active:
            lst_events = year.events
            lst_events = sorted(lst_events, key=lambda event: event.date)
            return render_template('edityear.html', years=Year.query.all(), year=year, user=current_user, lst_events=lst_events)
        else:
            flash('Brak aktywnej listy akcji', category='error')
            return redirect(url_for('views.add_year'))
    else:
        flash('Najpierw dodaj rok', category='error')
        return redirect(url_for('views.add_year'))

@views.route('/dashboard/editevent', methods=['GET', 'POST'])
@login_required
def edit_event():
    event_id = request.args.get('event_id', None)
    backup = request.args.get('backup', None)
    event = Events.query.get(int(event_id))
    if event:
        if request.method == 'POST':
            check = db_update_event(event)
            if check:
                return redirect(url_for('views.edit_year'))
            else:
                return redirect(f'/dashboard/editevent?event_id={event_id}')
        return render_template('editevent.html', event=event, user=current_user)
    else:
        flash('Operacja nie jest dostepna', category='error')
        return redirect(url_for('views.dashboard'))



@views.route('/dashboard/addevents', methods=['GET', 'POST'])
@login_required
def add_events():
    years = Year.query.all()
    if years:
        for item in years:
            if item.is_active:
                year = item
        if not year.first_add:
            if request.method == 'POST':
                tup = db_add_event(year)
                if tup[1]:
                    return redirect(url_for('views.dashboard'))
                else:
                    return render_template('addevents.html', year=year, user=current_user, dic=tup[0])
            return render_template('addevents.html', year=year, user=current_user, dic={})
        else:
            flash('Operacja nie jest dostepna', category='error')
            return redirect(url_for('views.dashboard'))
    else:
        flash('Najpierw dodaj rok', category='error')
        return redirect(url_for('views.add_year'))  

@views.route('/dashboard/blacklist', methods=['GET', 'POST'])
@login_required
def admin_blacklist():
    if request.method == 'POST':
        email = request.form.get('email')
        number = request.form.get('number')
        if check_bl(email, number):
            db_add_new_blacklist(email, number)

    return render_template('adminblacklist.html', blacklist=Blacklist.query.all(), user=current_user)


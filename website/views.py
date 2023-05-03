from flask import Blueprint, render_template, flash, request, jsonify, redirect, url_for, make_response, send_file, session
from flask_login import login_required, current_user
from modules.check_module import *
from modules.servis_html import *
from .models import Blacklist, User, Events, Year, Signup, Basic, Older, Winter, Person, Turnament 
from . import db
import json
from . import mail


views = Blueprint('views', __name__)

#--------> Templates paterns
temp1_schem = ['name', 'email', 'telNum', 'adress', 'year', 'selectSize', 'howMany', 'whereKnew', 'intro']
temp2_schem = ['name', 'email', 'telNum', 'adress', 'year', 'howMany', 'whereKnew', 'intro', 'skiEver', 'skiSkill', 'skiInst', 'passBuy', 'isLent', 'skiLent', 'weight', 'height']
temp3_schem_1 = ['name', 'email', 'telNum', 'ageCat', 'teamName', 'teamFrom', 'teamNum', 'peopleNum', 'say']
temp3_schem_2 = ['name', 'email', 'telNum', 'adress', 'year']
temp4_schem = ['name', 'email', 'telNum', 'adress', 'year', 'selectSize', 'howMany', 'whereKnew', 'intro', 'isBike', 'attrac', 'pray', 'freeTime']
temp5_schem = ['name', 'email', 'telNum', 'adress', 'year', 'howMany', 'whereKnew', 'intro']

nextt = True


#--------> For client
@views.route('/', methods=['GET', 'POST'])
def home():
    #check_date()
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
            session['event_id'] = event.id
            return redirect(url_for('views.signup'))

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

@views.route('/signup', methods=['GET','POST'])
def signup():
    if 'event_id' in session.keys():
        event_id = session['event_id']
        event = Events.query.get(event_id)
        if request.method == 'POST':
            if event.temp_id == 3:
                dic = get_form_val(temp3_schem_1)
                num = ""
                if check_vals(num, event, **dic):
                    if check_member(dic['telNum'], dic['email']):
                        session['first_step'] = True
                        tup = db_add_new_sigup(dic, event)
                        session['person_id'] = tup[0]
                        session['signup_id'] = tup[1]
                        session['teamNum'] = tup[2]
                        basket.event = event
                        return redirect(url_for('views.signup_next'))
                    else:
                        return redirect(url_for('views.home'))
                else:
                    return render_template('signup.html', event=event, user=current_user, dic=dic)

            elif event.temp_id == 6:
                pass
            else:
                if event.temp_id == 1:
                    dic = get_form_val(temp1_schem)
                    num = ""
                if event.temp_id == 2:
                    dic = get_form_val(temp2_schem)
                    num = ""
                if event.temp_id == 4:
                    dic = get_form_val(temp4_schem)
                    num = ""
                if event.temp_id == 5:
                    dic = get_form_val(temp5_schem)
                    num = ""
                if check_vals(num, event, **dic):
                    if check_member(dic['telNum'], dic['email']):
                        person = db_add_new_sigup(dic, event)
                        session['person_id'] = person.id
                        return redirect(url_for('views.after_sign_up'))
                    else:
                        return redirect(url_for('views.home'))
                else:
                    return render_template('signup.html', event=event, user=current_user, dic=dic)
            return render_template('signup.html', event=event, user=current_user, dic={})
        return render_template('signup.html', event=event, user=current_user, dic={})
    else:
        flash('Operacja nie jest dostępna.', category='error')
        return redirect(url_for('views.home'))


@views.route('/signup_next', methods=['GET','POST'])
def signup_next():
    if 'event_id' in session.keys():
        event_id = session['event_id']
        event = Events.query.get(event_id)
        if request.method == 'POST':
            if event.temp_id == 3:
                for i in range(int(session['teamNum'])):
                    lst_val = [f'name{i+1}', f'email{i+1}', f'telNum{i+1}', f'adress{i+1}', f'year{i+1}']
                    dic = get_form_val(lst_val)
                    if check_vals(i+1, event, **dic):
                        session['currentNum'] = i + 1
                        db_add_new_sigup(dic, event)
                    else:
                        return render_template('signup_next.html', event=event, user=current_user, dic=dic, number=session['teamNum'])
                session.pop('teamNum')
                session.pop('first_step')
                flash('Udało się drużynę!', category='success')
                return redirect(url_for('views.after_sign_up'))
            return render_template('signup_next.html', event=event, user=current_user, dic={}, number=session['teamNum'])
        return render_template('signup_next.html', event=event, user=current_user, dic={}, number=session['teamNum'])
    else:
        flash('Operacja nie jest dostępna.', category='error')
        return redirect(url_for('views.home'))

@views.route('/aftersignup')
def after_sign_up():
    if 'person_id' in session.keys() and 'event_id' in session.keys():
        event_id = session['event_id']
        event = Events.query.get(event_id)
        person_id = session['person_id']
        person = Person.query.get(person_id)
        session.pop('event_id')
        session.pop('person_id')
        #send_mail(event, person)

        return render_template('aftersignup.html', person=person, event=event, user=current_user)
    else:
        flash('Brak dostępu do tej strony', category='error')
        return redirect(url_for('views.home'))
    


#-----------------------------------> end templates
  
@views.route('/user', methods=['GET','POST'])
def user_page():
    event_id = request.args.get('event_id', None)
    numer_id = 'number' + event_id
    number = request.form.get(numer_id)
    return render_template('body.html')

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
            if request.method == 'POST':
                tup = db_new_event(year)
                if tup[0]:
                    return redirect(url_for('views.edit_year'))
                else:
                    return render_template('edityear.html', years=Year.query.all(), year=year, user=current_user, lst_events=lst_events, backup=tup[1])
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


@views.route('/dashboard/eventview', methods=['GET', 'POST'])
@login_required
def event_view():
    event_id = request.args.get('event_id', None)
    event = Events.query.get(int(event_id))
    if event:
        sn_lst = event.signup
        sn_lst = sorted(sn_lst, key=lambda signup: signup.id, reverse=True)
        return render_template('event_view.html', event=event, sn_lst=sn_lst, user=current_user)
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


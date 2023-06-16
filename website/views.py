from flask import Blueprint, render_template, flash, request, jsonify, redirect, url_for, make_response, send_file, session, abort
from flask_login import login_required, current_user
from modules.check_module import *
from modules.servis_html import *
from .models import Blacklist, User, Events, Year, Signup, Basic, Older, Winter, Person, Turnament 
from . import db
import json
from . import mail
import logging

views = Blueprint('views', __name__)
logger = logging.getLogger('views_logger')


#--------> Templates paterns
temp1_schem = ['name', 'email', 'telNum', 'adress', 'year', 'selectSize', 'howMany', 'whereKnew', 'intro']
temp2_schem = ['name', 'email', 'telNum', 'adress', 'year', 'howMany', 'whereKnew', 'intro', 'skiEver', 'skiSkill', 'skiInst', 'passBuy', 'isLent', 'skiLent', 'weight', 'height']
temp3_schem = ['name', 'email', 'telNum', 'ageCat', 'teamName', 'teamFrom', 'teamNum', 'peopleNum', 'say']
temp4_schem = ['name', 'email', 'telNum', 'adress', 'year', 'selectSize', 'howMany', 'whereKnew', 'intro', 'isBike', 'attrac', 'pray', 'freeTime']
temp5_schem = ['name', 'email', 'telNum', 'adress', 'year', 'howMany', 'whereKnew', 'intro']
temp6_schem = ['name', 'email', 'telNum', 'adress', 'year', 'selectSize', 'howMany', 'whereKnew', 'intro', 'sonNum']


#--------> For client
@views.route('/', methods=['GET', 'POST'])
def home():
    years = Year.query.all()
    if years:
        for yr in years:
            if yr.is_active:
                year = yr
        lst_events = []
        for event in year.events:
            if event.is_active:
                lst_events.append(event)
        if lst_events:
            lst_events = sorted(lst_events, key=lambda event: event.date.toordinal() if event.date else float('inf'))
            if request.method == 'POST':
                if 'person_id' in session.keys() and 'event_id' in session.keys():
                    session.pop('person_id')
                    session.pop('event_id')
                event_n = request.form.get('selectEvent')
                if event_n:
                    event_name = get_event_name(event_n)
                    for item in lst_events:
                        if item.is_active:
                            if item.name == event_name:
                                event = item
                    session['event_id'] = event.id
                    return redirect(url_for('views.signup'))
                else:
                    flash('Najpierw wybierz akcję.', category='error')
                    return render_template('home.html', user=current_user, lst_events=lst_events)
        return render_template('home.html', user=current_user, lst_events=lst_events)
    return render_template('home.html', user=current_user)

#-----------------> For client ---------> sign up 

@views.route('/signup', methods=['GET','POST'])
def signup():
    if 'event_id' in session.keys():
        event_id = session['event_id']
        event = Events.query.get(event_id)
        user_ip = request.remote_addr
        if request.method == 'POST':
            logger.info(f'Proba zapisu na: {event} | IP: {user_ip}')
            if event.temp_id == 1:
                dic = get_form_val(temp1_schem)
            if event.temp_id == 2:
                dic = get_form_val(temp2_schem)
            if event.temp_id == 3:
                dic = get_form_val(temp3_schem)
            if event.temp_id == 4:
                dic = get_form_val(temp4_schem)
            if event.temp_id == 5:
                dic = get_form_val(temp5_schem)
            if event.temp_id == 6:
                dic = get_form_val(temp6_schem)
            if check_vals(event, **dic):
                if check_member(dic['telNum'], dic['email']):
                    if event.temp_id != 3 and event.temp_id != 6:
                        person = db_add_new_sigup(dic, event, [])
                        session['person_id'] = person.id
                        return redirect(url_for('views.after_sign_up'))
                    if event.temp_id == 3:
                        session['dict'] = dic
                        return redirect(url_for('views.signup_next'))
                    if event.temp_id == 6:
                        if int(dic['sonNum']) == 0:
                            person = db_add_new_sigup(dic, event, [])
                            session['person_id'] = person.id
                            return redirect(url_for('views.after_sign_up'))
                        else:
                            session['dict'] = dic
                            return redirect(url_for('views.signup_next'))
                else:
                    return redirect(url_for('views.home'))
            else:
                return render_template('signup.html', event=event, user=current_user, dic=dic)
        return render_template('signup.html', event=event, user=current_user, dic={})
    else:
        abort(403)

@views.route('/signup_next', methods=['GET','POST'])
def signup_next():
    if 'event_id' in session.keys():
        event_id = session['event_id']
        event = Events.query.get(event_id)
        number = int(session['dict']['teamNum']) if event.temp_id == 3 else int(session['dict']['sonNum'])
        if request.method == 'POST':        
            lst_mem = []
            dic = {}
            for i in range(number):
                lst_val = [f'name{i+1}', f'email{i+1}', f'telNum{i+1}', f'adress{i+1}', f'year{i+1}'] if event.temp_id == 3 \
                            else [f'name{i+1}', f'email{i+1}', f'telNum{i+1}', f'adress{i+1}', f'year{i+1}', f'selectSize{i+1}']
                dic.update(get_form_val(lst_val))
            for i in range(number):    
                if check_vals(event, num=i+1, **dic):
                    num = i + 1
                    member = get_member(dic, event, num)
                    lst_mem.append(member)
                else:
                    lst_mem.clear()
                    return render_template('signup_next.html', event=event, user=current_user, dic=dic, number=number)
            person = db_add_new_sigup(session['dict'], event, lst_mem)
            session['person_id'] = person.id
            session.pop('dict')
            return redirect(url_for('views.after_sign_up'))
        return render_template('signup_next.html', event=event, user=current_user, dic={}, number=number)
    else:
        abort(403)

@views.route('/aftersignup')
def after_sign_up():
    if 'person_id' in session.keys() and 'event_id' in session.keys():
        event_id = session['event_id']
        event = Events.query.get(event_id)
        person_id = session['person_id']
        person = Person.query.get(person_id)
        user_ip = request.remote_addr
        if person and event:
            session.pop('event_id')
            session.pop('person_id')
            mail_self = send_mail_admin(event, person)
            logger.info(f'Nowy zapis - {event} | przez - {person} | IP: {user_ip} | Mail do nas = {mail_self}')
            session['sn_finish'] = True      
            return redirect(url_for('views.sign_up_finish'))
    else:
        abort(403)

@views.route('/signup_finish')
def sign_up_finish():
    return render_template('aftersignup.html', user=current_user)

    
#-----------------------------------> end sign up

#-----------------> end For client

@views.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@views.route('/dashboard/mail')
@login_required
def admin_mail():
    event_id = request.args.get('event_id', None)
    if event_id.isnumeric():
        event = Events.query.get(int(event_id))
        if event:
            mail_lst = generate_mails(event)
            mail_str = "; ".join(mail_lst)
            return render_template('adminmail.html', user=current_user, event=event, mail_str=mail_str)
        else:
            raise TypeError
    else:
        abort(400)

@views.route('/dashboard/events', methods=['GET', 'POST'])
@login_required
def admin_events():
    return render_template('adminevents.html', user=current_user)

@views.route('/dashboard/oldevents', methods=['GET', 'POST'])
@login_required
def old_events():
    years = Year.query.all()
    if years:
        lst_years = []
        for year in years:
            if not year.is_active:
                lst_years.append(year)
        lst_years = sorted(lst_years, key=lambda year: year.id, reverse=True)
        if request.method == 'POST':
            year_name = request.form.get('selectYear')
            if year_name:
                for item in lst_years:
                    if item.name == year_name:
                        year = item
                lst_events = year.events
                lst_events = sorted(lst_events, key=lambda event: event.date.toordinal() if event.date else float('inf'))
                return render_template('oldevents.html', lst_years=lst_years, year=year, user=current_user, lst_events=lst_events)
            else:
                flash('Najpierw wybierz rok.', category='error')
                return render_template('oldevents.html', lst_years=lst_years, year='', user=current_user, lst_events='')
        return render_template('oldevents.html', lst_years=lst_years, year='', user=current_user, lst_events='')
    else:
        flash('Najpierw dodaj rok', category='error')
        return redirect(url_for('views.add_year'))
        

@views.route('/dashboard/addyear', methods=['GET', 'POST'])
@login_required
def add_year():
    if request.method == 'POST':
        name = request.form.get('name')
        event_num = request.form.get('event_number')
        if check_year(name, event_num):
            year_session = {'year_name': name, 'event_num': event_num}
            session.update(year_session)
            return redirect(url_for('views.add_events'))
        else:
            return render_template('addyear.html', user=current_user)
    return render_template('addyear.html', user=current_user)

@views.route('/dashboard/addevents', methods=['GET', 'POST'])
@login_required
def add_events():
    if 'year_name' in session.keys() and 'event_num' in session.keys():
        year = Year(name=session['year_name'], event_num=int(session['event_num']))
        if request.method == 'POST':
            years = Year.query.all()
            tup = db_add_event(year, years)
            if tup[1]:
                session.pop('year_name')
                session.pop('event_num')
                return redirect(url_for('views.dashboard'))
            else:
                return render_template('addevents.html', year=year, user=current_user, dic=tup[0])
        return render_template('addevents.html', year=year, user=current_user, dic={})
    else:
        flash('Najpierw dodaj rok', category='error')
        return redirect(url_for('views.add_year'))

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
            lst_events = sorted(lst_events, key=lambda event: event.date.toordinal() if event.date else float('inf'))
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
    if event_id.isnumeric():
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
            raise TypeError
    else:
        abort(400)


@views.route('/dashboard/eventview', methods=['GET', 'POST'])
@login_required
def event_view():
    event_id = request.args.get('event_id', None)
    if event_id.isnumeric():
        event = Events.query.get(int(event_id))
        if event:
            sn_lst = event.signup
            sn_lst = sorted(sn_lst, key=lambda signup: signup.id, reverse=True)
            dic = get_sumup(event, sn_lst)
            if event.temp_id != 3:
                return render_template('event_view.html', event=event, sn_lst=sn_lst, user=current_user, dic=dic)
            else:
                lst_young = []
                lst_old = []
                for signup in event.signup:
                    for turn in signup.turnament:
                        if turn.ageCat == 'Młodsi: 2010-2014 (drużyna składa się z 6 osób + bramkarz)':
                            lst_young.append(signup)
                        else:
                            lst_old.append(signup)
                lst_young = sorted(lst_young, key=lambda signup: signup.id, reverse=True)
                lst_old = sorted(lst_old, key=lambda signup: signup.id, reverse=True)
                return render_template('event_view.html', event=event, lst_young=lst_young, lst_old=lst_old, user=current_user, dic=dic)
        else:
            raise TypeError
    else:
        abort(400)  

@views.route('/dashboard/blacklist', methods=['GET', 'POST'])
@login_required
def admin_blacklist():
    if request.method == 'POST':
        email = request.form.get('email')
        number = request.form.get('number')
        if check_bl(email, number):
            db_add_new_blacklist(email, number)

    return render_template('adminblacklist.html', blacklist=Blacklist.query.all(), user=current_user)

@views.route('/dashboard/logs')
@login_required
def admin_logs():
    with open('website/app.log', 'r') as file:
        logs = file.read()
    return render_template('logs.html', logs=logs, user=current_user)

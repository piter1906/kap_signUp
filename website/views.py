from flask import Blueprint, render_template, flash, request
from modules.check_module import email_is_valid, check_vals
from modules.servis_html import get_form_val, db_add_new_sigup
from .models import SignUpData, EventsNew
from . import db

views = Blueprint('views', __name__)

#--------> Templates paterns
temp1 = ['selectEvent', 'name', 'email', 
            'adress', 'year', 'telNum', 'howMany', 'whereKnew', 'intro', 'selectSize']



#--------> For client
@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        event = request.form.get('selectEvent')
        evns = EventsNew.query.all()
        id_template = 0
        for item in evns:
            if item.name == event:
                id_template = item.template
                break

        if id_template == 1:
            dic = get_form_val(temp1)

            if check_vals(dic, id_template):
                db_add_new_sigup(dic, id_template)
        else:
            flash('ziomek to nie ten event', category='error')

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

@views.route('/dashboard/blacklist')
def admin_blacklist():
    return render_template('adminblacklist.html') 


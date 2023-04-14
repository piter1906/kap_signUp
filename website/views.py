from flask import Blueprint, render_template, flash, request
from modules.check_module import email_is_valid
from .models import SignUpData, Events
from . import db

views = Blueprint('views', __name__)

#--------> For client
@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        selectEvent = request.form.get('selectEvent')
        name = request.form.get('name')
        email = request.form.get('email')
        adress = request.form.get('adress')
        year = request.form.get('year')
        telNum = request.form.get('telNum')
        howMany = request.form.get('howMany')
        whereKnew = request.form.get('whereKnew')
        intro = request.form.get('intro')
        selectSize = request.form.get('selectSize')

        if not email_is_valid(email):
            flash('Podaj poprawny adres email.', category='error')
        elif len(name) < 5:
            flash('Imię i nazwisko: wprowadzone dane są za krótkie.', category='error')
        elif len(adress) < 10:
            flash('Adres: wprowadzone dane są za krótkie.', category='error')
        elif not year.isdigit() or len(year) > 4 or not int(year) > 1970 and int(year) < 2016:
            flash('Podaj poprawny rok urodzenia.', category='error')
        elif not telNum.isdigit() or len(telNum) != 9:
            flash('Podaj 9cio cyfrowy numer telefonu.', category='error')
        else:
            new_singup = SignUpData(selectEvent=selectEvent, 
                name=name, email=email, adress=adress, year=year, 
                telNum=telNum, howMany=howMany, whereKnew=whereKnew,
                intro=intro, selectSize=selectSize)
            db.session.add(new_singup)
            db.session.commit()
            flash('Udało się zapisać!', category='success')




    return render_template('home.html', test=SignUpData.query.all(), events=Events.query.all())

@views.route('/aftersignup')
def after_sign_up():
    return render_template('aftersignup.html')


#--------> For admin
@views.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        eventName = request.form.get('eventName')
        new_event = Events(name=eventName)
        db.session.add(new_event)
        db.session.commit()
    return render_template('test.html', signup=SignUpData.query.all(), events=Events.query.all())

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


from flask import Blueprint, render_template, flash, request
from .modules import email_is_valid

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
            flash('Udało się zapisać!', category='success')




    return render_template('home.html')

@views.route('/aftersignup')
def after_sign_up():
    return render_template('aftersignup.html')


#--------> For admin
@views.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@views.route('/dashboard/signup')
def admin_sign_up():
    return render_template('adminsignup.html')

@views.route('/dashboard/events')
def admin_events():
    return render_template('adminevents.html') 

@views.route('/dashboard/blacklist')
def admin_blacklist():
    return render_template('adminblacklist.html') 


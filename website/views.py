from flask import Blueprint, render_template

views = Blueprint('views', __name__)

#--------> For client
@views.route('/')
def home():
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


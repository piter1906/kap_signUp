from flask import Blueprint, render_template, flash, request, jsonify, redirect, url_for, make_response, send_file
from flask_login import login_required, current_user
from modules.check_module import *
from modules.servis_html import *
from .models import Blacklist, User, Events, Year, Signup, Basic, Older, Winter, Person, Turnament 
from . import db
import json
from . import mail
import os
from flask_mail import Mail, Message
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, From, To, Subject, PlainTextContent, HtmlContent, SendGridException
from xhtml2pdf import pisa
from xhtml2pdf.default import DEFAULT_FONT
import io
import sys
import datetime 

action = Blueprint('action', __name__)

@action.route('/datetest', methods=['GET', 'POST'])
def date():
    date_stop = datetime.date.today() - datetime.timedelta(days=1)
    return render_template('body.html', date=date)

#---------------> delete
options = {
    'page-size': 'Letter',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': "UTF-8"
}

@action.route('/test-signup/<int:itemID>')
@login_required
def test_sn(itemID):
    event = Events.query.get(itemID)
    test_signup(event, 10)
    return redirect(url_for('views.home'))


@action.route('/delete-bl/<int:itemID>', methods=['GET','POST'])
@login_required
def delete_bl(itemID):
    item = Blacklist.query.get(itemID)
    if item:
        db.session.delete(item)
        db.session.commit()
        flash(f'Element {item.email} {item.number} usunięty z czarnej listy')
    return redirect(url_for('views.admin_blacklist'))

@action.route('/delete-year/<int:itemID>', methods=['GET','POST'])
@login_required
def delete_year(itemID):
    item = Year.query.get(itemID)
    if item:
        db.session.delete(item)
        db.session.commit()
        flash(f'Element {item.name} {item.is_active} usunięty lat')
    return redirect(url_for('views.edit_year'))

@action.route('/delete-event/<int:itemID>', methods=['GET','POST'])
@login_required
def delete_event(itemID):
    item = Events.query.get(itemID)
    if item:
        db.session.delete(item)
        db.session.commit()
        flash(f'Wydarzenie {item.name} usunięte listy')
    return redirect(url_for('views.edit_year'))

@action.route('/delete-signup', methods=['GET','POST'])
@login_required
def delete_signup():
    event_id = session['event_id']
    signup_id = session['signup_id']
    event = Events.query.get(event_id)
    signup = Signup.query.get(signup_id)
    if signup:
        db.session.delete(signup)
        db.session.commit()
        session.pop('event_id')
        session.pop('signup_id')
        flash(f'Zapis został usunięty.')
    return redirect(f'/dashboard/eventview?event_id={event.id}')

@action.route('/delete', methods=['GET','POST'])
@login_required
def delete_conf():
    event_id = request.args.get('event_id', None)
    signup_id = request.args.get('signup_id', None)
    if event_id and signup_id:
        event = Events.query.get(int(event_id))
        signup = Signup.query.get(int(signup_id))
        session['event_id'] = event.id
        session['signup_id'] = signup.id
        return render_template('delete_confirm.html', event=event, signup=signup, user=current_user)
    elif event_id:
        event = Events.query.get(int(event_id))
        session['event_id'] = event_id
        return render_template('delete_confirm.html', event=event, signup='', user=current_user)
    else:
        flash('Nie masz dostępu do tej strony.', category='error')
        return redirect(url_for('views.dashboard'))

      

#-----------------------------> end delete

#-----------------------------> event actions

@action.route('/event-status/<int:itemID>', methods=['GET','POST'])
@login_required
def event_status(itemID):
    item = Events.query.get(itemID)
    if item:
        if item.date >= datetime.date.today():
            item.is_active = True if not item.is_active else False
            db.session.commit()
            flash(f'Status {item.name} zmieniony.')
        else:
            flash(f'Status {item.name} nie został zmieniony, ponieważ data akcji jest już przestarzała', category='error')
    return redirect(url_for('views.edit_year'))

@action.route('/signup-verified', methods=['GET','POST'])
@login_required
def signup_verified():
    event_id = request.args.get('event_id', None)
    event = Events.query.get(int(event_id))
    person_id = request.args.get('person_id', None)
    person = Person.query.get(int(person_id))
    if person:
        if not person.is_verified:
            person.is_verified = True
            db.session.commit()
            flash('Zapis został zweryfikowany.', category='success')
            return redirect(f'/dashboard/eventview?event_id={event.id}')
        else:
            flash('Operacja nie jest dostępna', category='error')
    return redirect(url_for('views.edit_year'))

#-----------------------------> end event actions

@action.route('/pdf')
@login_required
def pdf():
    event_id = request.args.get('event_id', None)
    event = Events.query.get(event_id)
    if event:
        sn_lst = event.signup
        if sn_lst:
            sn_lst = sorted(sn_lst, key=lambda signup: signup.id, reverse=True)
            sn_lst = change_polish_char(event, sn_lst)
            dic = get_sumup(event, sn_lst)
            if event.temp_id != 3:
                body = render_template('html2pdf.html', event=event, sn_lst=sn_lst, user=current_user, dic=dic)
            else:
                lst_young = []
                lst_old = []
                for signup in event.signup:
                    for turn in signup.turnament:
                        if turn.ageCat == 'Do 14 roku życia (drużyna składa się z 6 osób + bramkarz)':
                         lst_young.append(signup)
                        else:
                            lst_old.append(signup)
                lst_young = sorted(lst_young, key=lambda signup: signup.id, reverse=True)
                lst_old = sorted(lst_old, key=lambda signup: signup.id, reverse=True)
                body = render_template('html2pdf.html', event=event, lst_young=lst_young, lst_old=lst_old, user=current_user, dic=dic)

            pdf_file = io.BytesIO()
            pisa.CreatePDF(body, pdf_file, encoding='utf-8')
            pdf_file.seek(0)
            response = make_response(pdf_file.getvalue())
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = f'attachment; filename=Uczestnicy_{event.name}.pdf'

            return response
        else:
            flash('Brak zapisów na daną akcję. PDF nie został wygenerowany', category='error')
            return redirect(url_for('views.edit_year'))
    else:
        flash('Nie masz bezpośredniego dostępu do tej strony', category='error')
        return redirect(url_for('views.dashboard'))


@action.route('/testo')
def testto():
	return "elo ziomek"

@action.route('/gmail', methods=['GET','POST'])
def send_mail_gmail():
    if 'person_id' in session.keys() and 'event_id' in session.keys():
        event_id = session['event_id']
        event = Events.query.get(event_id)
        person_id = session['person_id']
        person = Person.query.get(person_id)
        """msg = Message(f'Witaj {person.name}', sender = 'kapszlaksend@gmail.com', recipients = [person.email])
                                msg.body = f"Siemano ziomek. Udało Ci się zapisać na akcję {event.name}. \n Oto treść maila: {event.mail_temp}"
                                mail.send(msg)
                                msg1 = Message(f'Nowy zapis dla {event.name}', sender = 'kapszlaksend@gmail.com', recipients = ['brpiotrwojtowicz@gmail.com'])
                                msg1.body = f"Wlasnie zapisał sie {person.name} na akcję {event.name}"
                                mail.send(msg1)"""
        session.pop('event_id')
        session.pop('person_id')
        return render_template('aftersignup.html', person=person, event=event, user=current_user)
    else:
        flash('Operacja nie jest dostępna', category='error')
        return redirect(url_for('views.home'))

@action.route('/sendgrid/<text>', methods=['GET','POST'])
def send_mail(text):
    to_emails = [To('agbedwojt@gmail.com', 'Mama'), 
    To('brpiotrwojtowicz@gmail.com', 'Pietrek')]
    message = Mail(from_email=From('kapszlaksend@gmail.com', 'Kapszlak'),
               to_emails=to_emails,
               subject=Subject(f'To jest testowy mail do {text}'),
               plain_text_content=PlainTextContent(f'No siema {text}'))
               #html_content=HtmlContent('<strong>and easy to do anywhere, even with Python</strong>'))
    """
    multiple emails
	to_emails = [
    To('ethomas@twilio.com', 'Elmer SendGrid'),
    To('elmer.thomas@gmail.com', 'Elmer Thomas')
]
    """

    sendgrid_client = SendGridAPIClient(api_key='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')
    response = sendgrid_client.send(message=message)
    return "Sent"
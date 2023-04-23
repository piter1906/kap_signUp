from flask import Blueprint, render_template, flash, request, jsonify, redirect, url_for, make_response, send_file
from flask_login import login_required, current_user
from modules.check_module import *
from modules.servis_html import *
from .models import SignUpData, EventsNew, Events, Blacklist, Year, Template1, Template2, Template3
from . import db
import json
from . import mail
import pdfkit
import os
from flask_mail import Mail, Message
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, From, To, Subject, PlainTextContent, HtmlContent, SendGridException


action = Blueprint('action', __name__)

#---------------> delete
options = {
    'page-size': 'Letter',
    'margin-top': '0.75in',
    'margin-right': '0.75in',
    'margin-bottom': '0.75in',
    'margin-left': '0.75in',
    'encoding': "UTF-8"
}


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

#-----------------------------> end delete

@action.route('/pdf')
def pdf():
    years = Year.query.all()
    for yr in years:
        if yr.is_active:
            year = yr
            for item in year.events:
                if item.name == 'Góry':
                    event = item


    body = render_template('pdf.html', event=event, year=year)

    path_wkhtmltopdf = 'website/static/bin/wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    pdfkit.from_string(body, 'website/reports/event.pdf', configuration=config, options=options)

    f_name = 'event.pdf'
    f_path = os.path.join('reports', f_name)
    return send_file(f_path, as_attachment=True)

@action.route('/testo')
def testto():
	return "elo ziomek"

@action.route('/gmail/<text>', methods=['GET','POST'])
def send_mail_gmail(text):
    msg = Message(f'Hello {text}', sender = 'kapszlaksend@gmail.com', recipients = ['brpiotrwojtowicz@gmail.com'])
    msg.body = f"Hello Flask message sent from {text} Flask-Mail"
    mail.send(msg)
    msg1 = Message(f'Admin {text}', sender = 'kapszlaksend@gmail.com', recipients = ['kapszlaksend@gmail.com', 'brpiotrwojtowicz@gmail.com'])
    msg1.body = f"Wlasnie zapisał sie {text} Flask-Mail"
    mail.send(msg1)
    return "Sent"

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
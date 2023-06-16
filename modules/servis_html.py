from flask import flash, request, redirect, url_for, session, render_template
from flask_login import login_required, current_user
from flask_mail import Mail, Message
from website import mail
from website import db
from modules.check_module import *
from website.models import Year, Blacklist, Events, Signup, Person, Turnament, Winter, Older, Basic
import datetime 
from dotenv import load_dotenv
import os
import re
import docx2txt
import logging

logger = logging.getLogger('serwis_logger')


def polish(temp):
	chars = 'ąćęłńśźżĄĆĘŁŃŚŹŻ'
	replace ='acelnszzACELNSZZ'
	translator = str.maketrans(chars, replace)
	return temp.translate(translator)

def generate_mails(event):
	mail_lst = []
	for signup in event.signup:
		for person in signup.person:
			if person.is_contact:
				mail_lst.append(person.email)
	return mail_lst

def date_from_str(date, create_ev):
	if date:
	    if create_ev:
	        year = int(date[:4])
	        month = int(date[5:7]) if date[5] == '1' else int(date[6])
	        day = int(date[8:]) if int(date[8]) != 0 else int(date[9])
	        return datetime.date(year=year, month=month, day=day)
	    else:
	        year = int(date[:4])
	        month = int(date[5:7])
	        day = int(date[8:10])
	        hour = int(date[11:13])
	        minute = int(date[14:16])
	        second = int(date[17:19])
	        return datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
	else:
		return None

def get_form_val(lst):
	dic = {}
	if lst:
		for val in lst:
			if val == 'skiLent':
				dic[val] = request.form.getlist(val)
			else:
				dic[val] = request.form.get(val)
	return dic

def get_event_name(name):
	pattern = r'^\d{4}-\d{2}-\d{2}\s+'
	match = re.match(pattern, name)
	if match:
		date = match.group()
		return name[len(date):]
	else:
		return name

def send_mail_user(event, person):
    load_dotenv()
    with open('website/static/files/kapszlak_karta_uczestnika.docx', 'rb') as file:
        msg = Message(f'Witaj {person.name}', sender=os.getenv('MAIL_USER'), recipients=[person.email])
        msg.body = f"Pokój i dobro!. \n Potwierdziliśmy Twoje zgłoszenie na akcję: {event.name}. \n {event.mail_temp}"
        msg.attach(
            filename='kapszlak_karta_uczestnika.docx',
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            data=file.read()
        )
        try:
            mail.send(msg)
            mail_user = 'TAK'
        except Exception as e:
            mail_user = f'NIE - error: {e}'
    return mail_user

def send_mail_admin(event, person):
    load_dotenv()
    msg1 = Message(f'{event.name} - nowy zapis.', sender=os.getenv('MAIL_USER'), recipients=['brpiotrwojtowicz@gmail.com'])
    msg1.body = f"""Własnie zapisał się: {person}; na akcję: {event.name}.\nPrzejdź na stronę zapisów aby potwierdzić: {url_for('views.dashboard', _external=True)}"""
    try:
        mail.send(msg1)
        mail_self = 'TAK'
    except Exception as e:
        mail_self = f'NIE - error: {e}'
    return mail_self



def db_add_new_sigup(dic, event, lst):
	date = str(datetime.datetime.now())
	date = date_from_str(date, False)
	signup = Signup(event_id=event.id, date=date)
	db.session.add(signup)
	db.session.commit()
	if event.temp_id == 3:
		person = Person(signup_id=signup.id, name=dic['name'], email=dic['email'], telNum=dic['telNum'])
		db.session.add(person)
		db.session.commit()
		peopleNum = dic['peopleNum'] if dic['peopleNum'] else 0
		turnament = Turnament(signup_id=signup.id, ageCat=dic['ageCat'], teamName=dic['teamName'],
						teamFrom=dic['teamFrom'], teamNum=dic['teamNum'], peopleNum=peopleNum, say=dic['say'])
		db.session.add(turnament)
		db.session.commit()
		for player in lst:
			player.signup_id = signup.id
			db.session.add(player)
			db.session.commit()
		flash(f'Udało się zapisać drużynę!', category='success')
	else:
		basic = Basic(signup_id=signup.id, howMany=dic['howMany'], whereKnew=dic['whereKnew'], intro=dic['intro'])
		db.session.add(basic)
		db.session.commit()
		selectSize = '' if event.temp_id == 5 or event.temp_id == 2 else dic['selectSize']
		weight = dic['weight'] if event.temp_id == 2 else ''
		height = dic['height'] if event.temp_id == 2 else ''
		person = Person(signup_id=signup.id, name=dic['name'], email=dic['email'], 
				adress=dic['adress'], year=dic['year'], telNum=dic['telNum'], selectSize=selectSize, 
				weight=weight, height=height)
		db.session.add(person)
		db.session.commit()
		if event.temp_id == 2:
			skiEver = True if dic['skiEver'] == 'true' else False
			skiInst = True if dic['skiInst'] == 'true' else False
			isLent = True if dic['isLent'] == 'true' else False
			if isLent:
				skiLent = ", ".join(dic['skiLent'])
				winter = Winter(signup_id=signup.id, skiEver=skiEver, skiSkill=dic['skiSkill'],
					skiInst=skiInst, passBuy=dic['passBuy'], isLent=isLent, skiLent=skiLent)
			else:
				person.height= ''
				person.weight= ''
				db.session.commit()
				winter = Winter(signup_id=signup.id, skiEver=skiEver, skiSkill=dic['skiSkill'],
					skiInst=skiInst, passBuy=dic['passBuy'], isLent=isLent)
			db.session.add(winter)
			db.session.commit()
		if event.temp_id == 4:
			isBike = True if dic['isBike'] == 'true' else False
			older = Older(signup_id=signup.id, isBike=isBike, attrac=dic['attrac'],
					pray=dic['pray'], freeTime=dic['freeTime'])
			db.session.add(older)
			db.session.commit()
		if event.temp_id == 6:
			for son in lst:
				son.signup_id = signup.id
				db.session.add(son)
				db.session.commit()
		flash('Udało się zapisać!', category='success')
	return person

def get_member(dic, event, num):
	if event.temp_id == 3:
		member = Person(name=dic[f'name{num}'], email=dic[f'email{num}'], adress=dic[f'adress{num}'],
					year=dic[f'year{num}'], telNum=dic[f'telNum{num}'], is_contact=False)
		return member 
	if event.temp_id == 6:
		member = Person(name=dic[f'name{num}'], email=dic[f'email{num}'], adress=dic[f'adress{num}'],
					 year=dic[f'year{num}'], telNum=dic[f'telNum{num}'], selectSize=dic[f'selectSize{num}'], is_contact=False)
		return member 

def db_add_new_blacklist(email, number):
	if email and number:
		new_item = Blacklist(email=email, number=number)
	elif email:
		new_item = Blacklist(email=email)
	elif number:
		new_item = Blacklist(number=number)
	db.session.add(new_item)
	db.session.commit()
	flash('Dodano do czarnej listy', category='success')
	logger.info(f'BL: Dodano do czarnej listy {new_item}')

def db_add_year(year, years):
	if years:
		years[-1].is_active = False
	db.session.add(year)
	db.session.commit()

def db_update_event(event):
	name = request.form.get('name')
	date = date_from_str(request.form.get('date'), True)
	mail_temp = request.form.get('mail_temp')
	tup = check_event(name=name, date=date, template="test", mail_temp=mail_temp, num=event.id)
	if tup[0]:
		event.name = name
		event.date = date
		event.mail_temp = mail_temp
		db.session.commit()
		flash(f'Zaktualizowano {event.name}', category='success')
		logger.info(f'EVENT: Zaktualizowano {event.name}')
		return True
	else:
		return False

def db_new_event(year):
	check = True
	name = request.form.get('name')
	date = date_from_str(request.form.get('date'), True)
	template = request.form.get('template')
	mail_temp = request.form.get('mail_temp')
	tup = check_event(name=name, date=date, template=template, mail_temp=mail_temp, num='nowa')
	if tup[0]:
		temp_id = int(template[8])
		event = Events(name=name, year_id=year.id, temp_id=temp_id, date=date, mail_temp=mail_temp)
		db.session.add(event)
		db.session.commit()
		flash(f'Dodano {event.name} do wydarzeń', category='success')
		logger.info(f'EVENT: Dodano {event.name} do wydarzeń')
		backup = False
	else:
		backup = tup[1]
		check = False
	return (check, backup)

def db_add_event(year, years):
	dic = {}
	lst_event = []
	check = True
	for i in range(year.event_num):
		name = request.form.get(f'name{i+1}')
		template = request.form.get(f'template{i+1}')
		date = date_from_str(request.form.get(f'date{i+1}'), True)
		mail_temp = request.form.get(f'mail_temp{i+1}')
		tup = check_event(name, date, template, mail_temp, i+1)
		if tup[0]:
			temp_id = int(template[8])
			new_event = Events(name=name, temp_id=temp_id, date=date, mail_temp=mail_temp)
			lst_event.append(new_event)
			dic[i+1] = new_event
		else:
			dic[i+1] = tup[1]
			check = False 
	if check:
		db_add_year(year, years)
		for event in lst_event:
			event.year_id = year.id
			db.session.add(event)
			db.session.commit()
		flash(f'Dodano akcje do wybranego roku', category='success')
		logger.info(f'EVENT: Dodano akcje do wybranego roku: {year.name}')
	return (dic, check)

def get_sumup(event, lst):
	summary = {'num_signup':len(lst), 'num_active':0}
	sizes = ['xs', 's', 'm', 'l', 'xl', 'xxl']
	if event.temp_id in (1, 4):
		for size in sizes:
			summary.update({size:0})
	if event.temp_id == 2:
		winters = ['n_skiEver', 'n_skiInst', 'n_isLent', 'discount', 'normal', 'narty', 
				'buty', 'deska', 'kask', 'kijki', 'gogle']
		for winter in winters:
			summary.update({winter:0})
	if event.temp_id == 3:
		turnaments = ['players', 'sleep', 'young', 'old']
		for turnament in turnaments:
			summary.update({turnament:0})
	if event.temp_id == 6:
		summary.update({'members':0})
		for size in sizes:
			summary.update({size:0})

	for signup in lst:
		for member in signup.person:
			if member.is_verified:
				summary['num_active'] += 1
			if event.temp_id in (1, 4, 6):
				summary[member.selectSize.lower()] += 1
			if event.temp_id == 6:
				summary['members'] += 1
		if event.temp_id == 2:
			win = signup.winter[0]
			if win.skiEver:
				summary['n_skiEver'] += 1
			if win.skiInst:
				summary['n_skiInst'] += 1
			if win.isLent:
				summary['n_isLent'] += 1
			if win.passBuy == 'Ulgowy':
				summary['discount'] += 1
			else:
				summary['normal'] += 1
			if win.isLent:
				if 'Narty' in win.skiLent:
					summary['narty'] += 1
				if 'Buty' in win.skiLent:
					summary['buty'] += 1
				if 'Deska' in win.skiLent:
					summary['deska'] += 1
				if 'Kask' in win.skiLent:
					summary['kask'] += 1
				if 'Kijki' in win.skiLent:
					summary['kijki'] += 1
				if 'Gogle' in win.skiLent:
					summary['gogle'] += 1
		if event.temp_id == 3:
			tur = signup.turnament[0]
			summary['players'] += tur.teamNum 
			summary['sleep'] += tur.peopleNum
			if tur.ageCat == 'Młodsi: 2010-2014 (drużyna składa się z 6 osób + bramkarz)':
				summary['young'] += 1
			else:
				summary['old'] += 1
	return summary

def test_signup(event, number):
	for i in range(number):
		date = str(datetime.datetime.now())
		date = date_from_str(date, False)
		signup = Signup(event_id=event.id, date=date)
		db.session.add(signup)
		db.session.commit()
		person = Person(signup_id=signup.id, name=f'{i} Opiekun', email='email@email.com', telNum='345456567')
		db.session.add(person)
		db.session.commit()
		turnament = Turnament(signup_id=signup.id, ageCat='Starsi: 2004-2009 (drużyna składa się z 5 osób + bramkarz)', teamName=f'{i} teamName',
						teamFrom='teamFrom', teamNum=10, peopleNum=5, say='elo ziombelo')
		db.session.add(turnament)
		db.session.commit()
		for j in range(10):
			player = Person(signup_id=signup.id, name=f'name {i}', email='edsadas@dsad.pl', 
				adress='dasdasdsadd', year='1993', telNum='354635457', is_contact=False)
			db.session.add(player)
			db.session.commit()



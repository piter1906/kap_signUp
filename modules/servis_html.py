from flask import flash, request, redirect, url_for, session, render_template
from flask_login import login_required, current_user
from flask_mail import Mail, Message
from website import mail
from website import db
from modules.check_module import *
from website.models import Year, Blacklist, Events, Signup, Person, Turnament, Winter, Older, Basic
import datetime 

'attrac', 'pray', 'freeTime'

def change_polish_char(event, lst):
	chars = 'ąćęłńśźżĄĆĘŁŃŚŹŻ'
	replace ='acelnszzACELNSZZ'
	translator = str.maketrans(chars, replace)
	for signup in lst:
		if event.temp_id != 3:
			for person in signup.person:
				person.name = person.name.translate(translator)
				person.adress = person.adress.translate(translator)
			for basic in signup.basic:
				basic.intro = basic.intro.translate(translator)
		if event.temp_id == 3:
			for person in signup.person:
				person.name = person.name.translate(translator)
				if not person.is_contact:
					person.adress = person.adress.translate(translator)
			for turn in signup.turnament:
				turn.teamName = turn.teamName.translate(translator)
				turn.teamFrom = turn.teamFrom.translate(translator)
				turn.say = turn.say.translate(translator)
		if event.temp_id == 4:
			for old in signup.older:
				old.attrac = old.attrac.translate(translator)
				old.pray = old.pray.translate(translator)
				old.freeTime = old.freeTime.translate(translator)
	return lst


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
	#flash(f'dict: {dic}')
	return dic

def send_mail(event, person):
    msg = Message(f'Witaj {person.name}', sender = 'kapszlaksend@gmail.com', recipients = [person.email])
    msg.body = f"Siemano ziomek. Udało Ci się zapisać na akcję {event.name}. \n Oto treść maila: {event.mail_temp}"
    mail.send(msg)
    msg1 = Message(f'Nowy zapis dla {event.name}', sender = 'kapszlaksend@gmail.com', recipients = ['brpiotrwojtowicz@gmail.com'])
    msg1.body = f"Wlasnie zapisał sie {person.name} na akcję {event.name}"
    mail.send(msg1)


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
				skiLent = ''
				for item in dic['skiLent']:
					skiLent += item + ', '
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
    new_item = Blacklist(email=email, number=number)
    db.session.add(new_item)
    db.session.commit()
    flash('Dodano do czarnej listy', category='success')

def db_add_year(name, event_num, years):
	if not years:
		new_year = Year(name=name, event_num=event_num)
		db.session.add(new_year)
		db.session.commit()
	else:
		for item in years:
			item.is_active = False
		db.session.commit()
		new_year = Year(name=name, event_num=event_num)
		db.session.add(new_year)
		db.session.commit()

def db_update_event(event):
	dic = {}
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
		if template == 'Szablon 1':
			temp_id = 1
		if template == 'Szablon 2':
			temp_id = 2
		if template == 'Szablon 3':
			temp_id = 3
		if template == 'Szablon 4':
			temp_id = 4
		if template == 'Szablon 5':
			temp_id = 5
		if template == 'Szablon 6':
			temp_id = 6
		event = Events(name=name, year_id=year.id, temp_id=temp_id, date=date, mail_temp=mail_temp)
		db.session.add(event)
		db.session.commit()
		flash(f'Dodano {event.name} do wydarzeń', category='success')
		backup = False
	else:
		backup = tup[1]
		check = False
	return (check, backup)

def db_add_event(year):
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
			if template == 'Szablon 1':
				temp_id = 1
			if template == 'Szablon 2':
				temp_id = 2
			if template == 'Szablon 3':
				temp_id = 3
			if template == 'Szablon 4':
				temp_id = 4
			if template == 'Szablon 5':
				temp_id = 5
			if template == 'Szablon 6':
				temp_id = 6
			new_event = Events(name=name, year_id=year.id, temp_id=temp_id, date=date, mail_temp=mail_temp)
			lst_event.append(new_event)
			dic[i+1] = new_event
		else:
			dic[i+1] = tup[1]
			check = False 
	if check:
		for event in lst_event:
			db.session.add(event)
			db.session.commit()
		year.first_add = True
		db.session.commit()
		flash('Dodano akcje do wybranego roku', category='success')
	return (dic, check)

def get_sumup(event, lst):
	dic = {}
	dic_1 = {}
	dic_2 = {}
	dic_3 = {}
	dic['num_signup'] = len(lst)
	dic['num_active'] = 0
	temp1 = ['xs', 's', 'm', 'l', 'xl', 'xxl']
	temp2 = ['n_skiEver', 'n_skiInst', 'n_isLent', 'discount', 'normal', 'narty', 
				'buty', 'deska', 'kask', 'kijki', 'gogle']
	temp3 = ['players', 'sleep', 'young', 'old']
	if event.temp_id in (1, 4):
		for item in temp1:
			dic_1[item] = 0
		dic.update(dic_1)
	if event.temp_id == 2:	
		for item in temp2:
			dic_2[item] = 0
		dic.update(dic_2)
	if event.temp_id == 3:	
		for item in temp3:
			dic_3[item] = 0
		dic.update(dic_3)
	if event.temp_id == 6:
		for item in temp1:
			dic_1[item] = 0
		dic.update(dic_1)
		dic['members'] = 0

	for signup in lst:
		for member in signup.person:
			if member.is_verified:
				dic['num_active'] += 1
			if event.temp_id in (1, 4, 6):
				if member.selectSize == 'XS':
					dic['xs'] += 1
				elif member.selectSize == 'S':
					dic['s'] += 1
				elif member.selectSize == 'M':
					dic['m'] += 1
				elif member.selectSize == 'L':
					dic['l'] += 1
				elif member.selectSize == 'XL':
					dic['xl'] += 1
				elif member.selectSize == 'XXL':
					dic['xxl'] += 1
			if event.temp_id == 6:
				dic['members'] += 1
		if event.temp_id == 2:
			for win in signup.winter:
				if win.skiEver:
					dic['n_skiEver'] += 1
				if win.skiInst:
					dic['n_skiInst'] += 1
				if win.isLent:
					dic['n_isLent'] += 1
				if win.passBuy == 'Ulgowy':
					dic['discount'] += 1
				else:
					dic['normal'] += 1
				if win.isLent:
					if 'Narty' in win.skiLent:
						 dic['narty'] += 1
					if 'Buty' in win.skiLent:
						 dic['buty'] += 1
					if 'Deska' in win.skiLent:
						 dic['deska'] += 1
					if 'Kask' in win.skiLent:
						 dic['kask'] += 1
					if 'Kijki' in win.skiLent:
						 dic['kijki'] += 1
					if 'Gogle' in win.skiLent:
						 dic['gogle'] += 1
		if event.temp_id == 3:
			for tur in signup.turnament:
				dic['players'] += tur.teamNum 
				dic['sleep'] += tur.peopleNum
				if tur.ageCat == 'Do 14 roku życia (drużyna składa się z 6 osób + bramkarz)':
					dic['young'] += 1
				else:
					dic['old'] += 1
	return dic

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
		turnament = Turnament(signup_id=signup.id, ageCat='Od 14 do 19 roku życia (drużyna składa się z 5 osób + bramkarz)', teamName=f'{i} teamName',
						teamFrom='teamFrom', teamNum=10, peopleNum=5, say='elo ziombelo')
		db.session.add(turnament)
		db.session.commit()
		for j in range(10):
			player = Person(signup_id=signup.id, name=f'name {i}', email='edsadas@dsad.pl', 
				adress='dasdasdsadd', year='1993', telNum='354635457', is_contact=False)
			db.session.add(player)
			db.session.commit()



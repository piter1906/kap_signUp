from flask import flash, request
from website import db
from website.models import SignUpData, Year, Blacklist, Events, Template1, Template2, Template3

def get_form_val(lst):
	dic = {}
	if lst:
		for val in lst:
			dic[val] = request.form.get(val)
	return dic

def db_add_new_sigup(dic, id_template):
	if id_template == 1:
		new_it = SignUpData(selectEvent=dic['selectEvent'], 
	                name=dic['name'], email=dic['email'], adress=dic['adress'], year=dic['year'], 
	                telNum=dic['telNum'], howMany=dic['howMany'], whereKnew=dic['whereKnew'],
	                intro=dic['intro'], selectSize=dic['selectSize'])
		db.session.add(new_it)
		db.session.commit()
		flash('Udało się zapisać!', category='success')
	else:
		flash('To nie to id', category='error')

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

def db_add_event(year):
	for i in range(year.event_num):
		name = request.form.get(f'name{i+1}')
		new_event = Events(name=name, year_id=year.id)
		db.session.add(new_event)
		db.session.commit() 
		template = request.form.get(f'template{i+1}')
		if template == 'Szablon 1':
			temp_name = f'Szablon dla akcji o id {new_event.id}'
			new_temp = Template1(temp_name=temp_name, event_id=new_event.id)
			db.session.add(new_temp)
			db.session.commit()
		elif template == 'Szablon 2':
			temp_name = f'Szablon dla akcji o id {new_event.id}'
			new_temp = Template2(temp_name=temp_name, event_id=new_event.id)
			db.session.add(new_temp)
			db.session.commit() 
		elif template == 'Szablon 3':
			temp_name = f'Szablon dla akcji o id {new_event.id}'
			new_temp = Template3(temp_name=temp_name, event_id=new_event.id)
			db.session.add(new_temp)
			db.session.commit()
	flash('Dodano akcje do wybranego roku', category='success')




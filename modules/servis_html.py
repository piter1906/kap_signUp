from flask import flash, request
from website import db
from website.models import SignUpData, Year, Blacklist, Events, Template1, Template2, Template3

def get_form_val(lst):
	dic = {}
	if lst:
		for val in lst:
			dic[val] = request.form.get(val)
	return dic

def db_add_new_sigup(dic, event):
	if event.temp_id == 1:
		template = Template1(temp_name="testowe", event_id=event.id, name=dic['name'], email=dic['email'])
		db.session.add(template)
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
		template = request.form.get(f'template{i+1}')
		if template == 'Szablon 1':
			temp_id = 1
			new_event = Events(name=name, year_id=year.id, temp_id=temp_id)
			db.session.add(new_event)
			db.session.commit()
		elif template == 'Szablon 2':
			temp_id = 2
			new_event = Events(name=name, year_id=year.id, temp_id=temp_id)
			db.session.add(new_event)
			db.session.commit()
		elif template == 'Szablon 3':
			temp_id = 3
			new_event = Events(name=name, year_id=year.id, temp_id=temp_id)
			db.session.add(new_event)
			db.session.commit()
	flash('Dodano akcje do wybranego roku', category='success')




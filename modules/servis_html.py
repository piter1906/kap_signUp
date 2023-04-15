from flask import flash, request
from website import db
from website.models import SignUpData, EventsNew

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







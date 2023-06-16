import pytest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from website import db, app
from modules.servis_html import *
from website.models import Blacklist, User, Events, Year, Signup, Basic, Older, Winter, Person, Turnament 

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

def test_save_data(client):
    years = Year.query.all()
    year = Year(name='Testowa nazwa', event_num=4)
    assert db_add_year(year, years) == True

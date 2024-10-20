from os import environ
import re

from app import app, db
from server.models import Animal, Enclosure, Zookeeper

class TestApp:
    '''Flask application in app.py'''

    with app.app_context():
        a_1 = Animal()
        a_2 = Animal()
        e = Enclosure()
        z = Zookeeper()
        e.animals = [a_1, a_2]
        z.animals = [a_1, a_2]
        db.session.add_all([a_1, a_2, e, z])
        db.session.commit()

    def test_animal_route(self):
        '''has a resource available at "/animal/<id>".'''
        response = app.test_client().get('/animal/1')
        assert(response.status_code == 200)

    def test_animal_route_has_attrs(self):
        '''displays attributes in animal route in <ul> tags called Name, Species.'''
        # name_ul = re.compile(r'\<ul\>[Nn]ame.+')
        # species_ul = re.compile(r'\<ul\>[Ss]pecies.+')

        name_li = re.compile(r'<li>[Nn]ame:\s*\w+<\/li>')
        species_li = re.compile(r'<li>[Ss]pecies:\s*\w+<\/li>')

        
        response = app.test_client().get('/animal/1')

        assert(len(name_li.findall(response.data.decode())) == 1)
        assert(len(species_li.findall(response.data.decode())) == 1)

    def test_animal_route_has_many_to_one_attrs(self):
        '''displays attributes in animal route in <ul> tags called Zookeeper, Enclosure.'''
        # zookeeper_ul = re.compile(r'\<ul\>Zookeeper.+')
        # enclosure_ul = re.compile(r'\<ul\>Enclosure.+')
        zookeeper_ul = re.compile(r'<li>[Zz]ookeeper:\s*\w+\s*\w+<\/li>')
        enclosure_ul = re.compile(r'<li>[Ee]nclosure:\s*\w+<\/li>')
        
        response = app.test_client().get('/animal/1')

        assert(len(zookeeper_ul.findall(response.data.decode())) == 1)
        assert(len(enclosure_ul.findall(response.data.decode())) == 1)

    def test_zookeeper_route(self):
        '''has a resource available at "/zookeeper/<id>".'''
        response = app.test_client().get('/zookeeper/1')
        assert(response.status_code == 200)

    def test_zookeeper_route_has_attrs(self):
        '''displays attributes in zookeeper route in <ul> tags called Name, Birthday.'''
        # name_ul = re.compile(r'\<ul\>[Nn]ame.+')
        # birthday_ul = re.compile(r'\<ul\>[Bb]irthday.+')
        name_ul = re.compile(r'<li>[Nn]ame:\s*\w+\s*\w+<\/li>')
        birthday_ul = re.compile(r'<li>[Bb]irthday:\s*\d{4}-\d{2}-\d{2}<\/li>')
        
        response = app.test_client().get('/zookeeper/1')

        assert(len(name_ul.findall(response.data.decode())) == 1)
        assert(len(birthday_ul.findall(response.data.decode())) == 1)

    def test_zookeeper_route_has_one_to_many_attr(self):
        '''displays attributes in zookeeper route in <ul> tags called Animal.'''
        # animal_ul = re.compile(r'\<ul\>Animal.+')
        animal_ul = re.compile(r'<li>[Aa]nimal:\s*\w+<\/li>')
        
        id = 1
        response = app.test_client().get(f'/zookeeper/{id}')
        assert len(animal_ul.findall(response.data.decode()))

    def test_enclosure_route(self):
        '''has a resource available at "/enclosure/<id>".'''
        response = app.test_client().get('/enclosure/1')
        assert(response.status_code == 200)

    def test_enclosure_route_has_attrs(self):
        '''displays attributes in enclosure route in <ul> tags called Environment, Open to Visitors.'''
        # environment_ul = re.compile(r'\<ul\>[Ee]nvironment.+')
        # open_ul = re.compile(r'\<ul\>[Oo]pen\s[Tt]o\s[Vv]isitors.+')
        environment_ul = re.compile(r'<li>[Ee]nvironment:\s*\w+<\/li>')
        open_ul = re.compile(r'<li>[Oo]pen\s[Tt]o\s[Vv]isitors:\s*(True|False)<\/li>')
        
        response = app.test_client().get('/enclosure/1')

        assert(len(environment_ul.findall(response.data.decode())) == 1)
        assert(len(open_ul.findall(response.data.decode())) == 1)

    def test_enclosure_route_has_one_to_many_attr(self):
        '''displays attributes in enclosure route in <ul> tags called Animal.'''
        # animal_ul = re.compile(r'\<ul\>Animal.+')
        animal_ul = re.compile(r'<li>[Aa]nimal:\s*\w+<\/li>')
        
        id = 1
        response = app.test_client().get(f'/enclosure/{id}')
        assert len(animal_ul.findall(response.data.decode()))
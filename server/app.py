#!/usr/bin/env python3

from models import db, Scientist, Mission, Planet
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
api = Api(app)

db.init_app(app)


@app.route('/')
def home():
    return ''

class Scientists(Resource):
    def get(self):
        scientists = [scientist.to_dict() for scientist in Scientist.query.all()]
        return make_response( scientists, 200)
    
    def post(self):
        data = request.get_json()

        try:
            new_scientist = Scientist(
                name = data.get('name'),
                field_of_study = data.get('field_of_study')
            )

            db.session.add(new_scientist)
            db.session.commit()
            return make_response( new_scientist.to_dict(), 201 )
        except ValueError:
            return make_response( {'errors': ['validation errors']}, 400 )
    
api.add_resource(Scientists, '/scientists', endpoint='scientists')


class ScientistById(Resource):
    def get(self, id):
        scientist = Scientist.query.filter(Scientist.id == id).first()

        if not scientist:
            return make_response(jsonify({ 'error': 'Scientist not found'}), 404 )
        
        return make_response( scientist.to_dict(only=('id', 'name', 'missions', 'field_of_study')), 200 )
    
    def patch(self, id):
        scientist = Scientist.query.filter(Scientist.id == id).first()

        if not scientist:
            return make_response( {'error': 'Scientist not found'}, 404 )
        
        try:
            setattr(scientist, 'name', request.get_json()['name'])
            setattr(scientist, 'field_of_study', request.get_json()['field_of_study'])

            db.session.add(scientist)
            db.session.commit()

            return make_response( scientist.to_dict(), 202 )
        
        except ValueError:
            return make_response( {'errors': ['validation errors']}, 400 )
    
    def delete(self, id):
        scientist = Scientist.query.filter(Scientist.id == id).first()
        if scientist:            
            db.session.delete(scientist)
            db.session.commit()

            return make_response( {'message': 'Scientist successfully deleted.'}, 204 )
        
        return make_response( {'error': "Scientist not found"}, 404 )
    
api.add_resource(ScientistById, '/scientists/<int:id>', endpoint='<int:id>')

class Planets(Resource):
    def get(self):
        planets = [planet.to_dict() for planet in Planet.query.all()]
        return make_response( planets, 200)
    
api.add_resource(Planets, '/planets', endpoint='planets')

class Missions(Resource):
    def post(self):
        json = request.get_json()

        try:
            new_mission = Mission(
            name = json.get('name'),
            scientist_id = json.get('scientist_id'), 
            planet_id = json.get('planet_id')
            )
    
            db.session.add(new_mission)
            db.session.commit()

            return make_response( new_mission.to_dict(), 201 )
        
        except ValueError:
            return make_response( {'errors': ['validation errors']}, 400 )
        
api.add_resource(Missions, '/missions', endpoint='missions')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

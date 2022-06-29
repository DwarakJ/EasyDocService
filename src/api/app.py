from flask import jsonify, Flask
import os
from src.service.NotesService import NotesService
from flask_marshmallow import Marshmallow
import json

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
ma = Marshmallow(app)

class NoteSchema(ma.Schema):
    class Meta:
        fields = ('notes_id', 'name', 'details', 'note_type', 'created_time', 'modified_time')

note_schema = NoteSchema()
notes_schema = NoteSchema(many=True)


db_url = "sqlite:///mynote.sqlite"

note_service = NotesService(db_url)


@app.route('/notes_details', methods=["GET"])
def all_notes_details():
    note = note_service.retrieve_notes()
    if note:
        result = notes_schema.dump(note)
        return jsonify(result.data)
    else:
        return jsonify(message="Requested note doesn't exist"), 404

@app.route('/notes_details/<int:note_id>', methods=["GET"])
def notes_details(note_id: int):
    note = note_service.retrieve_notes_filter_by_noteid(note_id).first()
    if note:
        result = note_schema.dump(note)
        return jsonify(result.data)
    else:
        return jsonify(message="Requested note doesn't exist"), 404


# @app.route('/add_planet', methods=['POST'])
# def add_planet():
#     planet_name = request.form['planet_name']
#     test = Planet.query.filter_by(planet_name=planet_name).first()
#     if test:
#         return jsonify("There is already a planet by that name"), 409
#     else:
#         planet_type = request.form['planet_type']
#         home_star = request.form['home_star']
#         mass = float(request.form['mass'])
#         radius = float(request.form['radius'])
#         distance = float(request.form['distance'])

#         new_planet = Planet(planet_name=planet_name,
#                             planet_type=planet_type,
#                             home_star=home_star,
#                             mass=mass,
#                             radius=radius,
#                             distance=distance)

#         db.session.add(new_planet)
#         db.session.commit()
#         return jsonify(message="You added a planet"), 201


# @app.route('/update_planet', methods=['PUT'])
# def update_planet():
#     planet_id = int(request.form['planet_id'])
#     planet = Planet.query.filter_by(planet_id=planet_id).first()
#     if planet:
#         planet.planet_name = request.form['planet_name']
#         planet.planet_type = request.form['planet_type']
#         planet.home_star = request.form['home_star']
#         planet.mass = float(request.form['mass'])
#         planet.radius = float(request.form['radius'])
#         planet.distance = float(request.form['distance'])
#         db.session.commit()
#         return jsonify(message="You updated a planet"), 202
#     else:
#         return jsonify(message="That planet does not exist"), 404


# @app.route('/remove_planet/<int:planet_id>', methods=['DELETE'])
# def remove_planet(planet_id: int):
#     planet = Planet.query.filter_by(planet_id=planet_id).first()
#     if planet:
#         db.session.delete(planet)
#         db.session.commit()
#         return jsonify(message="You deleted a planet"), 202
#     else:
#         return jsonify(message="That planet does not exist"), 404


if __name__ == '__main__':
    app.run()
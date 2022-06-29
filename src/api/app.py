from datetime import datetime
from flask import jsonify, Flask, request
import os
from src.repository import db_operations
from src.service.NotesService import NotesService
from src.domain.notes import Notes

basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)

db_url = "sqlite:///mynote.sqlite"

note_service = NotesService(db_url)


@app.route('/notes_details', methods=["GET"])
def all_notes_details():
    result = note_service.retrieve_notes()
    if result:
        return jsonify(result)
    else:
        return jsonify(message="Requested note doesn't exist"), 404

@app.route('/notes_details/<int:note_id>', methods=["GET"])
def notes_details(note_id: int):
    note = note_service.retrieve_notes_filter_by_noteid(note_id)
    if note:
        return jsonify(note)
    else:
        return jsonify(message="Requested note doesn't exist"), 404


@app.route('/add_note', methods=['POST'])
def add_note():
    
    new_note = Notes(None,request.form['name'],
                        request.form['details'],
                        datetime.now(),
                        datetime.now(),
                        request.form['type']
                        )

    note_service.add_notes([new_note])
    return jsonify(message="Successfully added note"), 201


@app.route('/update_note', methods=['PUT'])
def update_note():
    note_id = int(request.form['id'])
    if note_id:
        updated_note = Notes(None,request.form['name'],
                            request.form['details'],
                            datetime.now(),
                            datetime.now(),
                            request.form['type']
                            )
        note_service.update_note(note_id, updated_note)
        return jsonify(message="Note updated successfully"), 202
    else:
        return jsonify(message="Note does not exist"), 404


@app.route('/remove_note/<int:note_id>', methods=['DELETE'])
def remove_planet(note_id: int):
    if note_service.delete_note(note_id):
        return jsonify(message="Note deleted successfully"), 202
    else:
        return jsonify(message="Note does not exist"), 404


if __name__ == '__main__':
    app.run()
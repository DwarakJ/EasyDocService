# EasyDocService
Python,  SQLAlchemy, Sqlite

# Note Types
    TECH = 1
    KT = 2
    MOM = 3
    IDEAS = 4
    TODO = 5
    
# REST API Endpoints

Method: GET
http://127.0.0.1:5000/notes_details/<id>

All notes
http://127.0.0.1:5000/notes_details/

Method: PUT
http://127.0.0.1:5000/update_note

form:
id: <id>
name: "some name"
type: note_type
details: "some details"

Method: POST
http://127.0.0.1:5000/add_note

form:
name: "some name"
type: note_type
details: "some details"

Method: DELETE
http://127.0.0.1:5000/remove_note/<id>

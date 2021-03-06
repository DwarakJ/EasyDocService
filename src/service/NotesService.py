from datetime import datetime
import datetime as dt
from src.domain.notes import Notes, NoteType
import json
from src.repository import db_operations
import os

class NotesService:

    def __init__(self, db_url) -> None:
        self.db_url = db_url

    def initialize_db(self):
        try:
            db_operations.create_db(self.db_url)
            print("DB initialized successfully")
        except Exception as e:
            print(e)
        
    def add_notes(self, notes_list):
        try:
            db_operations.insert_notes(self.db_url, notes_list)
            print("Record inserted successfully")
        except Exception as e:
            print(e)
    
    def delete_db(self):
        try:
            if db_operations.drop_db():
                print("DB deleted successfully")
            else:
                print("DB doesn't exist")
        except Exception as e:
            print(e)

    def delete_note(self, note_id):
        print(note_id)
        try:
            if db_operations.delete_note(self.db_url, note_id):
                print("Note deleted successfully")
                return True
            else:
                print("Note doesn't exist")
                return False
        except Exception as e:
            print(e)

    def retrieve_notes(self):
        try:
            result = db_operations.query_notes(self.db_url)

            result_list = []

            for row in result:
                note = Notes(row.notes_id, row.name, row.details, row.created_time, row.modified_time, row.note_type)
                result_list.append(note.__dict__)
            return result_list
        except Exception as e:
            print(e)
        
    
    def retrieve_notes_filter_by_noteid(self, note_id):
        try:
            result = db_operations.query_notes_with_filter(self.db_url, note_id).first()
            
            note = Notes(result.notes_id, result.name, result.details, result.created_time, result.modified_time, result.note_type)

            return note.__dict__
        except Exception as e:
            print(e)

    
    def update_note(self, note_id, note):
        try:
            print(db_operations.update_note(self.db_url, note_id, note))
            print("Note updated successfully")
        except Exception as e:
            print(e)


if __name__ == "__main__":
    
    curr_dir = os.getcwd()

    with open(os.path.join(curr_dir, "config.json")) as f:
        config_data = json.load(f)

    db_url = "sqlite:///" + config_data["DB_NAME"]

    notes_service = NotesService(db_url)

    notes_service.initialize_db()

    notes_list = [Notes("Sprint demo", "MOM", datetime.now(), datetime.now(), NoteType.MOM.value),
    Notes("VBA", "TECH", datetime.now(), datetime.now(), NoteType.MOM.value),
    Notes("Product Design", "KT", datetime.now(), datetime.now(), NoteType.MOM.value),
    Notes("Sprint demo", "MOM", datetime.now()-dt.timedelta(days=20), datetime.now()-dt.timedelta(days=10), NoteType.MOM.value),
    Notes("VBA", "TECH", datetime.now()-dt.timedelta(days=10), datetime.now()-dt.timedelta(days=5), NoteType.MOM.value)
    ]
    notes_service.add_notes()

    notes_service.retrieve_notes()

    notes_service.retrieve_notes_filter_by_noteid(2)

    un = Notes("VBA", "TECH123", datetime.now(), datetime.now(), NoteType.TECH.value)
    notes_service.update_note(2, un)

    notes_service.retrieve_notes_filter_by_noteid(2)
    #notes_service.delete_db()
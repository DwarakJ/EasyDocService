from dataclasses import dataclass
from datetime import datetime
from src.domain.notes import Notes, NoteType

from src.repository import db_operations


class NotesService:

    def __init__(self, db_url) -> None:
        self.db_url = db_url

    def initialize_db(self):
        try:
            db_operations.create_db(self.db_url)
            print("DB initialized successfully")
        except Exception as e:
            print(e)
        
    def add_notes(self):
        n = Notes("MOM", datetime.now(), datetime.now(), NoteType.MOM.value)

        try:
            db_operations.insert_notes(self.db_url, n)
            print("Record inserted successfully")
        except Exception as e:
            print(e)
    
    def delete_note(self):
        
        try:
            db_operations.drop_db(self.db_url)
            print("DB deleted successfully")
        except Exception as e:
            print(e)

    def retrieve_notes(self):

        try:
            result = db_operations.query_notes(self.db_url)

            for row in result:
                print(row)
        except Exception as e:
            print(e)
        
if __name__ == "__main__":
    notes_service = NotesService("sqlite:///mynote.sqlite")

    notes_service.initialize_db()

    notes_service.add_notes()

    #notes_service.retrieve_notes()

    #notes_service.delete_note()
from src.api.app import ma

class NoteSchema(ma.Schema):
    class Meta:
        fields = ('notes_id', 'name', 'details', 'note_type', 'created_time', 'modified_time')
from flask_restplus.fields import Integer, String, Nested
from extensions import api

get_note_fields = api.model('Notes results',
                            {'Author': String(description='Note author'),
                             'Contents': String(description='Note contents')}
                            )

post_note_response = api.model('New note posted',
                               {'note_id': String(description='Note unique id')}
                               )

get_notes_fields = Nested(get_note_fields)

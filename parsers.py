from flask_restplus import reqparse

post_note_args = reqparse.RequestParser()
post_note_args.add_argument('data', type=str, location='json', required=False)
#post_note_args.add_argument('contents', type=str, lo, author, contentscation='json', required=True)
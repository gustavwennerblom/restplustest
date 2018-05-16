from flask import Flask, jsonify
from flask_restplus import Resource
from extensions import api
from serializers import get_note_fields, post_note_response
from parsers import post_note_args
import boto3
from boto3.dynamodb.conditions import Key
from uuid import uuid1

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///notes.db'
api.init_app(app)
api.__setattr__('app', app)

dynamodb = boto3.resource('dynamodb')
notes_table = dynamodb.Table('notes2')

@api.route('/test')
class Test(Resource):
    @api.marshal_with(post_note_response)
    def get(self):
        return dict(note_id="Fjams")

@api.route('/note')
class NotesCollection(Resource):
    @api.marshal_with(get_note_fields)
    def get(self):
        notes = notes_table.scan()
        print(notes['Items'])
        return notes['Items']

    @api.marshal_with(post_note_response)
    @api.expect(post_note_args, validate=True)
    def post(self):
        note_id = str(uuid1())
        notes_table.put_item(Item={'Key': note_id,
                                   'Author': api.payload.get('author'),
                                   'Contents': api.payload.get('contents')})

        return dict(note_id=note_id)

@api.route('/note/<id>')
class Note(Resource):
    @api.marshal_with(get_note_fields)
    def get(self, id):
        note = notes_table.query(KeyConditionExpression=Key('Key').eq(id))
        print(note['Items'])
        return note['Items'][0]

if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=False)
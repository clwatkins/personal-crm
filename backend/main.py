from datetime import datetime
import hashlib
import os

from flask import Flask
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
import pytz

app = Flask('personal-crm-backend')
cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('FLASK_DATABASE_URI')
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api = Api(app)

DEFAULT_LIMIT = 1_000
UTC = pytz.timezone('UTC')

parser = reqparse.RequestParser()
parser.add_argument('persons', type=str, help='Comma-separated list of person ids or names')
parser.add_argument('context', type=str, help='Commentary around the person context')
parser.add_argument('limit', type=int, help='Limit results to N values')


def _get_hash(text: str) -> str:
    return hashlib.sha1(text.encode('utf-8')).hexdigest()


class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    first_met = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.utcnow)
    first_met_comment = db.Column(db.Text, unique=False, nullable=True)


class Meetings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meeting_hash = db.Column(db.String(40), unique=False, nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    when = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.utcnow)
    what = db.Column(db.Text, unique=False, nullable=True)


class Plans(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plan_hash = db.Column(db.String(40), unique=False, nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    when = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.utcnow)
    what = db.Column(db.Text, unique=False, nullable=True)


class Persons(Resource):
    def get(self):
        args = parser.parse_args()
        people = People.query.limit(args.get('limit') or DEFAULT_LIMIT).all()
        print(people)
        return {'people': [{'id': person.id, 'name': person.name} for person in people]}

    def post(self):
        args = parser.parse_args()
        people_names = args['persons'].split(',')
        context = args['context']
        when = datetime.utcnow()

        db.session.add_all([People(
            name=person_name,
            first_met=when,
            first_met_comment=context) for person_name in people_names])

        db.session.commit()
        return 'Added people to database'


class See(Resource):
    def get(self):
        args = parser.parse_args()
        meetings = Meetings.query.order_by(Meetings.when.desc()).limit(args.get('limit') or DEFAULT_LIMIT).all()
        return {'meetings': [
            {'id': meeting.id, 'meeting_id': meeting.meeting_hash, 'person_id': meeting.person_id,
             'when': UTC.localize(meeting.when).isoformat(), 'what': meeting.what} for meeting in meetings]}

    def post(self):
        args = parser.parse_args()
        people_ids = args['persons'].split(',')
        context = args['context']
        when = datetime.utcnow()

        meeting_id = _get_hash(datetime.utcnow().isoformat() + context)

        db.session.add_all([Meetings(
            meeting_hash=meeting_id,
            person_id=person_id,
            when=when,
            what=context) for person_id in people_ids])

        db.session.commit()
        return 'Added meeting to database'


class Plan(Resource):
    def get(self):
        args = parser.parse_args()
        plans = Plans.query.order_by(Plans.when.desc()).limit(args.get('limit') or DEFAULT_LIMIT).all()
        return {'plans': [
            {'id': plan.id, 'plan_id': plan.meeting_hash, 'person_id': plan.person_id,
             'when': UTC.localize(plan.when).isoformat(), 'what': plan.what} for plan in plans]}

    def post(self):
        args = parser.parse_args()
        people_ids = args['persons'].split(',')
        context = args['context']
        when = datetime.utcnow()

        plan_id = _get_hash(datetime.utcnow().isoformat() + context)

        db.session.add_all([Plans(
            plan_hash=plan_id,
            person_id=person_id,
            when=when,
            what=context) for person_id in people_ids])

        db.session.commit()
        return 'Added plans to database'


api.add_resource(Persons, '/people')
api.add_resource(See, '/see')
api.add_resource(Plan, '/plan')

if __name__ == '__main__':
    app.run(debug=False, host=os.getenv('FLASK_HOST'), port=os.getenv('FLASK_PORT'))

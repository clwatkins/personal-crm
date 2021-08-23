from collections import Counter, defaultdict
from datetime import datetime
from dateutil import relativedelta
import hashlib
import math
import os

from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import pytz

app = Flask('personal-crm-backend')
CORS(app)

# We want this to fail at start if we haven't set a db connection
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['FLASK_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)

DEFAULT_LIMIT = 1_000
UTC = pytz.timezone('UTC')

parser = reqparse.RequestParser()
parser.add_argument('persons', type=str,
                    help='Comma-separated list of person ids or names')
parser.add_argument('context', type=str,
                    help='Commentary around the person context')
parser.add_argument('limit', type=int, help='Limit results to N values')


def _get_hash(text: str) -> str:
    return hashlib.sha1(text.encode('utf-8')).hexdigest()


class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    first_met = db.Column(db.DateTime, unique=False,
                          nullable=False, default=datetime.utcnow)
    first_met_comment = db.Column(db.Text, unique=False, nullable=True)


class Meetings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meeting_hash = db.Column(db.String(40), unique=False, nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey(
        'people.id'), nullable=False)
    when = db.Column(db.DateTime, unique=False,
                     nullable=False, default=datetime.utcnow)
    what = db.Column(db.Text, unique=False, nullable=True)


class Plans(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plan_hash = db.Column(db.String(40), unique=False, nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey(
        'people.id'), nullable=False)
    when = db.Column(db.DateTime, unique=False,
                     nullable=False, default=datetime.utcnow)
    what = db.Column(db.Text, unique=False, nullable=True)


class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey(
        'people.id'), nullable=False)
    when = db.Column(db.DateTime, unique=False,
                     nullable=False, default=datetime.utcnow)
    what = db.Column(db.Text, unique=False, nullable=True)


class Persons(Resource):
    def get(self):
        args = parser.parse_args()
        people = People.query.limit(args.get('limit') or DEFAULT_LIMIT).all()

        response = jsonify({'people': [{'id': person.id, 'name': person.name} for person in people]})
        return response

    def post(self):
        args = parser.parse_args()
        people_names = args['persons'].split(',')
        context = args['context']
        when = datetime.utcnow()

        # Add new people to database
        db.session.add_all([
            People(
                name=person_name,
                first_met=when,
                first_met_comment=context) for person_name in people_names])

        db.session.commit()

        # Get newly-created person ids and use to add meetings as well
        people = People.query.limit(args.get('limit') or DEFAULT_LIMIT).all()

        return 'Added people to database'


class See(Resource):
    def get(self):
        args = parser.parse_args()
        meetings_people = db.session.query(Meetings, People).join(People).order_by(
            Meetings.when.desc()).limit(args.get('limit') or DEFAULT_LIMIT).all()

        meetings_return = {'meetings': []}
        for i, (meeting, person) in enumerate(meetings_people):
            meetings_return['meetings'].append(
                {
                    'local_query_id': i,
                    'meeting_hash': meeting.meeting_hash,
                    'person_name': person.name,
                    'when': UTC.localize(meeting.when).isoformat(),
                    'what': meeting.what
                }
            )

        response = jsonify(meetings_return)
        return response

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
        plans_people = db.session.query(Plans, People).join(People).order_by(
            Plans.when.desc()).limit(args.get('limit') or DEFAULT_LIMIT).all()

        plans_return = {'plans': []}
        for i, (plan, person) in enumerate(plans_people):
            plans_return['plans'].append(
                {
                    'local_query_id': i,
                    'plan_hash': plan.plan_hash,
                    'person_name': person.name,
                    'when': UTC.localize(plan.when).isoformat(),
                    'what': plan.what
                }
            )

        response = jsonify(plans_return)
        return response

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


class Note(Resource):
    def get(self, person_id):
        notes = Notes.query.filter_by(person_id=person_id).order_by(Notes.when.desc()).all()
        response = jsonify({'notes': [{'local_query_id': i, 'when': note.when, 'what': note.what} for i, note in enumerate(notes)]})
        return response

    def post(self, person_id):
        args = parser.parse_args()
        what = args['context']
        when = datetime.utcnow()

        db.session.add(Notes(
            person_id=person_id,
            when=when,
            what=what))

        db.session.commit()
        return 'Added note to database'


class Analytics(Resource):
    def get(self, analytics_type):
        args = parser.parse_args()

        if analytics_type == 'most-seen':
            meetings_people = db.session.query(Meetings, People).join(People).order_by(
                Meetings.when.desc()).all()

            meetings_people_all = []
            for _, (_, person) in enumerate(meetings_people):
                meetings_people_all.append(person.name)

            most_common_count = Counter(meetings_people_all).most_common(args.get('limit') or DEFAULT_LIMIT)

            response = jsonify({'data': [{'name': name, 'count': count} for name, count in most_common_count]})
            return response

        if analytics_type == 'to-see':
            min_meetings = 2
            min_timedelta_days = 0

            # Sort record of meetings in ascending order -- first to latest
            meetings_people = db.session.query(Meetings, People).join(People).order_by(
                Meetings.when.asc()).all()

            # Construct a record of how many times each person has been seen
            person_timeline = defaultdict(list)
            for meeting, person in meetings_people:
                person_timeline[person.name].append(meeting.when)

            to_see = []
            for person, meetings in person_timeline.items():
                # Skip anyone we haven't seen enough
                if len(meetings) < min_meetings:
                    continue

                # Calculate time since we last saw person
                last_seen_gap = relativedelta.relativedelta(datetime.utcnow(), meetings[-1]).normalized()

                if last_seen_gap.days > min_timedelta_days:
                    to_see.append(
                        {'name': person,
                         'total_meetings': len(meetings),
                         'days_since_last_seen': last_seen_gap.days
                         })

            eps = 1e-6
            to_see.sort(reverse=False,
                        # Sort list based on normalised length of time since last seen + number of meetings
                        key=lambda d: math.log(d['days_since_last_seen'] + eps) * math.log(d['total_meetings'])
                        )

            print(to_see)

            to_see = [{**info, **{'local_query_id': i}} for i, info in enumerate(to_see)]

            # Truncate list to desired limit
            to_see = to_see[:args.get('limit') or DEFAULT_LIMIT]
            return jsonify({'to_see': to_see})


api.add_resource(Persons, '/people')
api.add_resource(See, '/see')
api.add_resource(Plan, '/plan')
api.add_resource(Note, '/note/<person_id>')
api.add_resource(Analytics, '/analytics/<analytics_type>')

if __name__ == '__main__':
    app.run(debug=False, host=os.getenv(
        'FLASK_HOST'), port=os.getenv('FLASK_PORT'))

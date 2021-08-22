from datetime import datetime

from flask.cli import FlaskGroup

from src import app, db, People, Meetings, Notes, _get_hash

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    to_add = [
        People(name='Chris', first_met_comment='It is I'),
        People(name='Dom', first_met_comment='Tis someone else'),
        Meetings(meeting_hash=_get_hash(datetime.utcnow().isoformat() + 'chill'), person_id=1, when=datetime.utcnow(),
                 what='chill'),
        Meetings(meeting_hash=_get_hash(datetime.utcnow().isoformat() + 'eat'), person_id=1, when=datetime.utcnow(),
                 what='eat'),
        Meetings(meeting_hash=_get_hash(datetime.utcnow().isoformat() + 'sleep'), person_id=2, when=datetime.utcnow(),
                 what='sleep'),
        Meetings(meeting_hash=_get_hash(datetime.utcnow().isoformat() + 'repeat'), person_id=1, when=datetime.utcnow(),
                 what='repeat'),
        Notes(person_id=1, when=datetime.utcnow(), what='Cool guy'),
        Notes(person_id=2, when=datetime.utcnow(), what='Even cooler guy'),
        Notes(person_id=2, when=datetime.utcnow(), what='Learned something interesting...')
    ]

    db.session.add_all(to_add)
    db.session.commit()


if __name__ == "__main__":
    cli()

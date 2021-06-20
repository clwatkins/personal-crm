from flask.cli import FlaskGroup

from src import app, db, People

cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    person_1 = People(name='Chris', first_met_comment='It is I')
    person_2 = People(name='Dom', first_met_comment='Tis someone else')

    db.session.add(person_1)
    db.session.add(person_2)
    db.session.commit()


if __name__ == "__main__":
    cli()

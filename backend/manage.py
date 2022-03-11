import click

from src import main
from src.sql import crud, database, schemas

DB = database.SessionLocal()


@click.group()
def cli():
    pass


@cli.command()
def create_db():
    database.Base.metadata.drop_all(database.engine)
    database.Base.metadata.create_all(database.engine)
    click.echo("Database initialised successfully.")


@cli.command()
def seed_db():
    main.create_user(request=schemas.UserCreateRequest(email="hello@wor.ld", name="Me", raw_password="helloworld!"),
                     db=DB)
    seeded_user = crud.get_user(db=DB, email="hello@wor.ld", with_password=False)

    crud.create_persons(db=DB, user_id=seeded_user.id, names=["Chris", "Dom"], first_met_comment="The OG")
    crud.create_meeting(db=DB, user_id=seeded_user.id, person_ids=[1], what="Eat")
    crud.create_meeting(db=DB, user_id=seeded_user.id, person_ids=[1], what="Sleep")
    crud.create_meeting(db=DB, user_id=seeded_user.id, person_ids=[1], what="Code")
    crud.create_meeting(db=DB, user_id=seeded_user.id, person_ids=[2], what="Repeat")
    crud.create_note_for_person(db=DB, user_id=seeded_user.id, person_id=1, what="Cool guy")
    crud.create_note_for_person(db=DB, user_id=seeded_user.id, person_id=2, what="Even cooler guy")
    crud.create_note_for_person(db=DB, user_id=seeded_user.id, person_id=1,
                                what="Learned something interesting today...")
    click.echo("Database seeded successfully.")


if __name__ == '__main__':
    cli()

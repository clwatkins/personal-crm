import click

from src.sql import database
from src.sql import crud


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
    crud.create_persons(DB, names=["Chris", "Dom"], first_met_comment="The OG")
    crud.create_meeting(DB, person_ids=[1], what="Eat")
    crud.create_meeting(DB, person_ids=[1], what="Sleep")
    crud.create_meeting(DB, person_ids=[1], what="Code")
    crud.create_meeting(DB, person_ids=[2], what="Repeat")
    crud.create_note_for_person(DB, person_id=1, what="Cool guy")
    crud.create_note_for_person(DB, person_id=2, what="Even cooler guy")
    crud.create_note_for_person(DB, person_id=1, what="Learned something interesting today...")
    click.echo("Database seeded successfully.")


if __name__ == '__main__':
    cli()

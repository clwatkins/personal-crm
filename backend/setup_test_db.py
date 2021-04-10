from main import db, People
db.create_all()

person_1 = People(name='Chris', first_met_comment='myself!')
person_2 = People(name='Dom Aits')

db.session.add(person_1)
db.session.add(person_2)
db.session.commit()

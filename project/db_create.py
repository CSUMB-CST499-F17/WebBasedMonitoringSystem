#project/db_create.py
from project import db

db.create_all()

testUser1 = User('karara','password123')
testUser2 = User('puupy','cats')
db.session.add(testUser1)
db.session.add(testUser2)


db.session.commit()

from chat_bot import db
from chat_bot.models import User

db.create_all()

user1 = User(username="test01", email="test01@test.com", password="test01")
db.session.add(user1)
db.session.commit()
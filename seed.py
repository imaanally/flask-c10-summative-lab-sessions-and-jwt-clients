
from app import app
from models import db, User, Note


with app.app_context():
    db.drop_all()
    db.create_all()

    user1 = User(username="imaan")
    user1.set_password("Password123!")

    user2 = User(username="amina")
    user2.set_password("Password123!")

    db.session.add_all([user1, user2])
    db.session.commit()

    note1 = Note(
        title="My Study Plan",
        content="Study Flask and SQLAlchemy.",
        user_id=user1.id
    )

    note2 = Note(
        title="My Goals",
        content="Finish the productivity app.",
        user_id=user1.id
    )

    note3 = Note(
        title="Shopping List",
        content="Buy notebooks and pens.",
        user_id=user2.id
    )

    db.session.add_all([note1, note2, note3])
    db.session.commit()

    print("Database seeded successfully!")

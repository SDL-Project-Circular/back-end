from app import app, datastore
from model import db, Role


with app.app_context():
    db.create_all()
    datastore.find_or_create_role(name="admin", description="This user is an admin")
    db.session.commit()
    datastore.create_user(username="Shiva", email="admin@gmail.com", password="12345", roles=["admin"])
    db.session.commit()

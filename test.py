from app import app, datastore
from model import db, Role


with app.app_context():
    db.create_all()
    datastore.find_or_create_role(name="admin", description="This user is an admin")
    datastore.find_or_create_role(name="HOD", description="This user is the HOD")
    db.session.commit()
    datastore.create_user(username="Shiva", email="admin@gmail.com", password="12345", roles=["admin"])
    datastore.create_user(username="Harshita", email="hod@gmail.com", password="123456", roles=["HOD"])
    db.session.commit()

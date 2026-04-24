# Run once to setup db
from app import app
from extensions import db
from models.user import User
from models.field import Field

with app.app_context():
    db.create_all()
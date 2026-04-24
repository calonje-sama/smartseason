from werkzeug.security import generate_password_hash
from datetime import date
from models.user import User
from models.field import Field
from extensions import db

def seed_database():
    admin = User(
        name="Admin User",
        email="admin@test.com",
        password=generate_password_hash("1234"),
        role="admin"
    )

    agent = User(
        name="Field Agent",
        email="agent@test.com",
        password=generate_password_hash("1234"),
        role="agent"
    )

    db.session.add_all([admin, agent])
    db.session.commit()

    field = Field(
        name="Demo Field",
        crop_type="Maize",
        planting_date=date.today(),
        stage="Planted",
        status="Active",
        assigned_agent_id=agent.id
    )

    db.session.add(field)
    db.session.commit()
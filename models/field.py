from extensions import db
from datetime import date

class Field(db.Model):
    __tablename__ = 'fields'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    crop_type = db.Column(db.String(100), nullable=False)

    planting_date = db.Column(db.Date, nullable=False)

    stage = db.Column(db.String(20), nullable=False)  
    # Planted, Growing, Ready, Harvested

    status = db.Column(db.String(20), nullable=False, default="Active")
    # Active, At Risk, Completed

    assigned_agent_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def compute_status(self):
        if self.stage == "Harvested":
            return "Completed"

        days = (date.today() - self.planting_date).days

        if days > 14 and self.stage in ["Planted", "Growing"]:
            return "At Risk"

        return "Active"


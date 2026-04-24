from extensions import db

class FieldHistory(db.Model):
    __tablename__ = 'field_history'
    
    id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id'))
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', foreign_keys=[updated_by])
    old_stage = db.Column(db.String(20))
    new_stage = db.Column(db.String(20))
    note = db.Column(db.Text, nullable=True)

    timestamp = db.Column(db.DateTime, server_default=db.func.now())
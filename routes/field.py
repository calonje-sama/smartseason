from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user

from extensions import db
from datetime import datetime
from models.field import Field
from models.user import User
from models.field_history import FieldHistory

field_bp = Blueprint('field', __name__)

@field_bp.route('/fields/create', methods=['GET', 'POST'])
@login_required
def create_field():
    

    if current_user.role != 'admin':
        return "Unauthorized", 403

    agents = User.query.filter_by(role='agent').all()
    print(agents)

    if request.method == 'POST':
        field = Field(
            name=request.form['name'],
            crop_type=request.form['crop_type'],
            planting_date=datetime.strptime(request.form['planting_date'], "%Y-%m-%d"),
            stage="Planted",
            status="Active",
            assigned_agent_id=request.form['agent_id']
        )

        db.session.add(field)
        db.session.commit()

        return redirect('/dashboard')

    return render_template('create_field.html', agents=agents)

@field_bp.route('/fields/update/<int:field_id>', methods=['GET', 'POST'])
@login_required
def update_field(field_id):

    field = Field.query.get_or_404(field_id)

    if current_user.role != "agent":
        return "Unauthorized", 403

    if field.assigned_agent_id != current_user.id:
        return "Not your field", 403

    if request.method == "POST":
        old_stage = field.stage
        new_stage = request.form['stage']
        field.stage = new_stage

        history = FieldHistory(
            field_id=field.id,
            updated_by=current_user.id,
            old_stage=old_stage,
            new_stage=new_stage
        )

        db.session.add(history)
        db.session.commit()
        return redirect('/dashboard')

    return f"Field {field.name}"

from models.field_history import FieldHistory

@field_bp.route('/fields/history/<int:field_id>')
@login_required
def field_history(field_id):

    field = Field.query.get_or_404(field_id)

    history = FieldHistory.query.filter_by(field_id=field_id)\
        .order_by(FieldHistory.timestamp.desc()).all()

    return render_template(
        "field_history.html",
        field=field,
        history=history
    )

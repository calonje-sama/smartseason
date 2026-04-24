from flask import Blueprint, render_template, request, redirect, abort
from utils.decorators import role_required, owner_or_admin_required
from flask_login import login_required, current_user

from extensions import db
from datetime import datetime
from models.field import Field
from models.user import User
from models.field_history import FieldHistory

field_bp = Blueprint('field', __name__)

@field_bp.route('/fields/create', methods=['GET', 'POST'])
@login_required
@role_required('admin')
def create_field():    
    agents = User.query.filter_by(role='agent').all()

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
@role_required('agent')
@owner_or_admin_required(lambda field_id: Field.query.get_or_404(field_id))
def update_field(field_id):

    field = Field.query.get_or_404(field_id)

    if request.method == "POST":
        old_stage = field.stage
        new_stage = request.form['stage']
        field.stage = new_stage

        history = FieldHistory(
            field_id=field.id,
            updated_by=current_user.id,
            old_stage=old_stage,
            new_stage=new_stage,
            note=request.form.get('note')
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

    if current_user.role == "agent" and field.assigned_agent_id != current_user.id:
        abort(403)

    history = FieldHistory.query.filter_by(field_id=field_id)\
        .order_by(FieldHistory.timestamp.desc()).all()

    return render_template(
        "field_history.html",
        field=field,
        history=history, 
        now=datetime.now()
    )

from flask import Flask
from config import Config
from extensions import db, login_manager
from routes.auth import auth
from models.user import User
from models.field import Field
from routes.field import field_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(auth)
    app.register_blueprint(field_bp)

    return app

app = create_app()

from flask import render_template
from flask_login import login_required, current_user

@app.route('/dashboard')
@login_required
def dashboard():

    if current_user.role == "admin":
        fields = Field.query.all()
    else:
        fields = Field.query.filter_by(assigned_agent_id=current_user.id).all()

    # compute status
    for f in fields:
        f.status = f.compute_status()

    # ADMIN INSIGHTS (ONLY FOR ADMIN)
    total = active = risk = done = 0

    if current_user.role == "admin":
        total = len(fields)
        active = len([f for f in fields if f.status == "Active"])
        risk = len([f for f in fields if f.status == "At Risk"])
        done = len([f for f in fields if f.status == "Completed"])

    return render_template(
        "dashboard.html",
        user=current_user,
        fields=fields,
        total=total,
        active=active,
        risk=risk,
        done=done
    )


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=3000)
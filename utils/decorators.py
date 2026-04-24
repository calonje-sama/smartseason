from functools import wraps
from flask_login import current_user
from flask import abort

def role_required(role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if current_user.role != role:
                abort(403)
            return f(*args, **kwargs)
        return wrapper
    return decorator


def owner_or_admin_required(get_resource):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            resource = get_resource(*args, **kwargs)

            if current_user.role == "admin":
                return f(*args, **kwargs)

            if resource.assigned_agent_id != current_user.id:
                abort(403)

            return f(*args, **kwargs)
        return wrapper
    return decorator
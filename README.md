# 🌾 SmartSeason Field Monitoring System

A full-stack web application for tracking crop progress across agricultural fields during a growing season.  
Built as a technical assessment to demonstrate backend logic, role-based access control, and a functional dashboard system.

---

## 🚀 Live Demo
https://<your-render-link>.onrender.com

---

## 🔐 Demo Credentials

### Admin
- Email: admin@test.com  
- Password: 1234  

### Field Agent
- Email: agent@test.com  
- Password: 1234  

---

## 🧰 Tech Stack

### Backend
- Flask (Python)
- SQLAlchemy ORM
- Flask-Login (Authentication)
- PostgreSQL (or SQLite if local dev)

### Frontend
- HTML5
- CSS3 (custom styling)
- Jinja2 templates

### Deployment
- Render (single Flask web service)

---

## 📦 Features

### 👤 Authentication & Roles
- Session-based authentication using Flask-Login
- Two user roles:
  - Admin (Coordinator)
  - Field Agent
- Role-based route protection

---

### 🌾 Field Management
Admins can:
- Create new fields
- Assign fields to agents
- View all fields

Each field contains:
- Name
- Crop type
- Planting date
- Growth stage
- Assigned agent

---

### ✏️ Field Updates
Field Agents can:
- Update field stage (Planted → Growing → Ready → Harvested)
- Add observations/notes
- View only their assigned fields

All updates are tracked in a field history log.

---

### 📊 Field Lifecycle

Each field moves through:

- Planted
- Growing
- Ready
- Harvested

---

### ⚠️ Field Status Logic

Field status is automatically computed using business rules:

```python
def compute_status(self):
    if self.stage == "Harvested":
        return "Completed"

    days = (date.today() - self.planting_date).days

    if days > 14 and self.stage in ["Planted", "Growing"]:
        return "At Risk"

    return "Active"
Status Definitions:
Active → Normal progression
At Risk → No progress for 14+ days in early stages
Completed → Field has been harvested
📋 Field History
Every stage update is logged
Tracks:
Previous stage
New stage
Updated by (agent)
Timestamp
📊 Dashboard
Admin Dashboard:
Total fields
Active fields
At risk fields
Completed fields
Full visibility across all agents
Agent Dashboard:
Only assigned fields
Ability to update stage
View field history
🔐 Security & Access Control
Flask-Login session authentication
Role-based access enforcement
Route protection using decorators:
role_required(role)
owner_or_admin_required()

Prevents:

Agents accessing admin routes
Unauthorized field modifications
Cross-agent field updates
🧠 Design Decisions
Used Jinja templates for simplicity and speed (no frontend framework overhead)
Separated concerns using:
Blueprints (auth, fields)
Models (User, Field, FieldHistory)
Computed business logic (status) instead of storing static values
Lightweight architecture to meet assessment scope without over-engineering
🗄️ Database Design
Users
id
name
email
password
role
Fields
id
name
crop_type
planting_date
stage
status (computed)
assigned_agent_id
FieldHistory
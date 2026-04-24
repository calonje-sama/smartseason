# 🌾 SmartSeason Field Monitoring System

A full-stack web application for tracking crop progress across agricultural fields during a growing season.  
Built as a technical assessment to demonstrate backend logic, role-based access control, and a functional dashboard system.

---

## 🚀 Live Demo
https://smartseason-awca.onrender.com/login

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

## ⚙️ Setup Instructions

---

### 1. 📥 Clone the Repository

```bash
git clone <your-repo-url>
cd smartseason
```

---

### 2. 🐍 Create Virtual Environment

```bash
python -m venv venv
```

Activate it:

**Windows**
```bash
venv\Scripts\activate
```

**Mac/Linux**
```bash
source venv/bin/activate
```

---

### 3. 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. 🔧 Configure Environment Variables

> If using PostgreSQL or environment config:

**Mac/Linux**
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
```

**Windows (PowerShell)**
```powershell
set FLASK_APP=app.py
set FLASK_ENV=development
```

---

### 5. 🗄️ Run Database Migrations / Setup

> If using SQLAlchemy only:

```bash
python app.py
```

The app will automatically:
- Create database tables
- Seed initial admin, agent, and demo field *(if database is empty)*

---

### 6. 🚀 Run the Application

```bash
python app.py
```

Then open (or link given in your terminal for different ports):

👉 `http://127.0.0.1:5000`

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
```
## 📌 Status Definitions

- **Active** → Normal progression  
- **At Risk** → No progress for 14+ days in early stages  
- **Completed** → Field has been harvested  

---

## 📋 Field History

Every stage update is logged and stored for audit and tracking purposes.

### Tracked Data Includes:
- Previous stage  
- New stage  
- Updated by (agent/admin)  
- Timestamp  

---

## 📊 Dashboard Overview

### 🧑‍💼 Admin Dashboard
- Total fields  
- Active fields  
- At-risk fields  
- Completed fields  
- Full visibility across all agents  

### 👨‍🌾 Agent Dashboard
- Only assigned fields  
- Ability to update field stage  
- View field history  

---

## 🔐 Security & Access Control

The system uses secure authentication and role-based access control:

### Features:
- Flask-Login session authentication  
- Role-based access enforcement  
- Route protection via decorators  

### Security Decorators:
- `role_required(role)`  
- `owner_or_admin_required()`  

### Prevents:
- Agents accessing admin routes  
- Unauthorized field modifications  
- Cross-agent field updates  

---

## 🧠 Design Decisions

- Used **Jinja templates** for simplicity and speed (no frontend framework overhead)
- Separated concerns using:
  - Blueprints (`auth`, `fields`)
  - Models (`User`, `Field`, `FieldHistory`)
- Computed business logic (status) instead of storing static values
- Lightweight architecture suitable for assessment scope without over-engineering

---

## 🗄️ Database Design

### Users
- id  
- name  
- email  
- password  
- role  

### Fields
- id  
- name  
- crop_type  
- planting_date  
- stage  
- status *(computed)*  
- assigned_agent_id  

### FieldHistory
- id  
- field_id  
- old_stage  
- new_stage  
- updated_by  
- timestamp  

---

## 🌱 Seed Data

On first run, the system automatically seeds:

- 1 Admin user  
- 1 Field Agent  
- 1 Demo field assigned to the agent  

> This is for testing and demonstration purposes only.

---

## 🚀 Possible Improvements (Future Scope)

- Add charts for analytics (growth trends)  
- Add notifications for "At Risk" fields  
- GPS mapping for fields  
- Multi-agent assignment per field  
- API layer for mobile integration  

---

## 🏁 Summary

This project focuses on:

- Clean role-based architecture  
- Real-world agricultural tracking logic  
- Simple but scalable backend design  
- Usable and intuitive UI
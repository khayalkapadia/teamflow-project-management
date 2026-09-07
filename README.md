# TeamFlow – Project Management & Team Collaboration Platform

TeamFlow is a Django-based project management and team collaboration platform designed to help teams organize projects, assign tasks, track progress, and manage team activities from a centralized dashboard.

The platform provides role-based access for different team members and includes project management, task tracking, team member management, notifications, comments, calendar functionality, and activity tracking.

---

## 🚀 Project Overview

TeamFlow is a full-stack web application developed using Python and Django.

The application allows users to create and manage projects, add team members, create and assign tasks, track task progress, manage deadlines, and collaborate through comments and activity updates.

The system supports different user roles such as Manager, Developer, Designer, and Viewer, with permissions based on the assigned role.

The main goal of TeamFlow is to provide a simple and organized platform for managing software projects and improving team collaboration.

---

## ✨ Features

### 🔐 User Authentication
- User registration
- User login and logout
- Password management
- User profile management
- Authentication-based access control

### 👤 User Roles
TeamFlow supports different project roles:

- Manager
- Developer
- Designer
- Viewer

Each role has different permissions within a project.

### 📁 Project Management
- Create projects
- View project details
- Edit projects
- Manage project members
- Assign roles to team members
- Search and filter projects

### ✅ Task Management
- Create tasks
- Assign tasks to team members
- Edit tasks
- Delete tasks
- Set task priority
- Set task status
- Set due dates
- View detailed task information

### 📊 Dashboard
- Project statistics
- Task statistics
- Task progress
- Project overview
- User-specific information

### 📋 Kanban Task Board
Tasks can be organized based on their status, providing a visual way to track project progress.

### 📅 Calendar
- View project-related tasks and dates
- Organize tasks according to deadlines
- Track upcoming activities

### 🔔 Notifications
Users can receive notifications related to project and task activities.

### 💬 Comments & Collaboration
- Add comments to tasks
- Collaborate with team members
- Track project-related discussions

### 📝 Activity Tracking
The system records important project and task activities to help users track changes and actions.

### 🔎 Search & Filtering
Users can search and filter projects and tasks to quickly find required information.

### 🎨 Responsive Interface
The application provides a clean and responsive web interface using HTML, CSS, JavaScript, and Bootstrap-based components.

---

## 🛠️ Technologies Used

### Backend
- Python
- Django

### Frontend
- HTML5
- CSS3
- JavaScript
- Django Template Language (DTL)
- Bootstrap

### Database
- SQLite

### Tools
- Git
- GitHub
- Visual Studio Code

---

## 📂 Project Structure

```text
teamflow/
│
├── accounts/
│   ├── migrations/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── projects/
│   ├── migrations/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── tasks/
│   ├── migrations/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── teamflow/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── templates/
│   └── base.html
│
├── manage.py
├── README.md
└── .gitignore

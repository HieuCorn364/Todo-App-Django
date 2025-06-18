# Django Todo App

A simple and powerful Todo List application built with Django. Users can create, update and delete their personal tasks. The project is designed for learning purposes, showcasing Django fundamentals with a focus on clean code and best practices.

## Todo Page
<p align="center">
  <img src="https://github.com/HieuCorn364/Todo-App-Django/blob/main/Images/Tasks.png" alt="Todo Page" />
</p>

## Features
- User authentication (Login / Signup / Logout)
- Create, read, update, and delete (CRUD) tasks
- Mark tasks as complete or incomplete
- Track task completion progress
- Send email reminders for tasks that are due in 1 day
- Send OTP verification email when creating a new account
- Responsive UI

## Tech Stack
- **Backend:** Django (Python)
- **Frontend:** HTML, CSS (Bootstrap/Tailwind)
- **Database:** SQLite

## Installation
```bash
git clone https://github.com/yourusername/todo-django.git
cd todo-django
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Main Demo 
####  Verify OTP From Mail
<p align="center">
  <img src="https://github.com/HieuCorn364/Todo-App-Django/blob/main/Images/Mail_OTP.png" alt="Verify OTP" />
</p>

####  Completed Tasks
<p align="center">
  <img src="https://github.com/HieuCorn364/Todo-App-Django/blob/main/Images/Completed_100%25.png" alt="Completed Tasks" />
</p>

####  Email reminders for tasks due in 1 day
<p align="center">
  <img src="https://github.com/HieuCorn364/Todo-App-Django/blob/main/Images/Mail_remider.png" alt="Email Reminder" />
</p>

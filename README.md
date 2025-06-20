# Python Django Banao - User Management System
This project is a web application built with Python and Django as part of the Banao Task 1. It provides a complete user management system with role-based authentication and separate dashboards for different user types.
https://drive.google.com/file/d/1QpHe2Vftk17bCNgvlfOXmxxgVPZueKoG/view?usp=sharing

## Project Description
The application enables user signup and login for two distinct types of users: Patients and Doctors. After a successful login, users are automatically redirected to their respective dashboards, which display the details they provided during signup.

## Features
User Signup: New users can create an account by providing their details.
Role Selection: Users can sign up as either a "Patient" or a "Doctor".
User Login: Registered users can log in securely.
Role-Based Dashboards: Patients are redirected to a patient dashboard, and doctors are redirected to a doctor dashboard.
Profile Information Display: Dashboards display user-specific information, including their name, username, email, address, and profile picture.
Profile Picture Uploads: Users can upload a profile picture during signup.
Form Validation: Includes a check to ensure that the "Password" and "Confirm Password" fields match.
User Logout: A secure logout functionality is provided.

## Technology Stack
Backend: Python, Django
Database: SQLite 3 (Default Django DB)
Image Handling: Pillow

## Setup and Installation
Follow these steps to get the project up and running on your local machine.
1. Clone the Repository
```bash
git clone https://github.com/Saikumar1801/User-Management-System.git
cd User-Management-System
```
2. Create and Activate a Virtual Environment
It's highly recommended to use a virtual environment to manage project dependencies.
```bash
On Windows:
python -m venv venv
.\venv\Scripts\activate
On macOS / Linux:
python3 -m venv venv
source venv/bin/activate
```
4. Install Dependencies
Install Django and Pillow using pip.
```bash
pip install -r requirements.txt
```
(Note: If you don't have a requirements.txt file, you can create one with pip freeze > requirements.txt or install packages directly: pip install django pillow)
5. Apply Database Migrations
Run the following command to create the necessary database tables.
```bash
python manage.py migrate
```
How to Run the Application
Start the Django development server:
```bash
python manage.py runserver
```
Bash
Open your web browser and navigate to the following URLs:
Signup Page: http://127.0.0.1:8000/signup/
Login Page: http://127.0.0.1:8000/login/
Project Structure
```bash
djangobanao_task/
├── mainproject/         # Django project settings and URLs
│   ├── settings.py
│   └── urls.py
├── accounts/            # The main application
│   ├── migrations/
│   ├── templates/
│   │   └── accounts/
│   │       ├── doctor_dashboard.html
│   │       ├── login.html
│   │       ├── patient_dashboard.html
│   │       └── signup.html
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── media/               # For user-uploaded profile pictures
└── manage.py
```

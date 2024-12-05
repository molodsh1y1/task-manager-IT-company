
# Task Manager for IT Company

This is a task manager web application built in using Django. The application allows users to manage projects, tasks, and teams in an IT company. It includes functionality for creating, updating, deleting, and listing projects, as well as managing teams and tasks within those projects. 



## Demo

Live demo: <a href="https://task-manager-it-company.onrender.com/">Task manager it company</a>

Test credentials:
- Username: user
- Password: H.ieTuymVi_9NQw



## Features

- User Authentication: Users can register, log in
- Projects Management: Users can create, update, and delete projects.
- Team Management: Users can manage teams, assign team members
- Task Management: Tasks can be assigned to projects, and their statuses can be updated.
- Search Functionality: Users can search projects, tasks and teams by name
## Installation

Python must be already installed

Clone the repository:
```bash
git clone https://github.com/molodsh1y1/task-manager-IT-company.git
```
Set up a virtual environment:
```bash
python -m venv venv
```
Activate the virtual environment:

Windows:
```bash
venv/Scripts/activate
```
Linux:
```bash
venv/bin/activate (for MacOS and Linux)
```
Install the required dependencies:
```bash
pip install -r requerements.txt
```
Apply the database migrations:
```bash
python manage.py migrate
```
Run the development server:
```bash
python manage.py runserver
```
Visit http://127.0.0.1:8000/ in your browser to view the application.
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

```bash
SECRET_KEY=<your_secret_key>  # Django secret key for the project (keep it secret)
DEBUG=<True_or_False>     # Set to True for development, False for production
POSTGRES_DB=<db_name>    # Name of your PostgreSQL database
POSTGRES_DB_PORT=<db_port>  # Port for the PostgreSQL database (default is 5432)
POSTGRES_USER=<db_user_name>  # PostgreSQL database username
POSTGRES_PASSWORD=<db_password>  # PostgreSQL database password
POSTGRES_HOST=<db_host>  # Host of the PostgreSQL database (e.g., localhost or a remote address)
```
## Tech Stack

- Django
- Python
- PostgreSQL (SQLite locally)
- HTML
- Bootstrap
- Django Crispy Forms
- Git

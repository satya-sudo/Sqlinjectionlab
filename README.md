# SQL Injection Lab **DJANGO**

## Introduction
Sql Injection is a technique to inject malicious SQL code into a web application.
SQL injection usually occurs when you ask a user for input, like their username/userid, and instead of a name/id, the user gives you an SQL statement that you will unknowingly run on your database.

example:
```
query = f"SELECT * FROM users WHERE username = "{ username }";"

username  = input("Enter your username: ")
input  = random" OR 1=1 -- comment

```

## Setup

Python 
```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requrements.txt
$ python manage.py migrate
$ python manage.py runserver
```
Docker
```bash
$  sudo docker build -t sqlinjectionslab .
$  sudo docker run -p 8000:8000 sqlinjectionslab
```

## theme 
This is a project dashboard which is a collection of projects created by different user.
A project can be two types :
    - **public** : anyone can see this project
    - **private** : only the owner can see this project
a user can create a project, and can see all the projects he created.
a user can see and query all **public** projects.
a user can see and query all **private** projects that he created.


## tasks
- 1 : find the sql injection vulnerability in the application
- 2 : use sql injection to get the private project
- 3 : use sql injection to a bump of the whole database
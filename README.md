# Mastermind

This is a Mastermind game for LinkedIn's REACH program. 
The main focus for this app is backend-development. This is a full-stack app with uses
Python and Flask for both the front-end and back-end.


## Run Locally

Clone the project

```bash
  git clone https://github.com/TheHamhams/mastermind.git
```

Go to the project directory

```bash
  cd mastermind
```
To install virtualenv
```
  pip install virtualenv
```

Create and activate virtual environment (virtualenv Windows)

```bash
  virtualenv venv
  source venv/Scripts/activate
```
Create and activate virtual environment (virtualenv Linux)

```bash
  virtualenv venv
  source venv/bin/activate
```
Install requirements
```bash
  pip install -r requirements.txt
```
Next create a .env file in current directory. It should contain the following information.
```bash
  FLASK_APP=mastermind
  SQLALCHEMY_DATABASE_URI=sqlite:///site.db
  SECRET_KEY='secret key goes here'
```
Create database
```bash
  flask db init
  flask db migrate
  flask db upgrade
```
Finally, the app can be ran from the terminal.
```bash
  flask run
```
## Getting Started
#### Go To Sign Up Page
<img src='mastermind/static/images/readme_home.png' width=500>
#### Create an account
<img src='mastermind/static/images/readme_signup.png' width=500>
#### Login
<img src='mastermind/static/images/readme_login.png' width=500>
#### Click Start
<img src='mastermind/static/images/readme_start.png' width=500>
#### Choose a Difficulty
<img src='mastermind/static/images/readme_normal.png' width=500>
#### Play The Game
<img src='mastermind/static/images/readme_play.png' width=500>
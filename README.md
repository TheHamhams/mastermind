# Mastermind

This is a Mastermind game for LinkedIn's REACH program. 
The main focus for this app is backend-development. This is a full-stack app with uses
Python and Flask for both the front-end and back-end.


## Installation

Install Mastermind using pip and your choice of virtual environment. The example 
uses virtualenv on Windows.

```bash
  virtualenv venv
  source venv/Scripts/activate
```
Install the reqirements.
```bash
  pip install requirements.txt
```
Next create a .env file. It should contain the following information.
```bash
  FLASK_APP=mastermind
  SQLALCHEMY_DATABASE_URI=sqlite:///site.db
  SECRET_KEY='secret key goes here'
```
In order to create the database, run the following code in the terminal.
```bash
  flask db init
  flask db migrate
  flask db upgrade
```
Finally, the app can be ran from the terminal.
```bash
  flask run
```
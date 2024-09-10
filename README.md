# UWAttend---3200_27

Repository for CITS3200 group 27

# Setup

Requires python3 and pip
Make sure you are in the uppermost UWAttend directory.
Create a virtual environment:

```
python3 -m venv venv
```

Activate the environment:

- WINDOWS :

```
venv\Scripts\activate
```

- UNIX:

```
source venv/bin/activate
```

Install the requirements via pip:

pip install flask

```
pip install -r requirements.txt
```

Set the secret key:

- WINDOWS (COMMAND PROMPT) :

```
setx SECRET_KEY 'insert_secret_key_here'
```

- UNIX:

```
export SECRET_KEY='secret_string'
```

Note: variable name must be SECRET_KEY, but the value can be any string (a random and long key is best for security).


Create/update database :

```
flask db upgrade
```

Run the flask app :

```
flask run
```

or, to run in debug mode (allowing reload of page to display changed code)

```
flask run --debug
```

It should run on port 5000 by default

Change port with

```
flask run -p port_number
```

# Modifying database schema

If you have modified the database schema and want to update the database:

- Create a migration

```
flask db migrate -m "migration message"
```
Note: The migration script needs to be reviewed and edited, as Alembic is not always able to detect every change you make to your models.

- Apply the changes

```
flask db upgrade
```

To sync the changes in another system, refresh migrations folder (so that the new migration is there), then apply changes:
```
flask db upgrade
```
To revert changes:
```
flask db downgrade
```

# Initialising admin user

Create a .env file in the project root, populated with the required values.

In the root of the directory, run:

```
python -m app.createadmin
```

And the admin account should be added to the database.

# Testing `utilities.py`
Currently the only functionality of `utilities.py` is to read and print out a `csv` file. This will change once database has been configured and frontend is developed.

To test functionality, be on the project root and run:

``` shell
python -m app.utilities
```

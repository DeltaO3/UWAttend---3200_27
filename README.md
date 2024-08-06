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

**_When secret keys/database things are done, add instructions here!_**

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

# UWAttend - Group 27 (CITS3200)

UWAttend is a web-based application written in Flask that is designed to simplify and streamline the process of student sign-ins and sign-outs for university classes. This app helps class facilitators track student participation and manage grading and aims to replace hand-written attendance tracking.

## Manual
For more information on how to use UWAttend, visit the following: [MANUAL.md](manual.md)

## Prerequisites
To run UWAttend on your own machine, you must have the following dependencies installed on your system:

**Python 3.x:** Required to run the application
**Pip:** Python's package installer
**sqlcipher** Required to encrypt and decrypt the database

## Installation
### Clone the Repository
To get started, clone the repository:

``` shell
git clone https://github.com/DeltaO3/UWAttend---3200_27.git UWAttend
cd UWAttend
```

### Setting Up the Environment
1. Create the Python Virtual Environment and activate it:

``` shell
python3 -m venv venv
source /venv/vin/activate
```

2. Install the required dependencies:

``` shell
pip3 install -r requirements.txt
```

#### .env Secret Keys
UWAttend utilises secret keys located in `.env` for security purposes. Create a file called `.env` in the project root directory and set the following:

``` shell
SECRET_KEY="insert_secret_key_here"
DATABASE_PASSWORD="insert_password_here"
```
*Note: replace `"insert_secret_key_here"` and `"insert_password_here"` with your desired values*

`SECRET_KEY` - The key to initalise SQLalchemy
`DATABASE_PASSWORD` - The password that will be used to encrypt `app.db`

### Database Setup
1. Initialise the Database Schema:

``` shell
flask db upgrade
```

2. Populate the Database:

``` shell
python3 -m app.testdb
```

## Running UWAttend
Now that all the dependencies are set up, you can now run the flask app.

To start the web-app, run the following:

``` shell
flask run
```
This will host the application at (http://127.0.0.1:5000)

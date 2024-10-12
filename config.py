# config.py
from dotenv import load_dotenv
import os

basedir = os.path.abspath(os.path.dirname(__file__))

# Load environment variables from the .env file
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')

    # Use SQLCipher with the encryption key specified in the URI
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite+pysqlcipher://:{DATABASE_PASSWORD}@/' + os.path.join(basedir, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

# config.py
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # Use SQLCipher with the encryption key specified in the URI
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite+pysqlcipher://:password@/' + os.path.join(basedir, 'app.db') + \
        '?cipher=aes-256-cfb&kdf_iter=64000'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

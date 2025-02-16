import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'keycat22')
    # Aquí cambias el URI de la base de datos de SQLite a PostgreSQL
    SQLALCHEMY_DATABASE_URI = 'postgresql://franciny:keycat22@localhost/python_flask'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

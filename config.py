DEBUG = True,
SECRET_KEY = 'should always be secret',

#Database settings:
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1@localhost:5432/demo'
SQLALCHEMY_TRACK_MODIFICATIONS = False

WTF_CSRF_ENABLED = False
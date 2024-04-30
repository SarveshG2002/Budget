from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # Import SQLAlchemy

app = Flask(__name__)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3310/budget'
db = SQLAlchemy(app)
app.secret_key = '1234567890987654321'

# Import routes from authRoute.py
from authRoute import *

if __name__ == '__main__':
    app.run()

from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # Import SQLAlchemy
from context_processors import sidebar, username


app = Flask(__name__)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3310/budget'
db = SQLAlchemy(app)
app.secret_key = '1234567890987654321'

app.context_processor(sidebar)
app.context_processor(username)



# Import routes from authRoute.py
from authRoute import *
from paymentRoute import *
from accountsRoute import *
from categoryRoute import *

if __name__ == '__main__':
    app.run()

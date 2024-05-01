from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # Import SQLAlchemy

app = Flask(__name__)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3310/budget'
db = SQLAlchemy(app)
app.secret_key = '1234567890987654321'

@app.context_processor
def inject_common_variables():
    sidebar = [
        {
            'name': 'Home',
            'link': 'dashboard',
            'page': 'dashboard',
            'icon': 'home',
            'indicator': request.endpoint
        },
        {
            'name': 'New Payment',
            'link': 'new_payment',
            'page': 'new_payment',
            'icon': 'shopping_bag',
            'indicator': request.endpoint
        },
        # Add more sidebar items as needed
    ]
    return dict(sidebar=sidebar)

# Import routes from authRoute.py
from authRoute import *

if __name__ == '__main__':
    app.run()

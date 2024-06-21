from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # Import CORS
import socket  # Import socket to fetch local IP address
from context_processors import sidebar, username

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.static_folder = 'static'

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
from toDoApiRputes import *

def get_local_ip():
    """Get the local IP address of the system."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

if __name__ == '__main__':
    app.run(host=get_local_ip(), port=8080)

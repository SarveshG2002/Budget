from flask import Flask

app = Flask(__name__)

# Import routes from routes.py
from authRoute import *

if __name__ == '__main__':
    app.run()

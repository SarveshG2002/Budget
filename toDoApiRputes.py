from flask import render_template, request, redirect, url_for, session
from flask_app import app, db
from models import Account
from decorators import login_required
from datetime import datetime

@app.route('/api/addtodayTask', methods=['GET', 'POST'])
@login_required
def addtodayTask():
    
    



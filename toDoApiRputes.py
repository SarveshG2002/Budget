from flask import render_template, request, redirect, url_for, session,jsonify
from flask_app import app, db
from models import Account,Users,Todaytask
from decorators import login_required
from datetime import datetime,date,time

@app.route('/api/addtodayTask', methods=['POST'])
def addtodayTask():
    data = request.get_json()

    username = data.get('username')
    task_text = data.get('task')

    # Validate the username
    user = Users.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": "Invalid username", "success": False})

    # Get current date, time, and datetime
    today_date = date.today()
    current_time = datetime.now().time()
    current_datetime = datetime.now()

    # Set status to incomplete
    status = 'incomplete'

    # Insert the task into the database
    try:
        new_task = Todaytask(
            task=task_text,
            user_id=user.id,
            username=username,
            status=status,
            created_date=today_date,
            created_time=current_time,
            created_at=current_datetime
        )
        db.session.add(new_task)
        db.session.commit()

        return jsonify({"message": "Task added successfully", "success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e), "success": False})

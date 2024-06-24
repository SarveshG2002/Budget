from flask import render_template, request, redirect, url_for, session,jsonify
from flask_app import app, db
from models import Account,Users,Todaytask,Dailytask
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


@app.route('/api/getTodayTasks', methods=['POST'])
def get_today_tasks():
    try:
        
        data = request.get_json()
        username = data.get('username')

        # Validate the username
        user = Users.query.filter_by(username=username).first()
        if not user:
            return jsonify({"message": "Invalid username", "success": False})

        # Get current date
        today_date = date.today().strftime('%Y-%m-%d')

        # Query the database for tasks with today's date and the given username
        tasks = Todaytask.query.filter_by(created_date=today_date, username=username).order_by(Todaytask.id.desc()).all()

        # Convert tasks to a list of dictionaries
        tasks_list = [task.to_dict() for task in tasks]

        return jsonify({"tasks": tasks_list, "success": True})
    except Exception as e:
        return jsonify({"message": str(e), "success": False})


@app.route('/api/updateTask', methods=['POST'])
def update_task():
    try:
        data = request.get_json()
        task_id = data.get('id')
        new_task = data.get('task')
        # Retrieve the task from the database
        task = Todaytask.query.get(task_id)

        if not task:
            return jsonify({"message": "Task not found", "success": False})

        # Update the task attributes
        task.task = new_task
        task.created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Commit changes to the database
        db.session.commit()

        return jsonify({"message": "Task updated successfully", "success": True})

    except Exception as e:
        return jsonify({"message": str(e), "success": False})
    
@app.route('/api/updateTaskStatus', methods=['POST'])
def update_task_status():
    try:
        data = request.get_json()
        taskId = data.get('taskId')
        newStatus = data.get('newStatus')

        # Validate if the task belongs to the logged-in user
        task = Todaytask.query.filter_by(id=taskId).first()
        if not task:
            return jsonify({"message": "Task not found", "success": False}), 404
        
        # Update task status
        task.status = newStatus
        
        # Commit changes to the database
        db.session.commit()

        return jsonify({"message": "Task status updated successfully", "success": True})

    except Exception as e:
        return jsonify({"message": str(e), "success": False})



@app.route('/api/adddailytask', methods=['POST'])
def add_dailytask():
    data = request.get_json()

    username = data.get('username')
    task_text = data.get('task')

    # Validate the username
    user = Users.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": "Invalid username", "success": False}), 400

    # Get current date, time, and datetime
    today_date = date.today()
    current_time = datetime.now().time()
    current_datetime = datetime.now()

    # Set status to incomplete
    status = 'incomplete'

    # Insert the task into the database
    try:
        new_task = Dailytask(
            dailytask=task_text,
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



@app.route('/api/getdailytasks', methods=['POST'])
def get_all_dailytasks():
    try:
        data = request.get_json()
        username = data.get('username')

        user = Users.query.filter_by(username=username).first()
        if not user:
            return jsonify({"message": "Invalid username", "success": False})
        # Query all tasks from the database
        tasks = Dailytask.query.filter_by(username=username).order_by(Dailytask.id.desc()).all()
        # Convert the tasks to a list of dictionaries
        tasks_list = [task.to_dict() for task in tasks]

        return jsonify({"tasks": tasks_list, "success": True})
    except Exception as e:
        return jsonify({"message": str(e), "success": False})
    

@app.route('/api/updateDailytask', methods=['POST'])
def update_dailytask():
    data = request.get_json()

    task_id = data.get('task_id')
    username = data.get('username')
    updated_task_text = data.get('task')

    # Validate the username
    user = Users.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": "Invalid username", "success": False})

    # Validate the task_id
    task = Dailytask.query.filter_by(id=task_id, user_id=user.id).first()
    if not task:
        return jsonify({"message": "Task not found or you do not have permission to update this task", "success": False})

    # Update the task
    try:
        task.dailytask = updated_task_text
        db.session.commit()
        
        return jsonify({"message": "Task updated successfully", "success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e), "success": False})




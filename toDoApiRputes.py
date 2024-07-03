from flask import render_template, request, redirect, url_for, session,jsonify
from flask_app import app, db
from models import Account,Users,Todaytask,Dailytask,TodaysDailyTask
from decorators import login_required
from datetime import datetime,date,time
from sqlalchemy import func, text

@app.route('/api/addtodayTask', methods=['POST'])
def addtodayTask():
    data = request.get_json()

    username = data.get('username')
    task_text = data.get('task')
    important = data.get('important',0)

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
            important=important,
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



@app.route("/api/getTodayDailyTask", methods=["POST"])
def getTodayDailyTask():
    data = request.get_json()
    username = data.get("username")

    user = Users.query.filter_by(username=username).first()
    if not user:
        return jsonify({"message": "User Not Found", "status": False})

    query = text("""
    SELECT
    dailytask.*,
    COALESCE(task_counts.todays_task_count, 0) AS todays_task_count,
    task_counts.newTask,
    COALESCE(task_counts.status, 'Pending') AS actual_status
FROM
    dailytask
LEFT JOIN (
    SELECT 
        dailytask_id,
        COUNT(id) AS todays_task_count,
        SUBSTRING_INDEX(GROUP_CONCAT(task ORDER BY created_at DESC), ',', 1) AS newTask,
        MAX(status) AS status
    FROM
        todays_daily_task
    WHERE
        created_date = CURDATE()
    GROUP BY
        dailytask_id
) AS task_counts
ON
    dailytask.id = task_counts.dailytask_id
    WHERE dailytask.user_id = :user_id
    """)

    result = db.session.execute(query, {"user_id": user.id})
    
    tasks = []
    for row in result:
        task_dict = {
            'id': row.id,
            'dailytask': row.dailytask,
            'user_id': row.user_id,
            'username': row.username,
            'status': row.status,
            'created_date': row.created_date,
            'created_time': row.created_time,
            'created_at': row.created_at,
            'todays_task_count': row.todays_task_count,
            'newTask': row.newTask,
            'actual_status':row.actual_status
        }
        tasks.append(task_dict)

    return jsonify({"tasks": tasks, "status": True})


@app.route("/api/insertTodayDailyTask", methods=["POST"])
def insertTodayDailyTask():
    data = request.get_json()
    task_id = data.get("id")
    task_text = data.get("task")
    task_status = data.get("status", "Pending")

    # Fetch the original daily task
    daily_task = Dailytask.query.get(task_id)
    if not daily_task:
        return jsonify({"message": "Daily task not found", "status": False})

    # Create new TodaysDailyTask
    now = datetime.now()
    new_task = TodaysDailyTask(
        dailytask_id=str(task_id),
        user_id=daily_task.user_id,
        username=daily_task.username,
        task=task_text,
        status=task_status,
        created_date=now.strftime("%Y-%m-%d"),
        created_time=now.strftime("%H:%M:%S"),
        created_at=now.strftime("%Y-%m-%d %H:%M:%S")
    )

    try:
        db.session.add(new_task)
        db.session.commit()
        return jsonify({"message": "Task inserted successfully", "success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error inserting task: {str(e)}", "success": False})
    

@app.route("/api/updateTodayDailyTask", methods=["POST"])
def updateTodayDailyTask():
    data = request.get_json()
    task_id = data.get("id")
    task_text = data.get("task")
    task_status = data.get("status", "Pending")

    # Find the most recent task for today
    today = datetime.now().strftime("%Y-%m-%d")
    task = TodaysDailyTask.query.filter_by(
        dailytask_id=str(task_id),
        created_date=today
    ).order_by(TodaysDailyTask.created_at.desc()).first()

    if not task:
        return jsonify({"message": "No task found for today", "status": False})
    
    try:
        task.task = task_text
        task.status = task_status
        db.session.commit()
        return jsonify({"message": "Task updated successfully "+task.status, "success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error updating task: {str(e)}", "success": False})
    


@app.route('/api/getCombinedTasksByDate', methods=['POST'])
def get_combined_tasks_by_date():
    try:
        data = request.get_json()
        username = data.get('username')
        
        page = data.get('page', 1)
        limit = data.get('limit', 20)

        # Validate inputs
        if not username:
            return jsonify({"message": "Username is required", "success": False}), 400

        # Validate and parse the date
        

        # Calculate offset
        offset = (page - 1) * limit

        # Construct the SQL query with pagination
        query = text("""
        SELECT * FROM (
            SELECT id, task, user_id, username, status, created_date, created_time, created_at, 
                   important,
                   NULL AS dailytask_id,
                   'todaytask' AS source
            FROM todaytask
            WHERE username = :username

            UNION ALL

            SELECT id, task, user_id, username, status, created_date, created_time, created_at,
                   NULL AS important,
                   dailytask_id,
                   'todays_daily_task' AS source
            FROM todays_daily_task
            WHERE username = :username
        ) AS combined_tasks
        ORDER BY created_at DESC
        LIMIT :limit OFFSET :offset
        """)

        # Execute the query
        result = db.session.execute(query, {
            "username": username,
            "limit": limit,
            "offset": offset
        })

        # Process the results
        tasks = []
        for row in result:
            task = {
                "id": row.id,
                "task": row.task,
                "user_id": row.user_id,
                "username": row.username,
                "status": row.status,
                "created_date": row.created_date,
                "created_time": row.created_time,
                "created_at": row.created_at,
                "important": row.important,
                "dailytask_id": row.dailytask_id,
                "source": row.source
            }
            tasks.append(task)

        # Check if there are more tasks
        has_more = len(tasks) == limit

        return jsonify({
            "tasks": tasks, 
            "has_more": has_more,
            "success": True
        })

    except Exception as e:
        return jsonify({"message": str(e), "success": False})


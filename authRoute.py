from flask import render_template, request, redirect, url_for, session
from flask_app import app,db
from models import Users
from decorators import login_required  # Import the login_required decorator


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Query the User model to find a user with the given username
        user = Users.query.filter_by(username=username).first()
        
        if user and user.password == password:
            # Store user information in session
            session['user_id'] = user.id
            session['username'] = user.username
            # Redirect to dashboard upon successful login
            success = "Login Successfull"
            session['success'] = success
            return redirect(url_for('dashboard'))
        else:
            # error = 'Invalid username or password'
            session['error'] = 'Invalid username or password'
            return redirect(url_for('login'))
    else:
        # Render the login page
        return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    # Retrieve user information from session
    user_id = session.get('user_id')
    
    
    # Placeholder for dashboard logic
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    # Clear user session
    session.clear()
    # Redirect to the login page
    return redirect(url_for('login'))

@app.route('/')
def index():
    # Clear user session
    # session.clear()
    # Redirect to the login page
    return redirect(url_for('login'))

@app.route('/setting', methods=['GET', 'POST'])
@login_required
def setting():
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        
        user_id = session.get('user_id')
        user = Users.query.get(user_id)
        
        if user and user.password== old_password:
            user.password = new_password
            db.session.commit()
            session['success'] = "Password changed successfully."
        else:
            session['error'] = "Old password is incorrect."
        
        return redirect(url_for('setting'))
    
    return render_template('setting.html')

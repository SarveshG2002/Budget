from flask import render_template, request, redirect, url_for, session
from server import app
from models import Users

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
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)
    else:
        # Render the login page
        return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    # Retrieve user information from session
    user_id = session.get('user_id')
    username = session.get('username')
    
    # Placeholder for dashboard logic
    return render_template('dashboard.html', username=username)

@app.route('/logout')
def logout():
    # Clear user session
    session.clear()
    # Redirect to the login page
    return redirect(url_for('login'))

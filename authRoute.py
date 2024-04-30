from flask import render_template, request, redirect, url_for
from server import app
from models import Users

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Query the User model to find a user with the given username
        user = Users.query.filter_by(username=username).first()
        
        if user and user.password == password:
            # Redirect to dashboard upon successful login
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)
    else:
        # Render the login page
        return render_template('login.html')

        # Render the login page
        return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Placeholder for dashboard logic
    return render_template('dashboard.html')

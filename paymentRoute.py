from flask import render_template, request, redirect, url_for, session
from server import app
from models import Users
from decorators import login_required  # Import the login_required decorator


@app.route('/new_payment', methods=['GET', 'POST'])
@login_required
def new_payment():
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


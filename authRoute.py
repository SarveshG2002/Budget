from flask import render_template, request, redirect, url_for
from server import app  # Assuming your Flask app instance is named 'app'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Check username and password (this is just a placeholder, replace it with your authentication logic)
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':
            # Redirect to a different page after successful login (you can change the route as needed)
            return redirect(url_for('dashboard'))
        else:
            # Handle invalid login
            error = 'Invalid username or password'
            return render_template('login.html', error=error)
    else:
        # Render the login page
        return render_template('login.html')

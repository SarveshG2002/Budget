from flask import render_template, request, redirect, url_for, session
from flask_app import app
from models import Users
from decorators import login_required  # Import the login_required decorator


@app.route('/category', methods=['GET', 'POST'])
@login_required
def category():
    if request.method == 'POST':
        return redirect(url_for('login'))
    else:
        # Render the login page
        return render_template('category.html')


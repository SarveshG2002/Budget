from flask import render_template, request, redirect, url_for, session
from server import app
from models import Users
from decorators import login_required  # Import the login_required decorator


@app.route('/new_payment', methods=['GET', 'POST'])
@login_required
def new_payment():
    if request.method == 'POST':
        return redirect(url_for('login'))
    else:
        # Render the login page
        return render_template('new_payment.html')


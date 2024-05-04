from flask import render_template, request, redirect, url_for, session
from flask_app import app
from models import Account
from models import Category
from decorators import login_required  # Import the login_required decorator


@app.route('/new_payment', methods=['GET', 'POST'])
@login_required
def new_payment():
    if request.method == 'POST':
        return redirect(url_for('login'))
    else:
        # Render the login page
        accounts = Account.query.all()
        categories = Category.query.all()
        return render_template('new_payment.html',accounts=accounts,categories=categories)


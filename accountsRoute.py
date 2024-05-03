from flask import render_template, request, redirect, url_for, session
from flask_app import app, db
from models import Account
from decorators import login_required

@app.route('/accounts', methods=['GET', 'POST'])
@login_required
def accounts():
    if request.method == 'POST':
        account_name = request.form.get('account_name')
        opening_balance = request.form.get('opening')
        description = request.form.get('desc')

        # Create a new Account object and add it to the database session
        new_account = Account(acc_name=account_name, opening_balance=opening_balance, description=description, created_at="")
        db.session.add(new_account)
        db.session.commit()

        return redirect(url_for('dashboard'))  # Assuming you have a 'dashboard' route
    else:
        # Render the accounts page
        return render_template('accounts.html')

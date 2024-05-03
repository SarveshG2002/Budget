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

        # Validate account name
        if not account_name:
            # If account name is empty, set error message in session
            session['error'] = "Account name is required"
            return redirect(url_for('accounts'))

        try:
            # Create a new Account object and add it to the database session
            new_account = Account(acc_name=account_name, opening_balance=opening_balance, description=description, created_at="hello")
            db.session.add(new_account)
            db.session.commit()
            session['success'] = "Account created successfully"
        except SQLAlchemyError as e:
            # If an error occurs during database operation, set error message in session
            session['error'] = "Failed to create account. Please try again."
            # app.logger.error("Failed to create account: %s", str(e))
        finally:
            return redirect(url_for('accounts'))

    else:
        # Render the accounts page
        return render_template('accounts.html')

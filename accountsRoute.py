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
        accounts = Account.query.all()
        # Render the accounts page
        # print(accounts)
        return render_template('accounts.html', accounts=accounts)
    

@app.route('/delete_account/<int:account_id>', methods=['GET'])
@login_required
def delete_account(account_id):
    # Retrieve the account from the database
    account = Account.query.get(account_id)
    if account:
        # Delete the account
        db.session.delete(account)
        db.session.commit()
        session['success'] = 'Account deleted successfully'
    else:
        session['error'] = 'Account not found'
    return redirect(url_for('accounts'))


@app.route('/edit_account/<int:account_id>', methods=['GET', 'POST'])
@login_required
def edit_account(account_id):
    account = Account.query.get(account_id)
    if not account:
        session['error'] = 'Account not found'
        return redirect(url_for('accounts'))
    
    if request.method == 'POST':
        # Update account details based on form submission
        account.acc_name = request.form.get('account_name')
        account.opening_balance = request.form.get('opening')
        account.description = request.form.get('desc')
        db.session.commit()
        # flash('Account updated successfully', 'success')
        session['success'] = 'Account updated successfully'
        return redirect(url_for('accounts'))
    
    # Render the edit account page with the account data
    return render_template('edit-account.html', account=account)

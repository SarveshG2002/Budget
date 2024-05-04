from flask import render_template, request, redirect, url_for, session
from flask_app import app, db
from decorators import login_required
from models import Account, Category, Payment
from datetime import datetime

@app.route('/new_payment', methods=['GET', 'POST'])
@login_required
def new_payment():
    if request.method == 'POST':
        pdate = request.form.get('pdate')
        account_id = request.form.get('account')
        amount = request.form.get('amount')
        category_id = request.form.get('category')
        to = request.form.get('to')
        note = request.form.get('note')

        if not all([pdate, account_id, amount, category_id]):
            session['error'] = "Please fill in all required fields"
            return redirect(url_for('new_payment'))
        
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

        # Create a new Payment object and add it to the database session
        new_payment = Payment(date=pdate, account=account_id, amount=amount, category=category_id, to=to, note=note,created_at=formatted_datetime)
        db.session.add(new_payment)
        db.session.commit()

        # Redirect to a success page or wherever needed
        session['success'] = "Payment Added Successfully"
        return redirect(url_for('new_payment'))

    else:
        # Render the form with account and category options
        accounts = Account.query.all()
        categories = Category.query.all()
        return render_template('new_payment.html', accounts=accounts, categories=categories)

from flask import render_template, request, redirect, url_for, session
from flask_app import app, db
from decorators import login_required
from models import Account, Category, Payment
from datetime import datetime
import pprint
from sqlalchemy import func
from sqlalchemy.sql import text

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
        new_payment = Payment(user_id=session['user_id'],date=pdate,transaction_type="expense",account=account_id, amount=amount, category=category_id, to=to, note=note,created_at=formatted_datetime)
        db.session.add(new_payment)
        db.session.commit()

        # Redirect to a success page or wherever needed
        session['success'] = "Payment Added Successfully"
        return redirect(url_for('new_payment'))

    else:
        # Render the form with account and category options
        accounts = Account.query.filter_by(user_id=session['user_id']).all()
        categories = Category.query.filter_by(user_id=session['user_id']).all()
        return render_template('new_payment.html', accounts=accounts, categories=categories)


@app.route('/payment_list', methods=['GET'])
@login_required
def payment_list():
    # Get filter values from request arguments
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')
    account_id = request.args.get('account')
    category_id = request.args.get('category')

    # Build the base query
    query = db.session.query(Payment, Account.acc_name, Category.name.label('category_name')) \
                    .outerjoin(Account, Payment.account == Account.id) \
                    .outerjoin(Category, Payment.category == Category.id) \
                    .order_by(Payment.id.desc())

    query = query.filter(Payment.user_id==session['user_id'])
    query = query.filter(Payment.transaction_type=="expense")
    # Apply filters
    if from_date and to_date:
        query = query.filter(Payment.date.between(from_date, to_date))
    if account_id:
        query = query.filter(Payment.account == account_id)
    if category_id:
        query = query.filter(Payment.category == category_id)
    # query = query.filter(Payment.category == category_id)
    # Execute the query
    payments = query.all()
    accounts = Account.query.filter_by(user_id=session['user_id']).all()
    categories = Category.query.filter_by(user_id=session['user_id']).all()

    # Print the last executed query
    # print(query.statement)

    return render_template('payment_list.html', payments=payments,accounts=accounts,categories=categories)


@app.route('/delete_payment/<int:payment_id>', methods=['GET'])
@login_required
def delete_payment(payment_id):
    payment = Payment.query.get(payment_id)
    if payment:
        db.session.delete(payment)
        db.session.commit()
        session['success'] = 'Payment deleted successfully'
    else:
        session['error'] = 'Payment not found'
    return redirect(url_for('payment_list'))


# @app.route('/edit_payment/<int:payment_id>', methods=['GET'])
# @login_required
# def edit_payment(payment_id):
#     payment = Payment.query.get(payment_id)
#     accounts = Account.query.all()
#     categories = Category.query.all()

#     return render_template('edit_payment.html', payment=payment,accounts=accounts,categories=categories)


@app.route('/edit_payment/<int:payment_id>', methods=['GET', 'POST'])
@login_required
def edit_payment(payment_id):
    payment = Payment.query.get(payment_id)
    accounts = Account.query.filter_by(user_id=session['user_id']).all()
    categories = Category.query.filter_by(user_id=session['user_id']).all()

    if request.method == 'POST':
        # Get the updated data from the form
        pdate = request.form.get('pdate')
        account_id = request.form.get('account')
        amount = request.form.get('amount')
        category_id = request.form.get('category')
        to = request.form.get('to')
        note = request.form.get('note')

        # Update the payment object with the new data
        payment.date = pdate
        payment.account = account_id
        payment.amount = amount
        payment.category = category_id
        payment.to = to
        payment.note = note

        # Commit the changes to the database
        db.session.commit()

        # Redirect to a success page or somewhere else
        session['success'] = 'Payment updated successfully'
        return redirect(url_for('edit_payment', payment_id=payment_id))

    # Render the template with the payment details
    def to_int(value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return 0

    payment.category = to_int(payment.category)
    payment.account = to_int(payment.account)
    return render_template('edit_payment.html', payment=payment, accounts=accounts, categories=categories)



@app.route('/income', methods=['GET', 'POST'])
@login_required
def income():
    if request.method == 'POST':
        date = request.form.get('date')
        account_id = request.form.get('account')
        amount = request.form.get('amount')
        # category_id = request.form.get('category')
        # to = request.form.get('to')
        note = request.form.get('note')

        if not all([date,amount]):
            session['error'] = "Please fill in all required fields"
            return redirect(url_for('income'))

        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

        # # Create a new Payment object and add it to the database session
        new_payment = Payment(user_id=session['user_id'],date=date,transaction_type="income", account=account_id, amount=amount, note=note,created_at=formatted_datetime)
        db.session.add(new_payment)
        db.session.commit()

        print("First Call")
        # # Redirect to a success page or wherever needed
        session['success'] = "Income Added Successfully"
        return redirect(url_for('income'))

    else:

        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        account_id = request.args.get('account')

        query = db.session.query(Payment, Account.acc_name) \
                    .outerjoin(Account, Payment.account == Account.id) \
                    .order_by(Payment.id.desc())


        query = query.filter(Payment.user_id==session['user_id'])
        query = query.filter(Payment.transaction_type=="income")
        # Apply filters
        if from_date and to_date:
            query = query.filter(Payment.date.between(from_date, to_date))
        if account_id:
            query = query.filter(Payment.account == account_id)

        # Execute the query
        incomes = query.all()
        

        # Render the form with account and category options
        # accounts = Account.query.all()
        # categories = Category.query.all()
        accounts = Account.query.filter_by(user_id=session['user_id']).all()
        return render_template('income.html',accounts=accounts,incomes=incomes)
    

@app.route('/edit_income/<int:payment_id>', methods=['GET', 'POST'])
@login_required
def edit_income(payment_id):
    payment = Payment.query.get(payment_id)
    accounts = Account.query.filter_by(user_id=session['user_id']).all()
    # categories = Category.query.all()
    if request.method == 'POST':
        date = request.form.get('date')
        account_id = request.form.get('account')
        amount = request.form.get('amount')
        # category_id = request.form.get('category')
        # to = request.form.get('to')
        note = request.form.get('note')

        if not all([date,amount]):
            session['error'] = "Please fill in all required fields"
            return redirect(url_for('income'))

        payment.date = date
        payment.account = account_id
        payment.amount = amount
        # payment.category = category_id
        # payment.to = to
        payment.note = note
        db.session.commit()
        session['success'] = 'Income updated successfully'
        return redirect(url_for('edit_income', payment_id=payment_id))
        

    # else:
    def to_int(value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return 0
    payment.account = to_int(payment.account)
    accounts = Account.query.filter_by(user_id=session['user_id']).all()
    return render_template('edit_income.html',accounts=accounts,payment=payment)


@app.route('/cashbook', methods=['GET', 'POST'])
@login_required
def cashbook():

    account_id = request.args.get('account')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')

    income_query = db.session.query(func.sum(Payment.amount)) \
                             .filter(Payment.user_id == session['user_id']) \
                             .filter(Payment.transaction_type == "income")
    if account_id:
        income_query = income_query.filter(Payment.account == account_id)
    if from_date and to_date:
            income_query = income_query.filter(Payment.date.between(from_date, to_date))
    income_sum = income_query.scalar()

    expense_query = db.session.query(func.sum(Payment.amount)) \
                              .filter(Payment.user_id == session['user_id']) \
                              .filter(Payment.transaction_type == "expense")
    if account_id:
        expense_query = expense_query.filter(Payment.account == account_id)
    if from_date and to_date:
            expense_query = expense_query.filter(Payment.date.between(from_date, to_date))
    expense_sum = expense_query.scalar()

    query = db.session.query(Payment, Account.acc_name, Category.name) \
                .outerjoin(Account, Payment.account == Account.id) \
                .outerjoin(Category, Payment.category == Category.id) \
                .order_by(Payment.id.desc())


    query = query.filter(Payment.user_id==session['user_id'])
    if from_date and to_date:
            query = query.filter(Payment.date.between(from_date, to_date))
    if account_id:
            query = query.filter(Payment.account == account_id)
    incomes = query.all()
    # compiled_query = str(query.statement.compile(db.engine, compile_kwargs={"literal_binds": True}))
    # print(compiled_query)
    # pprint.pprint(incomes)
    # print(income_sum)
    accounts = Account.query.filter_by(user_id=session['user_id']).all()
    
    if income_sum is None:
        income_sum=0
    if expense_sum is None:
        expense_sum=0

    # print(incomes)
    tot=income_sum-expense_sum
    return render_template('cashbook.html',incomes=incomes,tot=tot,accounts=accounts)



@app.route('/transfer', methods=['GET', 'POST'])
@login_required
def transfer():
    accounts = Account.query.filter_by(user_id=session['user_id']).all()
    return render_template('transferToAnotherBank.html',accounts=accounts)

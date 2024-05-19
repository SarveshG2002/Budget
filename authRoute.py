from flask import render_template, request, redirect, url_for, session
from flask_app import app,db
from models import Users,Account, Category, Payment
from decorators import login_required  # Import the login_required decorator
from sqlalchemy import func
from datetime import date,datetime,timedelta
import random



@app.route('/login', methods=['GET', 'POST'])
def login():
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

@app.route('/dashboard')
@login_required
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    # Retrieve user information from session
    expense_sum = db.session.query(func.sum(Payment.amount)) \
                           .filter(Payment.user_id == session['user_id']) \
                           .filter(Payment.transaction_type == "expense") \
                           .scalar()
    
    income_sum = db.session.query(func.sum(Payment.amount)) \
                           .filter(Payment.user_id == session['user_id']) \
                           .filter(Payment.transaction_type == "income") \
                           .scalar()
    
    today = date.today()

    # Calculate today's expenses
    today_exp = db.session.query(func.sum(Payment.amount)) \
                          .filter(Payment.user_id == session['user_id']) \
                          .filter(Payment.transaction_type == "expense") \
                          .filter(func.date(Payment.date) == today) \
                          .scalar()
    
    start_of_month = today.replace(day=1)
    next_month = today.replace(day=28) + timedelta(days=4)  # this will never fail
    start_of_next_month = next_month.replace(day=1)
    end_of_month = start_of_next_month - timedelta(days=1)

    # Calculate total income for the current month
    month_income_sum = db.session.query(func.sum(Payment.amount)) \
                                 .filter(Payment.user_id == session['user_id']) \
                                 .filter(Payment.transaction_type == "income") \
                                 .filter(Payment.date >= start_of_month) \
                                 .filter(Payment.date <= end_of_month) \
                                 .scalar()
    
    month_expense_sum = db.session.query(func.sum(Payment.amount)) \
                                 .filter(Payment.user_id == session['user_id']) \
                                 .filter(Payment.transaction_type == "Expense") \
                                 .filter(Payment.date >= start_of_month) \
                                 .filter(Payment.date <= end_of_month) \
                                 .scalar()

    # Handle None case for month_income_sum
    if month_income_sum is None:
        month_income_sum = 0
    
    if month_expense_sum is None:
        month_expense_sum = 0
    
    if today_exp is None:
        today_exp = 0

    # Handle None case for expense_sum
    if expense_sum is None:
        expense_sum = 0

    if income_sum is None:
        income_sum = 0
    
    if month_income_sum is None:
        month_income_sum=0

    def generate_color():
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return f'rgb({r}, {g}, {b})'

    accounts = Account.query.filter_by(user_id=session['user_id']).all()
    # ccounts = ['Account 1', 'Account 2', 'Account 3']
    colors = [generate_color() for _ in accounts]
    
    
    # Placeholder for dashboard logic
    return render_template('dashboard.html',accounts=zip(accounts, colors),total_exp=expense_sum,today_exp=today_exp,total_inc=income_sum,month_income_sum=month_income_sum,month_expense_sum=month_expense_sum)

@app.route('/logout')
def logout():
    # Clear user session
    session.clear()
    # Redirect to the login page
    return redirect(url_for('login'))

@app.route('/')
def index():
    # Clear user session
    # session.clear()
    # Redirect to the login page
    return redirect(url_for('login'))

@app.route('/setting', methods=['GET', 'POST'])
@login_required
def setting():
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        
        user_id = session.get('user_id')
        user = Users.query.get(user_id)
        
        if user and user.password== old_password:
            user.password = new_password
            db.session.commit()
            session['success'] = "Password changed successfully."
        else:
            session['error'] = "Old password is incorrect."
        
        return redirect(url_for('setting'))
    
    return render_template('setting.html')


@app.route('/backup', methods=['GET', 'POST'])
@login_required
def backup():
    return render_template('backup.html')

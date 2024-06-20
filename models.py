from flask_app import db  # Assuming `db` is the SQLAlchemy instance

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User id={self.id}, username={self.username}, user_id={self.user_id}>'

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255))
    acc_name = db.Column(db.String(100), nullable=False)
    opening_balance = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Account id={self.id}, acc_name={self.acc_name}, user_id={self.user_id}>"
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255))
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Category id={self.id}, name={self.name}, user_id={self.user_id}>"


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255))
    transaction_type = db.Column(db.String(255))
    amount = db.Column(db.String(255))
    note = db.Column(db.String(255))
    to = db.Column(db.String(255))
    category = db.Column(db.String(255))
    account = db.Column(db.String(255))
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<Payment id={self.id}, user_id={self.user_id}, amount={self.amount}, date={self.date}, note={self.note}, account={self.account}, transaction_type={self.transaction_type}, created_at={self.created_at}>"

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(255))
    amount = db.Column(db.String(255), nullable=False)
    date = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.String(255))
    
    def __repr__(self):
        return f"Income id={self.id}, amount={self.amount}, date={self.date}, created_at={self.created_at}, user_id={self.user_id})"

class TodayTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    created_date = db.Column(db.Date, nullable=False)
    created_time = db.Column(db.Time, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    user = db.relationship('Users', backref=db.backref('tasks', lazy=True))

    def __repr__(self):
        return f"<TodayTask id={self.id}, task={self.task}, user_id={self.user_id}, status={self.status}, created_date={self.created_date}, created_time={self.created_time}, created_at={self.created_at}>"

    def to_dict(self):
        return {
            'id': self.id,
            'task': self.task,
            'user_id': self.user_id,
            'status': self.status,
            'created_date': self.created_date.strftime('%Y-%m-%d'),
            'created_time': self.created_time.strftime('%H:%M:%S'),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }



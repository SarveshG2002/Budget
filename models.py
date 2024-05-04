from flask_app import db  # Assuming `db` is the SQLAlchemy instance

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    acc_name = db.Column(db.String(100), nullable=False)
    opening_balance = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Account id={self.id}, acc_name={self.acc_name}>"
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Category id={self.id}, name={self.name}>"


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.String(255))
    note = db.Column(db.String(255))
    to = db.Column(db.String(255))
    category = db.Column(db.String(255))
    account = db.Column(db.String(255))
    date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

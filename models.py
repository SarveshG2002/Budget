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

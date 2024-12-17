from app.extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(300), primary_key=True, unique=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    mobile_number = db.Column(db.String(15), unique=True)
    password_hash = db.Column(db.String(255), nullable=False)

class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    created_by = db.Column(db.String(90), db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    creator = db.relationship('User', backref='created_groups')
    members = db.relationship('GroupMember', back_populates='group', cascade="all, delete-orphan")


class GroupMember(db.Model):
    __tablename__ = 'group_members'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    user_id = db.Column(db.String(90), db.ForeignKey('users.id'), nullable=False)
    group = db.relationship('Group', back_populates='members')
    user = db.relationship('User', backref='group_memberships')


class Expense(db.Model):
    __tablename__ = 'expenses'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), nullable=False)
    user_id = db.Column(db.String(100), db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(256), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    creator = db.relationship('User', backref='expenses_created')
    group = db.relationship('Group', backref='expenses')
    splits = db.relationship('ExpenseSplit', back_populates='expense', cascade="all, delete-orphan")


class ExpenseSplit(db.Model):
    __tablename__ = 'expense_splits'
    id = db.Column(db.Integer, primary_key=True)
    expense_id = db.Column(db.Integer, db.ForeignKey('expenses.id'), nullable=False)
    user_id = db.Column(db.String(), db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)

    expense = db.relationship('Expense', back_populates='splits')
    user = db.relationship('User', backref='expense_splits')


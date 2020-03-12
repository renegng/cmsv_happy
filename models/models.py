from datetime import datetime
from flask import jsonify
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# **************************************************************************
# Database models
# **************************************************************************

# User Information Class
class UserInfo(db.Model):
    __tablename__ = 'user_info'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(300), unique=False, nullable=False)
    phonenumber = db.Column(db.String(20), unique=False, nullable=True)
    cmsvuser = db.Column(db.String(15), unique=False, nullable=False)
    notifications = db.Column(db.Boolean, unique=False, nullable=True)
    enabled = db.Column(db.Boolean, unique=False, nullable=True, default=True)
    datecreated = db.Column(db.DateTime, unique=False, nullable=False, index=True, default=datetime.utcnow)
    roles = db.relationship('UserXRole', secondary='user_x_role', lazy='subquery', back_populates='user_info')

    def __repr__(self):
        return jsonify(
            id = self.id,
            email = self.email,
            name = self.name,
            phonenumber = self.phonenumber,
            cmsvuser = self.cmsvuser,
            notifications = self.notifications,
            enabled = self.enabled,
            roles = self.roles
        )


# Role Class
class UserRole(db.Model):
    __tablename__ = 'user_role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    enable = db.Column(db.Boolean, unique=False, nullable=True, default=True)
    users = db.relationship('UserXRole', secondary='user_x_role', lazy='subquery', back_populates='user_role')

    def __repr__(self):
        return jsonify(
            id = self.id,
            name = self.name,
            enabled = self.enable,
            users = self.users
        )


# User Roles Class
class UserXRole(db.Model):
    __tablename__ = 'user_x_role'
    user_id = db.Column(db.Integer, db.ForeignKey('user_info.id'), primary_key=True)
    user_role_id = db.Column(db.Integer, db.ForeignKey('user_role.id'), primary_key=True)
    datecreated = db.Column(db.DateTime, unique=False, nullable=False, index=True, default=datetime.utcnow)
    user_info = db.relationship('UserInfo', back_populates='roles')
    user_role = db.relationship('UserRole', back_populates='users')

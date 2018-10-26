import os

from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import INET
from flask_security import (
    Security, SQLAlchemyUserDatastore,
    UserMixin, RoleMixin, auth_required
)
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['WTF_CSRF_ENABLED'] = False
app.config['SECURITY_PASSWORD_HASH'] = 'sha512_crypt'

# redefine hashing_schemes, 'hex_md5' is checked.
app.config['SECURITY_HASHING_SCHEMES'] = ['md5_crypt', 'hex_md5']


app.config['SECURITY_PASSWORD_SALT'] = os.environ.get('SALT')

db = SQLAlchemy(app)

# Define models
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    # User tracking by flask-security
    last_login_at = db.Column(db.DateTime(timezone=False))
    current_login_at = db.Column(db.DateTime(timezone=False))
    last_login_ip = db.Column(INET)
    current_login_ip = db.Column(INET)
    login_count = db.Column(db.Integer())


db.drop_all()
db.create_all()

user_datastore = SQLAlchemyUserDatastore(db, User, Role)

# Setup Flask-Security
security = Security(app, user_datastore)

admin_role = Role(**{'name': 'admin', 'description': 'Admin role'})
db.session.add(admin_role)
db.session.commit()


user_datastore.create_user(email='test@example.com', password='test', active=True, roles=[Role.query.first()])
db.session.commit()


@app.route('/hello')
@auth_required('token')
def hello():
    return jsonify({'hello': 'world'})


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

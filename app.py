import os

from flask import Flask, render_template, jsonify
from flask_security import (
    Security, SQLAlchemySessionUserDatastore,
    UserMixin, RoleMixin, auth_required
)
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_ENABLED'] = False
app.config['SECURITY_PASSWORD_HASH'] = 'sha512_crypt'

# redefine hashing_schemes, 'hex_md5' is checked.
app.config['SECURITY_HASHING_SCHEMES'] = ['argon2', 'sha256_crypt', 'hex_md5']
app.config['SECURITY_DEPRECATED_HASHING_SCHEMES'] = ['hex_md5']

app.config['SECURITY_PASSWORD_SALT'] = os.environ.get('SALT')

# SqlAlchemy
engine = create_engine(os.environ.get('SQLALCHEMY_DATABASE_URI'))
session = scoped_session(sessionmaker(autoflush=False, bind=engine))
Base = declarative_base()
Base.query = session.query_property()


# Define models
class RolesUsers(Base):
    __tablename__ = 'roles_users'
    id = Column(Integer(), primary_key=True)
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    role_id = Column('role_id', Integer(), ForeignKey('role.id'))


class Role(Base, RoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))


class User(Base, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255))
    password = Column(String(255))
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    login_count = Column(Integer)
    active = Column(Boolean())
    confirmed_at = Column(DateTime())
    last_login_ip = Column(INET)
    current_login_ip = Column(INET)
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
# end

# Setup Flask-Security
user_session_store = SQLAlchemySessionUserDatastore(session, User, Role)
security = Security(app, user_session_store)

# Add role
admin_role = Role(**{'name': 'admin', 'description': 'Admin role'})
session.add(admin_role)
session.commit()

# Create user
user_session_store.create_user(email='test@example.com',
                               password='test', active=True, roles=[Role.query.first()])
session.commit()


@app.route('/hello')
@auth_required('token')
def hello():
    return jsonify({'hello': 'world'})


@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

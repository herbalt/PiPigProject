from random import SystemRandom
from hmac import compare_digest
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from backports.pbkdf2 import pbkdf2_hmac, compare_digest
from pipig.app_config import config_class as config

from pipig.data import db, CRUDMixin


class UserAccountStatus(db.Model, CRUDMixin):
    __tablename__ = 'user_account_status'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    code = db.Column(db.String(20))

    def __init__(self, code):
        self.code = code

    NOT_REGISTERED = 1
    REGISTERED = 2
    CONFIRMED = 3
    GUEST = 4


class UserProfile(db.Model, CRUDMixin):
    __tablename__ = 'user_profile'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(120), nullable=True)
    last_name = db.Column(db.String(120), nullable=True)
    account_id = db.Column(db.Integer, db.ForeignKey('user_account.id'))

    def __init__(self, account_id, first_name=None, last_name=None):
        self.account_id = account_id
        self.first_name = first_name
        self.last_name = last_name


class UserAccount(UserMixin, CRUDMixin, db.Model):
    __tablename__ = 'user_account'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(64), index=True, nullable=False, unique=True)
    email = db.Column(db.String(120), index=True, nullable=False, unique=True)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    _password = db.Column(db.LargeBinary(120), nullable=False)
    _salt = db.Column(db.String(120))
    _password_hash_algorithm = db.Column(db.String(50), default='sha512', nullable=False)

    registration_datetime = db.Column(db.DateTime, nullable=True)
    account_status_id = db.Column(db.Integer, db.ForeignKey('user_account_status.id'))
    status_updated_datetime = db.Column(db.DateTime, default=None)
    _password_reminder_expire = db.Column(db.DateTime, default=None)

    _email_confirmation_token = db.Column(db.String(100), nullable=True)
    _password_reminder_token = db.Column(db.String(120), nullable=True)

    _accept_terms_of_service = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return 'Username: ' + self.name

    def __init__(self, name, email, password, admin=False, status=UserAccountStatus.NOT_REGISTERED, status_time=None,
                 terms_service=False):
        self.name = name
        self.email = email
        self.password = password
        self.admin = admin
        self.account_status_id = status
        self.status_updated_datetime = status_time
        self._accept_terms_of_service = terms_service


    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        if self._salt is None:
            self._salt = bytes(SystemRandom().getrandbits(128))
        self._password = self._hash_password(value)

    def is_valid_password(self, password):
        new_hash = self._hash_password(password)
        return compare_digest(new_hash, self._password)

    def _hash_password(self, password):
        pwd = password.encode("utf-8")
        salt = bytes(self._salt)

        if self._password_hash_algorithm is None:
            self._password_hash_algorithm = "sha512"
        try:
            buff = pbkdf2_hmac(self._password_hash_algorithm, pwd, salt, iterations=config.HASH_ROUNDS)
        except:
            buff = pbkdf2_hmac("sha512", pwd, salt, iterations=config.HASH_ROUNDS)

        return bytes(buff)


class UserOAuth(db.Model, CRUDMixin):
    __tablename__ = 'user_oauth'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_account.id'))



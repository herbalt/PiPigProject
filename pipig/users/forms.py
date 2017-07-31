from flask_wtf import Form
from wtforms import fields
from wtforms.validators import Email, InputRequired, ValidationError
from .models import UserAccount
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from pipig.data import db


class LoginForm(Form):
    email = fields.StringField(validators=[InputRequired(), Email()])
    password = fields.PasswordField(validators=[InputRequired()])
    remember_me = fields.BooleanField(label='Remember Me')

    @staticmethod
    def populate(email='', password=''):
        obj = LoginForm()
        obj.email = email
        obj.password = password
        return obj

    def validate_password(form, field):
        try:
            user = UserAccount.query.filter(UserAccount.email == field.data).one()
        except (MultipleResultsFound, NoResultFound):
            raise ValidationError("Please register")
        if user is None:
            raise ValidationError("Please register")
        if not user.is_valid_password(field.data):
            raise ValidationError("Invalid password")

        form.user = user


class UpdateProfileForm(Form):
    name = fields.StringField('User name', validators=[InputRequired()])
    first_name = fields.StringField('First name')
    last_name = fields.StringField('Last name')

    @staticmethod
    def populate(name='', first_name='', last_name=''):
        obj = UpdateProfileForm()
        obj.name = name
        obj.first_name = first_name
        obj.last_name = last_name
        return obj


class RegistrationForm(Form):
    name = fields.StringField("User name", validators=[InputRequired()])
    first_name = fields.StringField("First name")
    last_name = fields.StringField("Last name")
    email = fields.StringField(validators=[InputRequired(), Email()])
    password = fields.PasswordField("Password", validators=[InputRequired()])

    @staticmethod
    def populate(name='', email='', password=''):
        obj = RegistrationForm()
        obj.name = name
        obj.email = email
        obj.password = password
        return obj

    def validate_email(form, field):
        # user = db.session.query(UserAccount).filter_by(UserAccount.email == form.email.data).first()

        user_account = UserAccount.query.filter_by(email=form.email).first()

        # user_account = UserAccount.query.filter_by(email=field.data).first()
        if user_account is not None:
            raise ValidationError("A user with that email already exists")
        return True

    def validate_user_name(form, field):
        # user = db.session.query(UserAccount).filter_by(form.name.data).first()
        user = UserAccount.query.filter_by(name=form.name).first()

        if user is not None:
            raise ValidationError("A user with that user name already exists")
        return True
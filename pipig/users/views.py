from datetime import datetime
from flask_login import current_user, login_user, login_required, logout_user

from pipig.mail import send_email
from .OAuth import OAuthSignIn, FacebookSignIn
from flask import Blueprint, redirect, url_for, flash, render_template, request

from .forms import LoginForm, RegistrationForm, UpdateProfileForm
from .token import generate_confirmation_token, confirm_token
from models import UserAccount, UserOAuth, UserProfile, UserAccountStatus
from pipig.data import db
from models import UserAccountStatus

from data_setup import data_setup

users = Blueprint('users', __name__)

index_url = 'users.user_index'


@users.route('/index')
@login_required
def user_index():
    return render_template('index.html', user=current_user)


@users.route('/login/', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_email = form.email
        user_account = UserAccount.query.filter_by(email=user_email).first_or_404()
        print str(user_account)
        login_user(user_account)
        flash("Logged in successfully.")
        return redirect(request.args.get("next") or url_for(index_url))
    return render_template('users/login.html', form=form)


@users.route('/register/', methods=('GET', 'POST'))
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print str(form.data)
        user_account = UserAccount(name=form.name.data,
                                   email=form.email.data,
                                   password=form.password.data,
                                   status=UserAccountStatus.REGISTERED,
                                   status_time=datetime.now())



        db.session.add(user_account)
        db.session.commit()

        user_id = UserAccount.query.filter_by(email=user_account.email).first_or_404()
        user_profile = UserProfile(account_id=user_id, first_name=form.first_name.data,
                                   last_name=form.last_name.data)

        db.session.add(user_profile)
        db.session.commit()

        login_user(user_account)

        token = generate_confirmation_token(user_account.email)
        confirm_url = url_for('users.confirm_email', token=token, _external=True)
        html = render_template('users/confirmation_email.html', confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(user_account.email, subject, html)
        return redirect(url_for(index_url))
    return render_template('users/register.html', form=form)


@users.route('/unconfirm/')
def unconfirmed():
    return render_template('users/unconfirmed.html')

@users.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        email = None
        flash('The confirmation link is invalid or has expired.', 'danger')
        return render_template('users/unconfirmed.html')
    user_account = UserAccount.query.filter_by(email=email).first_or_404()
    if user_account.status:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user_account.account_status_id = UserAccountStatus.CONFIRMED
        user_account.status_status_updated_datetime = datetime.now()
        db.session.add(user_account)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for(index_url))

@users.route('/profile/<int:user_id>')
def update_profile(user_id):
    user_account = UserAccount.query.filter_by(id=user_id).first()
    user_profile = UserProfile.query.filter_by(id=user_id).first()

    form = UpdateProfileForm()

    form.name.data = user_account.name
    form.first_name.data = user_profile.first_name
    form.last_name.data = user_profile.last_name

    if form.validate_on_submit():
        return redirect(url_for(index_url))
    return redirect(url_for('users.update_profile.%s' % user_id))

@users.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for(index_url))


@users.route('/authorize/<provider>')
def oauth_authorize(provider):
    """
        Sends a request to a provider for OAuth authentication
        :param provider:
        :return:
        """

    if not current_user.is_anonymous:
        return redirect(url_for(index_url))

    if provider == 'facebook':
        oauth = FacebookSignIn()
    # oauth = OAuthSignIn.get_provider(provider)

    return oauth.authorize()


@users.route('/callback/<provider>')
def oauth_callback(provider):
    """
        Adds a OAuth user to newsfeed database and logs the user into the newsfeed
        :param provider:
        :return:
        """

    if not current_user.is_anonymous():
        return redirect(url_for(index_url))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for(index_url))
    oauth_user = UserOAuth.query.filter_by(social_id=social_id).first()

    user = None
    if oauth_user:
        user_id = oauth_user.user_id
        user = UserAccount.query.filter_by(id=user_id).first()

    # Add records to databases
    if not user:
        user = UserOAuth()
        user.name = username, user.email = email
        db.session.add(user)
        db.session.commit()
        user_record = db.session.query(UserAccount).order_by(UserAccount.id.desc()).first()

        if not oauth_user:
            oauth_user = UserOAuth()
            oauth_user.social_id = social_id
            oauth_user.user_id = user_record.id
            db.session.add(oauth_user)
            db.session.commit()

    login_user(user, True)
    return redirect(url_for(index_url))

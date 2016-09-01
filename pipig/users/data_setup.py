import time

from datetime import datetime
from flask import render_template

from pipig.data import db
from pipig.users.models import UserAccountStatus, UserAccount

def setup_database_user_account_status_data():
    UserAccountStatus.query.delete()
    db.session.add(UserAccountStatus('NotRegistered'))
    db.session.add(UserAccountStatus('Registered'))
    db.session.add(UserAccountStatus('Confirmed'))
    db.session.add(UserAccountStatus('Guest'))
    db.session.commit()
    return True


def setup_database_admin_user():
    user = UserAccount.query.filter_by(email='ad@min.com').first()
    if user is None:
        db.session.add(
            UserAccount(name='admin', email='ad@min.com', password='admin', admin=True, status=True,
                    status_time=datetime.now())
        )

        db.session.commit()
    return True
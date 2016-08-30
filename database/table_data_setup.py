import time

from pipig.users.models import UserAccountStatus, UserAccount
from pipig.data import db


def data_user_account_status_id():
    db.session.add(UserAccountStatus('none'))
    db.session.add(UserAccountStatus('registered'))
    db.session.add(UserAccountStatus('confirmed'))
    db.session.add(UserAccountStatus('guest'))

    db.session.commit()


def data_create_admin_user():
    db.session.add(
        UserAccount('', email='ad@min.com', password='admin', admin=True, status=True, status_time=time.time())
        )

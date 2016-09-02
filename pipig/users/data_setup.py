from datetime import datetime
from pipig.users.models import UserAccountStatus, UserAccount


def run_setup():
    return setup_database_admin_user() and setup_database_user_account_status_data()


def setup_database_user_account_status_data():
    UserAccountStatus.query.delete()
    UserAccountStatus.create('NotRegistered')
    UserAccountStatus.create('Registered')
    UserAccountStatus.create('Confirmed')
    UserAccountStatus.create('Guest')
    return True


def setup_database_admin_user():
    user = UserAccount.query.filter_by(email='ad@min.com').first()
    if user is None:
        UserAccount.create(name='admin', email='ad@min.com', password='admin', admin=True, status=True,
                    status_time=datetime.now())
    return True
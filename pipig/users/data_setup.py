from datetime import datetime
from pipig import app
from pipig.users.models import UserAccountStatus, UserAccount


def data_setup():
    setup_database_user_account_status_data()
    setup_database_admin_user()
    return True

def setup_database_user_account_status_data():
    with app.app_context():
        UserAccountStatus.query.delete()

        UserAccountStatus.create(code='NotRegistered')
        UserAccountStatus.create(code='Registered')
        UserAccountStatus.create(code='Confirmed')
        UserAccountStatus.create(code='Guest')
    return True


def setup_database_admin_user():
    with app.app_context():
        user = UserAccount.query.filter_by(email='ad@min.com').first()
        if user is None:
            UserAccount.create(name='admin', email='ad@min.com', password='admin', admin=True, status=True,
                        status_time=datetime.now())
    return True
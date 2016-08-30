from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user_account = Table('user_account', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64), nullable=False),
    Column('email', String(length=120), nullable=False),
    Column('admin', Boolean, nullable=False, default=ColumnDefault(False)),
    Column('_password', LargeBinary(length=120), nullable=False),
    Column('_salt', String(length=120)),
    Column('_password_hash_algorithm', String(length=50), nullable=False, default=ColumnDefault('sha512')),
    Column('registration_datetime', DateTime),
    Column('account_status_id', Integer),
    Column('status_updated_datetime', DateTime),
    Column('_password_reminder_expire', DateTime),
    Column('_email_confirmation_token', String(length=100)),
    Column('_password_reminder_token', String(length=120)),
    Column('_accept_terms_of_service', Boolean, nullable=False, default=ColumnDefault(False)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user_account'].columns['registration_datetime'].create()
    post_meta.tables['user_account'].columns['status_updated_datetime'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user_account'].columns['registration_datetime'].drop()
    post_meta.tables['user_account'].columns['status_updated_datetime'].drop()

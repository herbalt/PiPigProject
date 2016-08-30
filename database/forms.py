from flask_wtf import Form
from wtforms import fields, RadioField
from wtforms.validators import Email, InputRequired

class DatabaseForm(Form):
    database_actions = fields.RadioField('Database Actions',
                                         choices=[
                                             ('Create', 'Create database'),
                                             ('Drop', 'Drop database'),
                                             ('Upgrade', 'Upgrade database'),
                                             ('Downgrade', 'Downgrade database'),
                                             ('Migrate', 'Migrate database')
                                         ])

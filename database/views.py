from flask import Blueprint, render_template, flash, url_for, redirect
from forms import DatabaseForm
from db_functions import db_create, db_drop, db_downgrade, db_migrate, db_upgrade
database = Blueprint('database', __name__)

# TODO Restrict all functions to ADMIN USER only


@database.route('/database/index',methods=['POST','GET'])
def database_index():
    form = DatabaseForm()

    if form.validate_on_submit():
        action = form.database_actions.data
        return redirect(url_for('.database_action', db_action=action))

    else:
        flash("Not Submitted")
    return render_template('database/index.html', form=form)


@database.route('/database/action/<db_action>')
def database_action(db_action):
    if db_action == 'Create':
        db_create()
        return database_action_render('Databases were created')
    elif db_action == 'Drop':
        db_drop()
        return database_action_render('Databases were Deleted')
    elif db_action == 'Upgrade':
        upgrade_name = db_upgrade()
        return database_action_render('Databases were Upgraded to %d' % upgrade_name)
    elif db_action == 'Downgrade':
        downgrade_name = db_downgrade()
        return database_action_render('Databases were Downgraded to %d' % downgrade_name)
    elif db_action == 'Migrate':
        migrated_name = db_migrate()
        return database_action_render('Databases were Migrated to %d' % migrated_name)
    else:
        return render_template('database/index.html')


def database_action_render(message):
    return render_template('database/action.html', db_action=message)

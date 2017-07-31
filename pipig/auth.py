from flask_login import AnonymousUserMixin, LoginManager

from .users.models import UserAccount

login_manager = LoginManager()

class AnonymousUser(AnonymousUserMixin):
    id = None

login_manager.anonymous_user = AnonymousUser
login_manager.login_view = "users.login"


@login_manager.user_loader
def load_user(user_id):
    return UserAccount.query.get(user_id)


from flask import url_for
from flask.ext.login import current_user
from wtforms import fields
from wtforms.validators import InputRequired

from microblog.users.forms import RegistrationForm, LoginForm, UpdateProfileForm
from microblog.users.models import UserAccount
from test_helpers.test_base import BaseTestCase
from test_helpers.test_forms import FormTestCase

class UserBlueprintTests(BaseTestCase):

    def test_page_not_found(self):
        self.client.get('/a-page-which-doesnt-exist')
        self.assertTemplateUsed('errors/404.html')

    def helper_url_requires_login(self, url):
        response = self.client.get(url, follow_redirects=True)
        self.assertTrue(response.status_code == 200)
        self.assertTemplateUsed('users/login.html')

    def test_index_requires_login(self):
        self.helper_url_requires_login('/users/index')


class UserFormTests(BaseTestCase, FormTestCase):

    def test_login_form(self):
        self.form_class = LoginForm

        self.assert_type('email', fields.StringField)
        self.assert_type('password', fields.PasswordField)

        self.assert_has_validator('email', validator=InputRequired)
        self.assert_email('email')

        self.assert_has_validator('password', validator=InputRequired)

    def test_registration_form(self):
        self.form_class = RegistrationForm

        self.assert_type('name', fields.StringField)
        self.assert_type('email', fields.StringField)
        self.assert_type('password', fields.PasswordField)
        self.assert_type('first_name', fields.StringField)
        self.assert_type('last_name', fields.StringField)

        self.assert_has_validator('name', validator=InputRequired)

        self.assert_has_validator('email', validator=InputRequired)
        self.assert_email('email')

        self.assert_has_validator('password', validator=InputRequired)

        test_form = RegistrationForm.build(name='Test', email='testtest', password='password')

        email_validate = test_form.validate_email(None)
        user_name_validate = test_form.validate_user_name(None)

        self.assertTrue(email_validate, 'Email: %s does not validate' % test_form.email)
        self.assertTrue(user_name_validate, 'Username: %s does not validate' % test_form.name)

    def test_update_profile_form(self):
        self.form_class = UpdateProfileForm

        self.assert_type('name', fields.StringField)
        self.assert_type('first_name', fields.StringField)
        self.assert_type('last_name', fields.StringField)

        self.assert_has_validator('name', validator=InputRequired)


class UserViewsTests(BaseTestCase):

    def test_users_can_login(self):

        with self.client:
            UserAccount.create(name="Joe", email="joe@gmail.com", password='1')
            response = self.client.post(url_for('users.login'), data={'email': 'joe@gmail.com', 'password': '1'})

            self.assertFalse(current_user.is_anonymous)
            self.assertTrue(current_user.name == 'Joe')


    def test_users_can_logout(self):
        UserAccount.create(name="Joe", email="joe@gmail.com", password='1')
        with self.client:
            self.client.post(url_for('users.login'), data={'email': 'joe@gmail.com', 'password': '1'})
            self.client.get(url_for('users.logout'))
            self.assertTrue(current_user.is_anonymous)

    def test_invalid_password_is_rejected(self):
        UserAccount.create(name="Joe", email="joe@gmail.com", password='1')

        with self.client:
            response = self.client.post(url_for('users.login'), data={'email': 'joe@gmail.com', 'password': '12'})
            self.assertTrue(current_user.is_anonymous)
            self.assert200(response)
            self.assertIn("Invalid password", response.data)

    def test_user_can_register_account(self):

        with self.client:
            response = self.client.post(url_for('users.register'), data={'name': 'Joe', 'password': '1', 'email': 'joe@gmail.com'})
            self.assert_redirects(response, url_for('users.user_index'))

            self.assertTrue(current_user.name == 'Joe')
            self.assertEqual(current_user.email, "joe@gmail.com")
            self.assertFalse(current_user.is_anonymous)

            self.client.get(url_for('users.logout'))
            self.client.post(url_for('users.login'), data={'email': 'joe@gmail.com', 'password': '1'})
            self.assertFalse(current_user.is_anonymous)
            self.assertTrue(current_user.name == 'Joe')


    def test_user_cannot_register_email_twice(self):
        with self.client:
            response1 = self.client.post(url_for('users.register'),
                                         data={'name': 'Joe', 'password': '1', 'email': 'joe@gmail.com'})
            self.client.get(url_for('users.logout'))
            response2 = self.client.post(url_for('users.register'),
                                         data={'name': 'Joesph', 'password': '12', 'email': 'joe@gmail.com'})
            self.assertTrue(current_user.is_anonymous)
            self.assert200(response2)
            response3 = self.client.post(url_for('users.register'),
                                         data={'name': 'Joe', 'password': '1', 'email': 'joesph@gmail.com'})
            self.assertFalse(current_user.is_anonymous)


    def test_user_is_redirected_to_index_from_logout(self):
        UserAccount.create(name="Joe", email="joe@gmail.com", password='1')
        with self.client:
            self.client.post(url_for('users.login'), data={'email': 'joe@gmail.com', 'password': '1'})
            response = self.client.get(url_for('users.logout'))
            self.assert_redirects(response, url_for('users.user_index'))
            self.assertTrue(current_user.is_anonymous)

    def test_oauth_registration(self):
        self.assertFalse(True, 'Unwritten test for Oauth registration')
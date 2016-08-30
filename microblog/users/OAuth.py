from abc import abstractmethod

from flask import url_for, redirect, request
from rauth import OAuth2Service
from credentials import credentials as oauth


class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = oauth.OAUTH_CREDENTIALS[provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    @abstractmethod
    def authorize(self):
        raise NotImplementedError

    @abstractmethod
    def callback(self):
        raise NotImplementedError

    def get_callback_url(self):
        return url_for('users.oauth_callback', provider=self.provider_name, _external=True)

    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


class FacebookSignIn(OAuthSignIn):
    def __init__(self):
        super(FacebookSignIn, self).__init__('facebook')
        self.service = OAuth2Service(name='facebook',
                                     client_id=self.consumer_id,
                                     client_secret=self.consumer_secret,
                                     access_token_url='https://graph.facebook.com/oauth/access_token',
                                     authorize_url='https://graph.facebook.com/oauth/authorize',
                                     base_url='https://graph.facebook.com/')

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_uri=self.get_callback_url()
        ))

    def callback(self):
        if 'code' not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
            data={
                'code': request.args['code'],
                'grant_type': 'authorization_code',
                'redirect_uri': self.get_callback_url()
            })
        me = oauth_session.get('me').json()
        return ('facebook$' + me['id'],
                me.get('email').split('@')[0]), \
               me.get('email')


class GoogleSignIn(OAuthSignIn):
    def __init__(self):
        super(GoogleSignIn, self).__init__('google')
        raise NotImplementedError

    def authorize(self):
        raise NotImplementedError

    def callback(self):
        raise NotImplementedError



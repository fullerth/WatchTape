from .base import FunctionalTest
import unittest

from WatchTape.settings import INSTALLED_APPS, TEMPLATE_CONTEXT_PROCESSORS, \
    AUTHENTICATION_BACKENDS, SITE_ID, LOGIN_REDIRECT_URL

class DjangoAllauthSetup(unittest.TestCase):
    def test_djangoallauth_settings_INSTALLED_APPS(self):
        self.assertIn('django.contrib.sites', INSTALLED_APPS)
        self.assertIn('allauth', INSTALLED_APPS)
        self.assertIn('allauth.account', INSTALLED_APPS)
        self.assertIn('allauth.socialaccount', INSTALLED_APPS)
        self.assertIn('allauth.socialaccount.providers.facebook', 
                      INSTALLED_APPS)
    
    def test_djangoallauth_settings_TEMPLATE_CONTEXT_PROCESSORS(self):
        self.assertIn('django.core.context_processors.request', 
                      TEMPLATE_CONTEXT_PROCESSORS)
        self.assertIn('django.contrib.auth.context_processors.auth', 
                      TEMPLATE_CONTEXT_PROCESSORS)
        self.assertIn('allauth.account.context_processors.account', 
                      TEMPLATE_CONTEXT_PROCESSORS)
        self.assertIn('allauth.socialaccount.context_processors.socialaccount', 
                      TEMPLATE_CONTEXT_PROCESSORS)
        
    def test_djangoallauth_settings_AUTHENTICATION_BACKENDS(self):
        self.assertIn('django.contrib.auth.backends.ModelBackend',
                      AUTHENTICATION_BACKENDS)
        self.assertIn('allauth.account.auth_backends.AuthenticationBackend',
                      AUTHENTICATION_BACKENDS)
        
    def test_djangoallauth_settings_LOGIN_REDIRECT(self):
        self.assertIn('/', LOGIN_REDIRECT_URL)
        
    def test_djangoallauth_settings_SITE_ID(self):
        self.assertEqual(2, SITE_ID)        

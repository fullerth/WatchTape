from .base import FunctionalTest

from django.contrib.auth.models import User

from django.test.utils import override_settings
from django.conf import settings

from django.contrib.sites.models import Site

from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers import facebook


class NavbarTest(FunctionalTest):
    def setUp(self):
        self.home_url = [self.server_url, '/']
        site_expected_data = {'domain':'localhost', 'name':'localhost'}
        site_instance = Site.objects.create(
                                    domain=site_expected_data['domain'],
                                    name=site_expected_data['name']
                                    )
        self.site = {
                     'instance': site_instance, 
                     'expected_data': site_expected_data
                    }
        social_app_expected_data = {'name':'test_fb', 'provider':'facebook',
                                    'secret':'foo', 'client_id':'bar'}
        social_app_instance = SocialApp.objects.create(
                                name=social_app_expected_data['name'],
                                provider=social_app_expected_data['provider'],
                                secret=social_app_expected_data['secret'],
                                client_id=social_app_expected_data['client_id']
                                )
        social_app_instance.full_clean()
        self.social_app = {
                           'instance':social_app_instance,
                           'expected_data':social_app_expected_data
                           }
        super().setUp()
        
    def _loginSuperUser(self):
        self.admin_user = {'login':'admin', 'password':'admin', 
                      'email':'admin@example.com'}
        User.objects.create_superuser(
                                      username=self.admin_user['login'],
                                      password=self.admin_user['password'],
                                      email=self.admin_user['email']
                                      )
        
        self.browser.get(''.join([self.server_url, '/accounts/login/']))
                
        
        login = self.browser.find_element_by_id("id_login")
        password = self.browser.find_element_by_id("id_password")
        sign_in = self.browser.find_element_by_class_name("primaryAction")
        
        login.send_keys(self.admin_user['login'])
        password.send_key(self.admin_user['password'])
        sign_in.click()
    
    def test_navbar_has_login_on_right(self):
        #Load the homepage
        self.browser.get(''.join(self.home_url))
        
        #See a button group on the right side of the navbar
        button_group = self.browser.find_element_by_id('id_right_navbar')
        self.assertIn("navbar-right", button_group.get_attribute("class"), 
                      msg="id_right_navbar should have navbar-right class")
        login_button_li = button_group.find_element_by_id('login')
        login_button_link = login_button_li.find_element_by_xpath(".//a")
        login_href = login_button_link.get_attribute("href")
        self.assertEqual(''.join((self.server_url,'/accounts/login')), 
                        login_href, msg="Incorrect login href")
        
    @override_settings(SITE_ID=2, DEBUG=True)
    def test_logged_in_user_sees_logout(self):
        #Load the homepage
        #self.browser.get(''.join(self.home_url))
        
        self.site['instance'].save()
        self.social_app['instance'].save()
        self.social_app['instance'].sites.add(self.site['instance'])
        self._loginSuperUser()

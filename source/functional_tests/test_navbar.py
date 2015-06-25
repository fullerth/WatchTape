from .base import FunctionalTest

from django.contrib.auth.models import User

from django.test.utils import override_settings
from django.conf import settings

from django.contrib.sites.models import Site

from allauth.socialaccount.models import SocialApp

from selenium.common.exceptions import NoSuchElementException


class NavbarTest(FunctionalTest):
    def setUp(self):
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
        
    def _login_super_user(self):
        self.site['instance'].save()
        self.social_app['instance'].save()
        self.social_app['instance'].sites.add(self.site['instance'])
        self.admin_user = {'login':'admin', 'password':'admin', 
                      'email':'admin@example.com'}
        settings.SITE_ID = self.site['instance'].id
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
        password.send_keys(self.admin_user['password'])
        sign_in.click()
        
    def _get_login_button(self):
        #See a button group on the right side of the navbar
        button_group = self.browser.find_element_by_id('id_right_navbar')
        login_button_li = button_group.find_element_by_id('id_login')
        login_button_anchor = login_button_li.find_element_by_xpath(".//a")
        return{'button_group' : button_group, 'li':login_button_li,
               'a':login_button_anchor}
        
    def _get_logout_button(self):
        #See a button group on the right side of the navbar
        button_group = self.browser.find_element_by_id('id_right_navbar')
        logout_button_li = button_group.find_element_by_id('id_logout')
        logout_button_anchor = logout_button_li.find_element_by_xpath(".//a")
        return{'button_group' : button_group, 'li':logout_button_li,
               'a':logout_button_anchor}

    
    def test_logged_out_navbar_has_correct_login_on_right(self):
        #Load the homepage
        self.browser.get(self.home_url)
        
        login = self._get_login_button()
        
        #See a button group on the right side of the navbar
        self.assertIn(
                      "navbar-right", 
                      login['button_group'].get_attribute("class"), 
                      msg="id_right_navbar should have navbar-right class"
                     )
        
        #Button goes to the login url
        self.assertEqual(
                         ''.join((self.server_url,'/accounts/login')), 
                         login['a'].get_attribute("href"), 
                         msg="Incorrect login href"
                        )
        
    def test_logged_in_navbar_has_correct_logout_on_right(self):
        #Load the homepage
        self.browser.get(self.home_url)
        
        self._login_super_user()
        
        logout = self._get_logout_button()
        
        #Button group exists on the right side of the navbar
        self.assertIn(
                      "navbar-right", 
                      logout['button_group'].get_attribute("class"),
                      msg="id_right_navbar should have navbar-right class"
                     )
        
        #Button goes to the logout url
        self.assertEqual(''.join((self.server_url,'/accounts/logout')),
                         logout['a'].get_attribute("href"), 
                         msg="Incorrect logout href")
        
    def test_logged_out_user_sees_only_login(self):
        #Load the homepage
        self.browser.get(self.home_url)
        
        self._get_login_button()
        
        #Make sure the logout button is not displayed
        with self.assertRaises(NoSuchElementException):
            self._get_logout_button()
        
    def test_logged_in_user_sees_only_logout(self):
        #user logs in
        self._login_super_user()
        
        #user is redirected to the login url
        self.assertEqual(
                         self.browser.current_url, 
                         self.server_url+settings.LOGIN_REDIRECT_URL, 
                         msg="Login not successful"
                        )
            
        #user now sees the logout button (throws NoSuchElementException on failure)
        self._get_logout_button()
        
        with self.assertRaises(NoSuchElementException):
            self._get_login_button()
            
    

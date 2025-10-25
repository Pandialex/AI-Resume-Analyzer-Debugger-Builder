from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User

class AccountsFlowTests(TestCase):
    def test_register_and_login(self):
        c = Client()
        resp = c.post(reverse("accounts:register"), {
            "username":"test1","email":"t@x.com","password1":"Abcd1234!","password2":"Abcd1234!"
        })
        self.assertEqual(resp.status_code, 302)  # redirected to verify_otp


from django.test import TestCase, Client
from django.urls import reverse

class EmailSendTests(TestCase):
    def test_send_simple_email(self):
        c = Client()
        resp = c.post(reverse('mailapp:send_email'), {
            'sender': 'sender@test.com',
            'recipients': 'r1@test.com, r2@test.com',
            'cc': '',
            'subject': 'hello',
            'body': 'test body',
        })
        self.assertEqual(resp.status_code, 302)  # redirect on success
        # check that SentEmail created
        from .models import SentEmail
        self.assertTrue(SentEmail.objects.filter(subject='hello').exists())

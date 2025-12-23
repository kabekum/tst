# backend/core/tests/test_models.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import Firm, Client, Matter

User = get_user_model()

class ModelsSmokeTest(TestCase):
    def test_create_firm_client_matter(self):
        firm = Firm.objects.create(name="Acme Law")
        user = User.objects.create_user(username="bob", password="pass")
        client = Client.objects.create(firm=firm, name="John Doe")
        matter = Matter.objects.create(firm=firm, client=client, title="Case A")
        self.assertEqual(str(firm), "Acme Law")
        self.assertEqual(str(client), "John Doe")
        self.assertEqual(str(matter), "Case A")

from datetime import timedelta
from rest_framework import status
from rest_framework.test import APITestCase
from members.models import Member
from recover.models import RecoverToken


class RecoverPasswordTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        Member.objects.create_user(username="test",
                                   email="test@example.com",
                                   password="Test")

    def request_token_issue(self, email):
        data = {"email": email}
        return self.client.post("/recover/token/", data)

    def make_token_expired(self, token):
        instance = RecoverToken.objects.get(token=token)
        instance.valid_until = instance.valid_until - timedelta(days=2)
        instance.save()

    def test_recover_password(self):
        email = "test@example.com"
        member_id = Member.objects.get(email=email).id
        member_username = Member.objects.get(email=email).username
        password = "renewed"

        # 1. issue token
        res = self.request_token_issue(email)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["member"], member_id)
        self.assertEqual(RecoverToken.objects.count(), 1)

        token = res.data["token"]

        # 2. verify token
        data = {"token": token}
        res = self.client.post("/recover/verify/", data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["token"], token)
        self.assertEqual(res.data["member"], member_id)

        # 3. renew password
        data = {"token": token, "password": password}
        res = self.client.post("/recover/renew/", data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["token"], token)
        self.assertEqual(res.data["member"], member_id)
        self.assertEqual(RecoverToken.objects.count(), 0)

        # 4. login with new password
        data = {"username": member_username, "password": password}
        res = self.client.post("/auth/token/", data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_issue_token_failure(self):
        email = "wrong@example.com"

        # 1. issue token
        res = self.request_token_issue(email)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_expired_token_failure(self):
        email = "test@example.com"

        # 1. issue token and make it expured
        res = self.request_token_issue(email)
        token = res.data["token"]
        self.make_token_expired(token)

        # 2. verify token
        data = {"token": token}
        res = self.client.post("/recover/verify/", data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(RecoverToken.objects.count(), 0)

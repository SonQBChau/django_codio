from django.test import LiveServerTestCase
from requests.auth import HTTPBasicAuth
from rest_framework.test import RequestsClient
from django.contrib.auth import get_user_model
from blog.models import Tag


class TagApiTestCase(LiveServerTestCase):
    """
        The TagApiTestCase inherits from LiveServerTestCase, which means a
        Django Dev Server will be started when the test case is run.
    """
    def setUp(self):
        """
            setUp() creates a testing user, inserts some test Tag objects into the
            database, then sets self.client to an instance of RequestClient.
        """
        get_user_model().objects.create_user(
            email="testuser@example.com", password="password"
        )
        self.tag_values = {"tag1", "tag2", "tag3", "tag4"}
        for t in self.tag_values:
            Tag.objects.create(value=t)
        self.client = RequestsClient()

    def test_tag_list(self):
        """
            test_tag_list() uses self.client to fetch a list of Tags using the API,
            then verifies that they match what’s in the database.
        """
        resp = self.client.get(self.live_server_url + "/api/v1/tags/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()["results"]
        self.assertEqual(len(data), 4)
        self.assertEqual(self.tag_values, {t["value"] for t in data})

    def test_tag_create_basic_auth(self):
        """
            test_tag_create_basic_auth() authenticates by setting client.auth to
            an instance of HTTPBasicAuth. It then creates a new Tag and tests that
            the number of tags in the DB has increased.
        """
        self.client.auth = HTTPBasicAuth("testuser@example.com", "password")
        resp = self.client.post(
            self.live_server_url + "/api/v1/tags/", {"value": "tag5"}
        )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(Tag.objects.all().count(), 5)

    def test_tag_create_token_auth(self):
        """
            test_tag_create_token_auth() performs the same test as
            test_tag_create_basic_auth(), but authenticates with a token instead
            of basic authentication. It fetches the token by using the token-auth
            endpoint.
        """
        token_resp = self.client.post(
            self.live_server_url + "/api/v1/token-auth/",
            {"username": "testuser@example.com", "password": "password"},
        )
        self.client.headers["Authorization"] = "Token " + token_resp.json()["token"]
        resp = self.client.post(
            self.live_server_url + "/api/v1/tags/", {"value": "tag5"}
        )
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(Tag.objects.all().count(), 5)

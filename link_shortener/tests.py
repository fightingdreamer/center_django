from django.urls import reverse
from rest_framework.exceptions import status
from rest_framework.test import APITestCase

from link_shortener import models
from link_shortener.mapping import encode_with_padding


def create_redirection(client):
    url = reverse("create-redirection")
    data = {"location": "https://httpstatuses.io"}
    return client.post(url, data, format="json")


def visit_redirection(client):
    name = encode_with_padding(uid=1, size=10, randomize=True)
    url = reverse("visit-redirection", args=[name])
    return client.get(url)


def get_user_info(client):
    name = encode_with_padding(uid=1, size=10, randomize=True)
    url = reverse("get-user-info", args=[name])
    return client.get(url)


def get_statistics(client):
    name = encode_with_padding(uid=1, size=10, randomize=True)
    url = reverse("get-statistics", args=[name])
    return client.get(url)


class RedirectionTests(APITestCase):
    def test_create_redirection(self):
        response = create_redirection(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Redirection.objects.count(), 1)

    def test_reuse_redirection(self):
        response = create_redirection(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Redirection.objects.count(), 1)

        response = create_redirection(self.client)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Redirection.objects.count(), 1)

    def test_visit_redirection(self):
        response = create_redirection(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = visit_redirection(self.client)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response.headers["location"], "https://httpstatuses.io")
        self.assertEqual(models.Redirection.objects.get().hits, 1)

    def test_user_info(self):
        response = create_redirection(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = get_user_info(self.client)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            models.Redirection.objects.get().user_ip, response.json()["user_ip"]
        )
        self.assertEqual(
            models.Redirection.objects.get().user_agent, response.json()["user_agent"]
        )

    def test_statistics(self):
        response = create_redirection(self.client)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = visit_redirection(self.client)
        response = visit_redirection(self.client)
        response = visit_redirection(self.client)

        response = get_statistics(self.client)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(models.Redirection.objects.get().hits, response.json()["hits"])

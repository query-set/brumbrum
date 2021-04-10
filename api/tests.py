from django.urls import reverse
from rest_framework.test import APITestCase


class CarViewSetTests(APITestCase):
    def setUp(self):
        self.url = reverse("cars-list")
        self.data = {"make": "honda", "model": "civic"}

    def test_create_car(self):
        response = self.client.post(self.url, data=self.data)
        assert response.status_code == 201, response.data
        assert response.data["make"] == self.data["make"]
        assert response.data["model"] == self.data["model"]

    def test_create_car_with_missing_model(self):
        data = self.data
        del data["model"]
        response = self.client.post(self.url, data=self.data)
        assert response.status_code == 400, response.data
        assert response.data["model"][0] == "This field is required."

    def test_create_car_with_missing_make(self):
        data = self.data
        del data["make"]
        response = self.client.post(self.url, data=self.data)
        assert response.status_code == 400, response.data
        assert response.data["make"][0] == "This field is required."

    def test_create_car_that_does_not_exist_in_the_api_db(self):
        data = {"make": "honda", "model": "XYZ"}
        response = self.client.post(self.url, data=self.data)
        assert response.status_code == 400, response.data
        assert response.data["make"][0] == "This field is required."

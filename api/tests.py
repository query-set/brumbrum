from django.urls import reverse
from rest_framework.test import APITestCase

from api.models import Car


class CarCreateViewSetTests(APITestCase):
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

    def test_create_model_that_does_not_exist_in_the_api_db(self):
        data = {"make": "honda", "model": "blablabla"}
        response = self.client.post(self.url, data=data)
        assert response.status_code == 400, response.data
        assert response.data["non_field_errors"][0] == "Model not found."

    def test_create_car_with_make_that_does_not_exist(self):
        data = {"make": "blablabla", "model": "civic"}
        response = self.client.post(self.url, data=data)
        assert response.status_code == 400, response.data
        error_string = f"Cannot find models with '{data['make']}' make."
        assert response.data["non_field_errors"][0] == error_string

    def test_create_car_that_already_exists_in_the_database(self):
        response = self.client.post(self.url, data=self.data)
        assert response.status_code == 201, response.data
        response = self.client.post(self.url, data=self.data)
        assert response.status_code == 400, response.data
        assert "already exists in the database" in response.data["non_field_errors"][0]


class CarListViewSetTests(APITestCase):
    def url(self):
        return reverse("cars-list")

    def setUp(self):
        self.car = Car.objects.create(make="honda", model="civic")

    def test_cars_fields(self):
        response = self.client.get(self.url())
        assert response.status_code == 200, response.data
        for field in ["id", "make", "model", "avg_rating"]:
            assert field in response.data[0].keys(), (field, response.data)

    def test_list_more_than_one_car(self):
        Car.objects.create(make="honda", model="accord")
        response = self.client.get(self.url())
        assert response.status_code == 200, response.data
        assert len(response.data) == 2, response.data


class RateTests(APITestCase):
    def setUp(self):
        self.url = reverse("rate-list")
        self.car = Car.objects.create(make="honda", model="civic")

    def test_rate_car(self):
        # TODO: to be continued
        data = {"car_id": self.car.id, "rating": 5}
        response = self.client.post(self.url, data=data)
        assert response.status_code == 201, response.data
        self.car.refresh_from_db()
        assert self.car.avg_rating == 5.0
        data = {"car_id": self.car.id, "rating": 1}
        response = self.client.post(self.url, data=data)
        assert response.status_code == 201, response.data
        self.car.refresh_from_db()
        assert self.car.avg_rating == 3.0

    def test_rate_not_existing_car(self):
        data = {"car_id": 5, "rating": 5}
        response = self.client.post(self.url, data=data)
        error_string = 'Invalid pk "5" - object does not exist.'
        assert response.status_code == 400, response.data
        assert error_string in response.data["car_id"][0]

    def test_rate_car_with_too_high_grade(self):
        data = {"car_id": self.car.id, "rating": 6}
        response = self.client.post(self.url, data=data)
        assert response.status_code == 400, response.data
        error_string = "Ensure this value is less than or equal to 5."
        assert error_string in response.data["rating"][0]

    def test_rate_car_with_too_low_grade(self):
        data = {"car_id": self.car.id, "rating": 0}
        response = self.client.post(self.url, data=data)
        assert response.status_code == 400, response.data
        error_string = "Ensure this value is greater than or equal to 1."
        assert error_string in response.data["rating"][0]


class PopularVievTest(APITestCase):
    def setUp(self):
        pass

    def test_list_by_popular(self):
        pass

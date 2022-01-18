import requests
from assertpy import assert_that

class TestFavorites:
    AUTH = {'Authorization': 'Bearer token=DyaLehQJWRYLirxw9XuXJazc'}
    URL = "https://airportgap.dev-tester.com/api/favorites"

    def _get_first_favorite(self):
        response_id = requests.get(self.URL, headers=self.AUTH)
        return response_id.json().get("data")[0].get("id")

    def test_create_favorite_airport(self):
        response = requests.post(self.URL, data={
            "airport_id": "LAE",
            "note": "Saya suka airport ini"
        }, headers=self.AUTH)
        assert_that(response.status_code).is_equal_to(201)
        airport = response.json()["data"]["attributes"]["airport"]
        assert_that(airport["name"]).is_equal_to("Nadzab Airport")
        assert_that(airport['country']).is_equal_to_ignoring_case("Papua New Guinea")
        #print(response.text)

    def test_get_favorite(self):
        response = requests.get(self.URL, headers=self.AUTH)
        assert_that(response.status_code).is_equal_to(200)
        print(response.text)
        assert_that(len(response.json().get("data"))).is_greater_than_or_equal_to(1)

    def test_update_favorite_note(self):
        id = self._get_first_favorite()
        payload = {'note': 'Notenya diubah'}
        response = requests.patch(f"{self.URL}/{id}", headers=self.AUTH, data=payload)
        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.json()["data"]["attributes"]["note"]).is_equal_to('Notenya diubah')

    def test_delete_favorite(self):
        id = self._get_first_favorite()
        response = requests.delete(f"{self.URL}/{id}", headers=self.AUTH)
        assert_that(response.status_code).is_equal_to(204)

import requests
import pytest

account1 = {
    "name": "Jan",
    "surname": "Kowalski",
    "pesel": "01234567890"
}

account2 = {
    "name": "Karolina",
    "surname": "Lis",
    "pesel": "00112233445"
}

url = "http://127.0.0.1:5000/api/accounts"

class TestApi:
    def test_account_creation(self):
        response = requests.post(url, json=account1)
        assert response.status_code == 201
        assert response.json()["message"] == "Account created"
    def test_show_accounts(self):
        requests.post(url, json=account2)
        response = requests.get(url)
        assert response.status_code == 200
        accounts = response.json()
        expected_accounts = [
            {
                "balance": 0,
                "name": "Jan",
                "pesel": "01234567890",
                "surname": "Kowalski"
            },
            {
                "balance": 0,
                "name": "Karolina",
                "pesel": "00112233445",
                "surname": "Lis"
            }
        ]
        for expected in expected_accounts:
            assert expected in accounts
    def test_get_pesel(self):
        response = requests.get(f"{url}/01234567890")
        assert response.status_code == 200
        assert response.json() == {
                "balance": 0,
                "name": "Jan",
                "pesel": "01234567890",
                "surname": "Kowalski"
            }
    def test_get_pesel_not_existing(self):
        response = requests.get(f"{url}/00000000000")
        assert response.status_code == 404
    def test_update(self):
        response = requests.patch(f"{url}/00112233445", json={
            "name": "Tomasz",
            "surname": "Adamczyk",
        })
        assert response.status_code == 200
        assert response.json()["message"] == "Account updated"
        assert requests.get(f"{url}/00112233445").json() == {
            "balance": 0,
            "name": "Tomasz",
            "pesel": "00112233445",
            "surname": "Adamczyk"
        }
    def test_update_only_one(self):
        response = requests.patch(f"{url}/00112233445", json={"name": "Piotr"})
        assert response.status_code == 200
        assert response.json()["message"] == "Account updated"
        assert requests.get(f"{url}/00112233445").json() == {
            "balance": 0,
            "name": "Piotr",
            "pesel": "00112233445",
            "surname": "Adamczyk"
        }
    def test_update_not_existing(self):
        response = requests.patch(f"{url}/00000000000", json={"name": "Piotr"})
        assert response.status_code == 404
    def test_delete(self):
        response = requests.delete(f"{url}/00112233445")
        assert response.status_code == 200
        assert response.json()["message"] == "Account deleted"
        assert requests.get(f"{url}/00112233445").status_code == 404
    def test_delete_not_existing(self):
        response = requests.delete(f"{url}/00000000000")
        assert response.status_code == 404

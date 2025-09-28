import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_register_and_login(api):
    payload = {
        "username": "u1",
        "password": "Testpass123",
        "email": "u1@mail.com",
        "role": "student",
    }
    r = api.post("/api/register/", payload, format="json")
    assert r.status_code in (200, 201)

    r = api.post("/api/token/", {"username": "u1", "password": "Testpass123"}, format="json")
    assert r.status_code == 200
    assert "access" in r.data and "refresh" in r.data

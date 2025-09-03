import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api():
    return APIClient()


@pytest.fixture
def teacher(db):
    user = User.objects.create_user(username="teacher", password="Pass12345!", role="teacher")
    return user


@pytest.fixture
def student(db):
    user = User.objects.create_user(username="student", password="Pass12345!", role="student")
    return user


@pytest.fixture
def admin_user(db):
    user = User.objects.create_user(
        username="admin1",
        password="Pass12345!",
        role="admin",
        is_staff=True,
        is_superuser=True,
    )
    return user


@pytest.fixture
def auth(api):
    """Логин через JWT, возвращает функцию для авторизации клиента под нужным юзером."""

    def _auth(user):
        resp = api.post(
            "/api/token/",
            {"username": user.username, "password": "Pass12345!"},
            format="json",
        )
        assert resp.status_code == 200, resp.content
        token = resp.data["access"]
        api.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        return api

    return _auth

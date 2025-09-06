import pytest
from django.contrib.auth import get_user_model

from courses.models import Course
from users.permissions import IsOwnerOrReadOnly, ReadOnlyOrTeacherAdmin

pytestmark = pytest.mark.django_db
User = get_user_model()


def make_user(role, username):
    return User.objects.create_user(username=username, password="Pass12345!", role=role)


def test_readonly_or_teacher_admin_allows_safe_methods():
    perm = ReadOnlyOrTeacherAdmin()

    class Req:
        method = "GET"
        user = type("U", (), {"is_authenticated": False})()

    assert perm.has_permission(Req, view=None) is True


def test_is_owner_or_readonly_allows_owner_edit():
    owner = make_user("teacher", "t1")
    other = make_user("teacher", "t2")
    course = Course.objects.create(owner=owner, title="C", description="D")

    class ReqOwner:
        method = "PATCH"
        user = owner

    class ReqOther:
        method = "PATCH"
        user = other

    perm = IsOwnerOrReadOnly()
    assert perm.has_object_permission(ReqOwner, view=None, obj=course) is True
    assert perm.has_object_permission(ReqOther, view=None, obj=course) is False

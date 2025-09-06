import pytest

from courses.models import Course, Material, Section

pytestmark = pytest.mark.django_db


def setup_section(user):
    c = Course.objects.create(owner=user, title="C2", description="D")
    s = Section.objects.create(course=c, title="S")
    return c, s


def test_material_list_public(api, teacher):
    _, sec = setup_section(teacher)
    Material.objects.create(section=sec, title="M1", content="txt")
    r = api.get("/api/materials/")
    assert r.status_code == 200
    assert r.data["count"] >= 1


def test_student_cannot_create_material(auth, student, teacher):
    api = auth(student)
    _, sec = setup_section(teacher)
    r = api.post("/api/materials/", {"section": sec.id, "title": "M2", "content": "x"}, format="json")
    assert r.status_code in (401, 403)


def test_teacher_can_create_material_for_own_course(auth, teacher):
    api = auth(teacher)
    _, sec = setup_section(teacher)
    r = api.post("/api/materials/", {"section": sec.id, "title": "M-own", "content": "x"}, format="json")
    assert r.status_code == 201
    mat_id = r.data["id"]
    r2 = api.patch(f"/api/materials/{mat_id}/", {"title": "M-own-upd"}, format="json")
    assert r2.status_code == 200


def test_other_teacher_cannot_edit_foreign_material(auth, teacher):
    _, sec = setup_section(teacher)
    mat = Material.objects.create(section=sec, title="M-A", content="x")

    from django.contrib.auth import get_user_model

    User = get_user_model()
    other = User.objects.create_user(username="teacher3", password="Pass12345!", role="teacher")

    api2 = auth(other)
    r2 = api2.patch(f"/api/materials/{mat.id}/", {"title": "hack"}, format="json")
    assert r2.status_code in (403, 404)

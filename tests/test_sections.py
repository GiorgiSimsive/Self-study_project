import pytest

from courses.models import Course, Section

pytestmark = pytest.mark.django_db


def create_course_for(user):
    return Course.objects.create(owner=user, title="C", description="D")


def test_section_list_public(api, teacher):
    course = create_course_for(teacher)
    Section.objects.create(course=course, title="S1")
    r = api.get("/api/sections/")
    assert r.status_code == 200
    assert r.data["count"] >= 1


def test_student_cannot_create_section(auth, student, teacher):
    api = auth(student)
    course = create_course_for(teacher)
    r = api.post("/api/sections/", {"course": course.id, "title": "S2"}, format="json")
    assert r.status_code in (401, 403)


def test_teacher_can_create_section_for_own_course(auth, teacher):
    api = auth(teacher)
    course = create_course_for(teacher)
    r = api.post("/api/sections/", {"course": course.id, "title": "S-own"}, format="json")
    assert r.status_code == 201
    sec_id = r.data["id"]
    r2 = api.patch(f"/api/sections/{sec_id}/", {"title": "S-own-upd"}, format="json")
    assert r2.status_code == 200


def test_other_teacher_cannot_edit_foreign_section(auth, teacher):
    course_a = create_course_for(teacher)
    sec = Section.objects.create(course=course_a, title="S-A")

    from django.contrib.auth import get_user_model

    User = get_user_model()
    other = User.objects.create_user(username="teacher2", password="Pass12345!", role="teacher")

    api2 = auth(other)
    r2 = api2.patch(f"/api/sections/{sec.id}/", {"title": "hack"}, format="json")
    assert r2.status_code in (403, 404)

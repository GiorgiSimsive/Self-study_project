import pytest


@pytest.mark.django_db
def test_student_cannot_create_course(auth, student):
    api = auth(student)
    r = api.post("/api/courses/", {"title": "X", "description": "Y"}, format="json")
    assert r.status_code in (401, 403)


@pytest.mark.django_db
def test_teacher_can_create_own_course(auth, teacher):
    api = auth(teacher)
    r = api.post("/api/courses/", {"title": "Course1", "description": "D"}, format="json")
    assert r.status_code == 201
    course_id = r.data["id"]

    r2 = api.patch(f"/api/courses/{course_id}/", {"title": "Course1-upd"}, format="json")
    assert r2.status_code == 200


@pytest.mark.django_db
def test_other_teacher_cannot_edit_foreign_course(auth, teacher):
    api = auth(teacher)
    r = api.post("/api/courses/", {"title": "CourseA", "description": "D"}, format="json")
    course_id = r.data["id"]

    from django.contrib.auth import get_user_model

    User = get_user_model()
    other = User.objects.create_user(username="teacher2", password="Pass12345!", role="teacher")

    api2 = auth(other)
    r2 = api2.patch(f"/api/courses/{course_id}/", {"title": "Hack"}, format="json")
    assert r2.status_code in (403, 404)

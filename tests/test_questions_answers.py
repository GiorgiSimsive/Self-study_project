import pytest

from courses.models import Answer, Course, Material, Question, Section, Test

pytestmark = pytest.mark.django_db


def setup_test_tree(user):
    course = Course.objects.create(owner=user, title="CT", description="")
    sec = Section.objects.create(course=course, title="S")
    mat = Material.objects.create(section=sec, title="M", content="x")
    test = Test.objects.create(material=mat, title="T")
    return course, sec, mat, test


def test_question_list_public(api, teacher):
    _, _, _, test = setup_test_tree(teacher)
    Question.objects.create(test=test, text="Q1")
    r = api.get("/api/questions/")
    assert r.status_code == 200
    assert r.data["count"] >= 1


def test_answer_list_public(api, teacher):
    _, _, _, test = setup_test_tree(teacher)
    q = Question.objects.create(test=test, text="Q2")
    Answer.objects.create(question=q, text="A1", is_correct=False)
    r = api.get("/api/answers/")
    assert r.status_code == 200
    assert r.data["count"] >= 1


def test_student_cannot_create_question_or_answer(auth, student, teacher):
    api = auth(student)
    _, _, _, test = setup_test_tree(teacher)
    r1 = api.post("/api/questions/", {"test": test.id, "text": "Qx"}, format="json")
    assert r1.status_code in (401, 403)

    q = Question.objects.create(test=test, text="Q3")
    r2 = api.post("/api/answers/", {"question": q.id, "text": "Ax", "is_correct": True}, format="json")
    assert r2.status_code in (401, 403)


def test_teacher_can_create_q_and_a_for_own_test(auth, teacher):
    api = auth(teacher)
    _, _, _, test = setup_test_tree(teacher)
    rq = api.post("/api/questions/", {"test": test.id, "text": "Qt"}, format="json")
    assert rq.status_code == 201
    qid = rq.data["id"]

    ra = api.post("/api/answers/", {"question": qid, "text": "At", "is_correct": True}, format="json")
    assert ra.status_code == 201


def test_other_teacher_cannot_edit_foreign_q_or_a(auth, teacher):
    _, _, _, test = setup_test_tree(teacher)
    q = Question.objects.create(test=test, text="Q-foreign")
    a = Answer.objects.create(question=q, text="A-foreign", is_correct=False)

    from django.contrib.auth import get_user_model

    User = get_user_model()
    other = User.objects.create_user(username="teacher4", password="Pass12345!", role="teacher")

    api2 = auth(other)
    r1 = api2.patch(f"/api/questions/{q.id}/", {"text": "hack"}, format="json")
    r2 = api2.patch(f"/api/answers/{a.id}/", {"text": "hack2"}, format="json")
    assert r1.status_code in (403, 404)
    assert r2.status_code in (403, 404)

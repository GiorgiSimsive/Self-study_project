import pytest

from courses.models import Answer, Course, Material, Question, Section, Test


@pytest.mark.django_db
def test_student_submit_test_flow(auth, teacher, student):
    api_t = auth(teacher)
    course_id = api_t.post("/api/courses/", {"title": "C1", "description": ""}, format="json").data["id"]
    course = Course.objects.get(id=course_id)
    section = Section.objects.create(course=course, title="S1")
    material = Material.objects.create(section=section, title="M1", content="txt")
    test = Test.objects.create(material=material, title="T1")
    q = Question.objects.create(test=test, text="2+2")
    a_correct = Answer.objects.create(question=q, text="4", is_correct=True)
    Answer.objects.create(question=q, text="3", is_correct=False)

    api_s = auth(student)
    full = api_s.get(f"/api/tests/{test.id}/full/").data
    assert full["id"] == test.id

    payload = {
        "test_id": test.id,
        "answers": [{"question_id": q.id, "answer_id": a_correct.id}],
    }
    r = api_s.post("/api/tests/submit/", payload, format="json")
    assert r.status_code == 200
    assert r.data["correct_answers"] == 1
    assert r.data["score_percent"] == 100.0

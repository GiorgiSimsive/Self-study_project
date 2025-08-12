from rest_framework import viewsets, status
from .models import Course, Section, Material, Test, Question, Answer
from .serializers import (
    CourseSerializer, SectionSerializer, MaterialSerializer,
    TestSerializer, QuestionSerializer, AnswerSerializer,
    TestSubmissionSerializer
)
from users.permissions import ReadOnlyOrTeacherAdmin, IsAuthenticatedStudent
from rest_framework.decorators import action
from rest_framework.response import Response


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [ReadOnlyOrTeacherAdmin]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [ReadOnlyOrTeacherAdmin]


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [ReadOnlyOrTeacherAdmin]


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [ReadOnlyOrTeacherAdmin]


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [ReadOnlyOrTeacherAdmin]


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [ReadOnlyOrTeacherAdmin]


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [ReadOnlyOrTeacherAdmin]

    @action(detail=False, methods=['post'], url_path='submit', permission_classes=[IsAuthenticatedStudent])
    def submit_test(self, request):
        serializer = TestSubmissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        test_id = serializer.validated_data['test_id']
        answers_data = serializer.validated_data['answers']

        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            return Response({"error": "Тест не найден"}, status=status.HTTP_404_NOT_FOUND)

        total_questions = test.questions.count()
        correct_count = 0

        for ans in answers_data:
            try:
                question = Question.objects.get(id=ans['question_id'], test=test)
                answer = Answer.objects.get(id=ans['answer_id'], question=question)
                if answer.is_correct:
                    correct_count += 1
            except (Question.DoesNotExist, Answer.DoesNotExist):
                continue

        result = {
            "total_questions": total_questions,
            "correct_answers": correct_count,
            "score_percent": round((correct_count / total_questions) * 100, 2) if total_questions > 0 else 0
        }

        return Response(result, status=status.HTTP_200_OK)

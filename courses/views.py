from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from users.permissions import IsAuthenticatedStudent, IsOwnerOrReadOnly, ReadOnlyOrTeacherAdmin

from .models import Answer, Course, Material, Question, Section, Test
from .serializers import (
    AnswerSerializer,
    CourseSerializer,
    MaterialSerializer,
    QuestionSerializer,
    SectionSerializer,
    TestFullSerializer,
    TestResultSerializer,
    TestSerializer,
    TestSubmissionSerializer,
)


@extend_schema_view(
    list=extend_schema(tags=["courses"], summary="Список курсов"),
    retrieve=extend_schema(tags=["courses"], summary="Курс"),
    create=extend_schema(tags=["courses"], summary="Создать курс"),
    update=extend_schema(tags=["courses"], summary="Обновить курс"),
    partial_update=extend_schema(tags=["courses"], summary="Частично обновить курс"),
    destroy=extend_schema(tags=["courses"], summary="Удалить курс"),
)
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [ReadOnlyOrTeacherAdmin, IsOwnerOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["owner__username"]
    search_fields = ["title", "description"]
    ordering_fields = ["title", "id"]


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [ReadOnlyOrTeacherAdmin, IsOwnerOrReadOnly]


class MaterialViewSet(viewsets.ModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [ReadOnlyOrTeacherAdmin, IsOwnerOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["section__course", "section"]
    search_fields = ["title", "content"]


class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [ReadOnlyOrTeacherAdmin, IsOwnerOrReadOnly]

    @extend_schema(
        tags=["tests"],
        summary="Отправить ответы на тест",
        request=TestSubmissionSerializer,
        responses={200: OpenApiResponse(response=TestResultSerializer, description="Результат проверки")},
        examples=[
            OpenApiExample(
                "Пример отправки",
                value={
                    "test_id": 1,
                    "answers": [
                        {"question_id": 5, "answer_id": 12},
                        {"question_id": 6, "answer_id": 15},
                    ],
                },
            )
        ],
    )
    @action(
        detail=False,
        methods=["post"],
        url_path="submit",
        permission_classes=[IsAuthenticatedStudent],
    )
    def submit_test(self, request):
        serializer = TestSubmissionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        test_id = serializer.validated_data["test_id"]
        answers_data = serializer.validated_data["answers"]

        try:
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            return Response({"error": "Тест не найден"}, status=status.HTTP_404_NOT_FOUND)

        total_questions = test.questions.count()
        correct_count = 0

        for ans in answers_data:
            try:
                question = Question.objects.get(id=ans["question_id"], test=test)
                answer = Answer.objects.get(id=ans["answer_id"], question=question)
                if answer.is_correct:
                    correct_count += 1
            except (Question.DoesNotExist, Answer.DoesNotExist):
                continue

        result = {
            "total_questions": total_questions,
            "correct_answers": correct_count,
            "score_percent": (round((correct_count / total_questions) * 100, 2) if total_questions > 0 else 0),
        }

        return Response(result, status=status.HTTP_200_OK)

    @extend_schema(
        tags=["tests"],
        summary="Получить тест с вопросами и вариантами",
        responses={200: TestFullSerializer},
    )
    @action(detail=True, methods=["get"], url_path="full")
    def full(self, request, pk=None):
        test = self.get_object()
        data = TestFullSerializer(test).data
        return Response(data)


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [ReadOnlyOrTeacherAdmin, IsOwnerOrReadOnly]


class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [ReadOnlyOrTeacherAdmin, IsOwnerOrReadOnly]

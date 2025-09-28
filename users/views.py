from django.contrib.auth import get_user_model
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import generics

from .serializers import RegisterSerializer

User = get_user_model()


@extend_schema(
    tags=["auth"],
    summary="Регистрация пользователя",
    description="Создаёт нового пользователя. Пароль валидируется стандартными валидаторами Django.",
    request=RegisterSerializer,
    examples=[
        OpenApiExample(
            "Пример запроса",
            value={
                "username": "student1",
                "password": "Testpass123",
                "email": "student1@mail.com",
                "first_name": "Ivan",
                "last_name": "Petrov",
                "role": "student",
            },
        ),
    ],
)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from courses.views import AnswerViewSet, CourseViewSet, MaterialViewSet, QuestionViewSet, SectionViewSet, TestViewSet
from users.views import RegisterView

router = DefaultRouter()
router.register(r"courses", CourseViewSet)
router.register(r"sections", SectionViewSet)
router.register(r"materials", MaterialViewSet)
router.register(r"tests", TestViewSet)
router.register(r"questions", QuestionViewSet)
router.register(r"answers", AnswerViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    # Регистрация
    path("api/register/", RegisterView.as_view(), name="register"),
    # JWT
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # OpenAPI Docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

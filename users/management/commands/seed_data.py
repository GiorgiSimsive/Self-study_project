from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from courses.models import Answer, Course, Material, Question, Section, Test

User = get_user_model()


class Command(BaseCommand):
    help = "Создаёт тестовые данные для демонстрации проекта"

    def handle(self, *args, **kwargs):
        admin, _ = User.objects.get_or_create(
            username="admin",
            defaults={"role": "admin", "is_staff": True, "is_superuser": True},
        )
        admin.set_password("admin123")
        admin.save()

        teacher, _ = User.objects.get_or_create(
            username="teacher1",
            defaults={"role": "teacher"},
        )
        teacher.set_password("teacher123")
        teacher.save()

        student, _ = User.objects.get_or_create(
            username="student1",
            defaults={"role": "student"},
        )
        student.set_password("student123")
        student.save()

        course, _ = Course.objects.get_or_create(
            owner=teacher, title="Курс по математике", description="Базовый курс по арифметике"
        )

        section, _ = Section.objects.get_or_create(course=course, title="Сложение чисел")

        material, _ = Material.objects.get_or_create(
            section=section, title="2+2", content="Как складывать числа: пример 2+2"
        )

        test, _ = Test.objects.get_or_create(material=material, title="Мини-тест по сложению")

        question, _ = Question.objects.get_or_create(test=test, text="Сколько будет 2+2?")

        Answer.objects.get_or_create(question=question, text="4", is_correct=True)
        Answer.objects.get_or_create(question=question, text="3", is_correct=False)
        Answer.objects.get_or_create(question=question, text="5", is_correct=False)

        self.stdout.write(self.style.SUCCESS("Тестовые данные успешно созданы!"))
        self.stdout.write(self.style.SUCCESS("Логины и пароли:"))
        self.stdout.write("admin / admin123")
        self.stdout.write("teacher1 / teacher123")
        self.stdout.write("student1 / student123")

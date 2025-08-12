from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Course(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Material(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title


class Test(models.Model):
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='tests')
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.text} ({'correct' if self.is_correct else 'wrong'})"

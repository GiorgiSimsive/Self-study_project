from rest_framework import serializers

from .models import Answer, Course, Material, Question, Section, Test


class CourseSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Course
        fields = ("id", "owner", "title", "description")


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = "__all__"


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = "__all__"


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"


class TestSubmissionSerializer(serializers.Serializer):
    test_id = serializers.IntegerField()
    answers = serializers.ListField(child=serializers.DictField(child=serializers.CharField()))


class AnswerShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ("id", "text")


class QuestionFullSerializer(serializers.ModelSerializer):
    answers = AnswerShortSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ("id", "text", "answers")


class TestFullSerializer(serializers.ModelSerializer):
    questions = QuestionFullSerializer(many=True, read_only=True)

    class Meta:
        model = Test
        fields = ("id", "title", "questions")


class TestResultSerializer(serializers.Serializer):
    total_questions = serializers.IntegerField()
    correct_answers = serializers.IntegerField()
    score_percent = serializers.FloatField()

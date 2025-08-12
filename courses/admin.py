from django.contrib import admin
from .models import Course, Section, Material, Test, Question, Answer

admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Material)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Answer)

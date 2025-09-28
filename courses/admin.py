from django.contrib import admin

from .models import Answer, Course, Material, Question, Section, Test

admin.site.register(Course)
admin.site.register(Section)
admin.site.register(Material)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Answer)

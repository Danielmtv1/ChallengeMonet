from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import StudentManager, Student, Test, Answer, Question, Nota, StudentAnswer

admin.site.register(StudentManager)
admin.site.register(Student)
admin.site.register(Test)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Nota)
admin.site.register(StudentAnswer)

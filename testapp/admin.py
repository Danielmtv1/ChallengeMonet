from django.contrib import admin

from .models import Student, Test, Answer, Question, Nota, StudentAnswer


admin.site.register(Student)
admin.site.register(Test)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Nota)
admin.site.register(StudentAnswer)

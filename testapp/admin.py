from django.contrib import admin
from .models import Student, Test, StudentAnswer, Question
from .forms import StudentForm


class StudentAdmin(admin.ModelAdmin):
    form = StudentForm
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    list_filter = ("is_active", "is_staff", "is_superuser")
    search_fields = ("email", "first_name", "last_name")
    filter_horizontal = ()
    fieldsets = (
        (
            None,
            {"fields": ("email", "password", "first_name", "last_name")},
        ),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    ordering = ("email",)


class StudentAnswerAdmin(admin.ModelAdmin):
    model = StudentAnswer
    list_display = ("id", "student", "question", "answers")

    def get_queryset(self, request):
        user = request.user.id
        if request.user.is_superuser:
            return super().get_queryset(request)
        else:
            return super().get_queryset(request).filter(student=user)


admin.site.register(Student)

admin.site.register(Test)

admin.site.register(Question)

admin.site.register(StudentAnswer, StudentAnswerAdmin)

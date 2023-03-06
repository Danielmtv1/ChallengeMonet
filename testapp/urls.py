from django.urls import include, path
from rest_framework import routers
from .views import (
    AnswerStudentViewSet,
    StudentSignupView,
)

router = routers.DefaultRouter()


urlpatterns = [
    path("student/signup/", StudentSignupView.as_view(), name="signup"),
    path(
        "student/answers/",
        AnswerStudentViewSet.as_view(),
        name="Student_Answers",
    ),
    path("", include(router.urls)),
]

from django.urls import include, path
from rest_framework import routers
from .views import (
    ActiveTestList,
    AnswerStudentViewSet,
    StudentSignupView,
    TestTakingView,
)


router = routers.DefaultRouter()


urlpatterns = [
    path("student/signup/", StudentSignupView.as_view(), name="signup"),
    path(
        "student/answers/",
        AnswerStudentViewSet.as_view(),
        name="Student Answers",
    ),
    path("tests/<int:test_id>/take/", TestTakingView.as_view(), name="Take Test"),
    path(
        "tests/",
        ActiveTestList.as_view(
            {
                "get": "list",
            }
        ),
        name="test-list",
    ),
    path("", include(router.urls)),
]

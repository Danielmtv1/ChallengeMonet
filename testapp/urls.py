from django.urls import include, path
from rest_framework import routers
from .views import (
    ActiveTestList,
    AnswerStudentViewSet,
    ProtectedView,
    StudentSignupView,
)


router = routers.DefaultRouter()

router.register(r"tests", ActiveTestList)
router.register(r"studentanswers", AnswerStudentViewSet)

urlpatterns = [
    path("student/signup/", StudentSignupView.as_view(), name="signup"),
    path("protected/", ProtectedView.as_view(), name="protected"),
    path("", include(router.urls)),
]

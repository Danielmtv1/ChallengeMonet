from django.urls import include, path
from rest_framework import routers
from . import views
from .views import (
    ActiveTestList,
    AnswerStudentViewSet,
    ProtectedView,
    StudentSignupView,
    StudentLoginView,
)


router = routers.DefaultRouter()

router.register(r"tests", ActiveTestList)
router.register(r"studentanswers", AnswerStudentViewSet)

urlpatterns = [
    path("signup/", StudentSignupView.as_view(), name="signup"),
    path("login/", StudentLoginView.as_view(), name="login"),
    path("protected/", ProtectedView.as_view(), name="protected"),
    path("my_tests/", views.viewst, name="my_tests"),
    path("", include(router.urls)),
]

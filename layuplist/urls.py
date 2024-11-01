""" URL Configuration for the layuplist app. """

from rest_framework.routers import DefaultRouter
from .views import (
    DepartmentViewSet,
    CourseViewSet,
    ReviewViewSet,
)

router = DefaultRouter()
router.register(r"departments", DepartmentViewSet)
router.register(r"courses", CourseViewSet)
router.register(r"reviews", ReviewViewSet)

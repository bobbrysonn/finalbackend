""" URL Configuration for the layuplist app. """

from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    DepartmentViewSet,
    CourseViewSet,
    CourseViewByDepartment,
    ReviewViewSet,
)

router = DefaultRouter()
router.register(r"departments", DepartmentViewSet)
router.register(r"courses", CourseViewSet)
router.register(r"reviews", ReviewViewSet)

urlpatterns = router.urls + [
    # Add additional URLs here
    path(
        "department/<str:department_short_name>/",
        CourseViewByDepartment.as_view(),
        name="courses-by-department",
    ),
]

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, DepartmentViewSet, CourseViewSet

router = DefaultRouter()
router.register(r"departments", DepartmentViewSet)
router.register(r"courses", CourseViewSet)

urlpatterns = router.urls
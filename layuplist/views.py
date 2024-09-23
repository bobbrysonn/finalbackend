from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, permissions, viewsets
from .models import Course, Department
from .serializers import (
    UserSerializer,
    DepartmentSerializer,
    CourseSerializer,
    MyTokenObtainPairSerializer,
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseViewByDepartment(generics.ListAPIView):
    serializer_class = CourseSerializer

    def get_queryset(self):
        department = self.kwargs["department_short_name"]
        print(department)
        return Course.objects.filter(department__short_name=department)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

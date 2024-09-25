from django.contrib.auth import get_user_model
from django.http import QueryDict
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from .models import Course, Department, Review, Professor
from .serializers import (
    UserSerializer,
    DepartmentSerializer,
    CourseSerializer,
    MyTokenObtainPairSerializer,
    ReviewSerializer,
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseViewByName(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        course_name = self.kwargs["course_name"]
        return Course.objects.filter(title__icontains=course_name)


class CourseViewByDepartment(generics.ListAPIView):
    """ViewSet for listing courses by department."""

    serializer_class = CourseSerializer
    queryset = Course.objects.all()


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def create(self, request, *args, **kwargs):
        # Enable request editing
        # First check whether it's dict or query dict
        if isinstance(request.data, QueryDict):
            request.data._mutable = True

        # Get the user from email
        request.data["student"] = User.objects.get(email=request.data.get("student")).id

        # Get prof name and email
        prof_name = " ".join(request.data.get("professor").split("@")[0].split(".")).title()
        prof_email = request.data.get("professor")

        # Get Course and store id in request
        course = Course.objects.filter(title__startswith=request.data.get("course")).first()
        request.data["course"] = course.id

        # Check if review is a layup and subtract or add
        layup = request.data.get("layup")
        if layup:
            course.layup += 1
        else:
            course.layup -= 1
        course.save()

        # Create prof object and store id in request
        prof, _ = Professor.objects.get_or_create(name=prof_name, email=prof_email)
        request.data["professor"] = prof.id

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

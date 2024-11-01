from django.contrib.auth import get_user_model
from django.http import QueryDict
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from .models import Course, Department, Review, Professor
from .serializers import (
    DepartmentSerializer,
    CourseSerializer,
    MyTokenObtainPairSerializer,
    ReviewSerializer,
)

# Get the current user model
# Advisable to do it this way
User = get_user_model()


class CourseViewSet(viewsets.ModelViewSet):
    """Viewset for the Course model

    Overrides `get_queryset` to allows filtering courses based on title and department
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["number"]
    ordering = ["number"]

    def get_queryset(self):
        """
        Optionally restricts the courses based on the presence
        of the `title` keyword argument
        """
        title = self.request.query_params.get("title")
        dept = self.request.query_params.get("dept")

        if title is not None:
            return Course.objects.filter(title__icontains=title)
        elif dept is not None:
            return Course.objects.filter(title__istartswith=dept)
        else:
            return Course.objects.all()


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
        prof_name = " ".join(
            request.data.get("professor").split("@")[0].split(".")
        ).title()
        prof_email = request.data.get("professor")

        # Get Course and store id in request
        course = Course.objects.filter(
            title__startswith=request.data.get("course")
        ).first()
        request.data["course"] = course.id

        # Check if review is a layup and subtract or add
        layup = request.data.get("layup")
        if layup:
            course.layup += 1
        else:
            course.layup -= 1
        course.save()

        # Create prof object and store id in request
        prof, _ = Professor.objects.get_or_create(email=prof_email)
        prof.name = prof_name
        prof.save()
        request.data["professor"] = prof.id

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def retrieve(self, request, *args, **kwargs):
        course = kwargs.get("pk")

        queryset = Review.objects.filter(course=course)

        if not queryset.exists():
            return Response(
                [],
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

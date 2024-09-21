from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Course, Department
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""

    class Meta:
        """Metadata for the UserSerializer."""

        model = User
        fields = ["id", "username"]


class CourseSerializer(serializers.ModelSerializer):
    """Serializer for the Course model."""

    class Meta:
        """Metadata for the CourseSerializer."""

        model = Course
        fields = [
            "id",
            "description",
            "distribs",
            "title",
            "layup",
            "rating",
            "url",
        ]


class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for the Department model."""

    courses = CourseSerializer(many=True)

    class Meta:
        """Metadata for the DepartmentSerializer."""

        model = Department
        fields = [
            "id",
            "short_name",
            "long_name",
            "description",
            "course_count",
            "url",
            "courses",
        ]
        read_only_fields = ("course_count",)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom TokenObtainPairSerializer to include user's name in response."""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        token["email"] = user.email
        # ...

        return token

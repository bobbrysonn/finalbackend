from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Course, Department, Review, Professor
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CourseSerializer(serializers.ModelSerializer):
    """Serializer for the Course model."""

    class Meta:
        """Metadata for the CourseSerializer."""

        model = Course
        fields = [
            "id",
            "code",
            "distribs",
            "description",
            "title",
            "layup",
            "rating",
            "url",
        ]


class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for the Department model."""

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
        ]
        read_only_fields = ("course_count",)


class DepartmentCourseSerializer(serializers.ModelSerializer):
    """Serializer for the Department model with courses."""

    courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        """Metadata for the DepartmentCourseSerializer."""

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


class ProfessorSerializer(serializers.ModelSerializer):
    """Serializer for the Professor model."""

    class Meta:
        """Metadata for the ProfessorSerializer."""

        model = Professor
        fields = ["id", "name", "email", "avg_rating"]


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for the Review model."""
    professor_name = serializers.ReadOnlyField(source="professor.name", read_only=True)

    class Meta:
        """Metadata for the ReviewSerializer."""

        model = Review
        fields = [
            "id",
            "content",
            "course",
            "course_rating",
            "layup",
            "term",
            "professor",
            "professor_name",
            "professor_rating",
            "median",
            "student",
        ]


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

""" Models for the layuplist app """

from django.contrib.auth.models import AbstractUser
from django.db import models


class Student(AbstractUser):
    """Custom user model for students"""

    email = models.EmailField(unique=True)
    graduation_year = models.IntegerField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


# Create your models here.
class Department(models.Model):
    """Model for a department"""

    short_name = models.CharField(max_length=4)
    long_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    url = models.URLField(max_length=400, null=True)

    class Meta:
        ordering = ["short_name"]

    def __str__(self):
        return self.short_name

    def course_count(self):
        return self.courses.count()


class Course(models.Model):
    department = models.ForeignKey(
        Department, related_name="courses", on_delete=models.CASCADE
    )
    code = models.CharField(max_length=400)
    title = models.CharField(max_length=400)
    description = models.TextField(blank=True, null=True)
    distribs = models.JSONField(blank=True, null=True)
    number = models.FloatField(blank=True, null=True)
    url = models.URLField(max_length=400)
    rating = models.FloatField(default=0)
    layup = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.department.short_name + " " + str(self.code)


class Professor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    avg_rating = models.FloatField(default=0)

    def __str__(self):
        return self.name


class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="reviews")
    content = models.TextField()
    layup = models.BooleanField(default=False)
    median = models.CharField(max_length=3)
    term = models.CharField(max_length=3)
    professor = models.ForeignKey(
        Professor, related_name="professors", on_delete=models.CASCADE
    )
    professor_rating = models.FloatField(default=0)
    course_rating = models.FloatField(default=0)
    student = models.ForeignKey(
        Student, related_name="students", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.professor.email)

""" Models for the layuplist app """

from django.contrib.auth.models import AbstractUser
from django.db import models


class Student(AbstractUser):
    """Custom user model for students"""

    email = models.EmailField("email_address", unique=True)
    graduation_year = models.IntegerField(null=True, blank=True)


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
    code = models.CharField(max_length=40)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    distribs = models.JSONField(blank=True, null=True)
    url = models.URLField(max_length=400)
    rating = models.FloatField(blank=True, null=True)
    layup = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.department.short_name + " " + str(self.code)


class Professor(models.Model):
    name = models.CharField(max_length=100)


class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="reviews")
    content = models.TextField()
    term = models.CharField(max_length=3)
    professor = models.ForeignKey(
        Professor, related_name="reviews", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            self.course.department.short_name
            + " "
            + str(self.course.code)
            + " "
            + str(self.rating)
            + " "
            + str(self.layup)
        )

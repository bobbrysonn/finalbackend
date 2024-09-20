from django.db import models

# Create your models here.
class Department(models.Model):
    short_name = models.CharField(max_length=4)
    long_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.short_name


class Course(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    code = models.FloatField()
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    disribs = models.JSONField(blank=True, null=True)
    url = models.URLField(max_length=200)
    rating = models.FloatField(blank=True, null=True)
    layup = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.department.short_name + " " + str(self.code)


class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content = models.TextField()
    term = models.CharField(max_length=3)
    professor = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.course.department.short_name + " " + str(self.course.code) + " " + str(self.rating) + " " + str(self.layup)

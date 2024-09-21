from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Course, Department, Review, Student


class DepartmentAdmin(admin.ModelAdmin):
    fields = [
        "short_name",
        "long_name",
        "description",
    ]
    list_display = ("short_name", "long_name", "course_name")

    def course_name(self, obj):
        return ", ".join(
            [
                course.department.short_name + " " + str(course.code)
                for course in obj.courses.all()
            ]
        )


# Register your models here.
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Student, UserAdmin)
admin.site.register([Course, Review])

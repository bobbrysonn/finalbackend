from django.core.management.base import BaseCommand, CommandError
from json import load
from layuplist.models import Course, Department, Review
import os

class Command(BaseCommand):
    help = "Populates the database with the latest info from ORC Catalog"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        SCRAPY_DIR = os.path.join(os.getcwd(), 'crawler', 'spyder')
        os.chdir(SCRAPY_DIR)

        self.stdout.write("Running Scrapy spider...")
        os.system("scrapy crawl orc" + " --logfile=orc.log")
        self.stdout.write("Running Scrapy spider complete")
        self.stdout.write("Populating database with the latest info from ORC Catalog")

        with open("full_courses.json") as f:
            courses_list = load(f)

            for dept in courses_list.keys():
                d, _ = Department.objects.get_or_create(short_name=dept)

                for course in courses_list[dept]:
                    Course.objects.get_or_create(code=str(course["code"]), title=course["course_name"], department=d, url=course["course_link"])

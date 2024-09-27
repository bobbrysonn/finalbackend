from django.core.management.base import BaseCommand, CommandError
from json import load
from layuplist.models import Course, Department, Review
import os

department_mapping = {
    "AAAS": "African and African American Studies",
    "ACAD": "Academic Skills Center",
    "AHUM": "Arts and Humanities",
    "ANTH": "Anthropology",
    "ARAB": "Arabic",
    "ARTH": "Art History",
    "ASCL": "Asian Societies, Cultures, and Languages",
    "ASTR": "Astronomy",
    "BIOL": "Biological Sciences",
    "CHEM": "Chemistry",
    "CHIN": "Chinese",
    "CLST": "Classics",
    "COCO": "College Courses",
    "COGS": "Cognitive Science",
    "COLT": "Comparative Literature",
    "COSC": "Computer Science",
    "CRWT": "Creative Writing",
    "EARS": "Earth Sciences",
    "ECON": "Economics",
    "EDUC": "Education",
    "EEER": "East European, Eurasian, and Russian Studies",
    "ENGL": "English",
    "ENGS": "Engineering Sciences",
    "FILM": "Film and Media Studies",
    "FREN": "French",
    "FRIT": "French and Italian",
    "GEOG": "Geography",
    "GERM": "German Studies",
    "GOVT": "Government",
    "GRK": "Greek",
    "HEBR": "Hebrew",
    "HIST": "History",
    "HUM": "Humanities",
    "ITAL": "Italian",
    "JAPN": "Japanese",
    "JWST": "Jewish Studies",
    "LACS": "Latin American, Latino, and Caribbean Studies",
    "LAT": "Latin",
    "LATS": "Latino Studies",
    "LING": "Linguistics",
    "MATH": "Mathematics",
    "MES": "Middle Eastern Studies",
    "MUS": "Music",
    "NAIS": "Native American and Indigenous Studies",
    "PHIL": "Philosophy",
    "PHYS": "Physics",
    "PORT": "Portuguese",
    "PSYC": "Psychological and Brain Sciences",
    "QSS": "Quantitative Social Science",
    "REL": "Religion",
    "RUSS": "Russian",
    "SART": "Studio Art",
    "SCI": "Science",
    "SOC": "Social Science",
    "SOCY": "Sociology",
    "SPAN": "Spanish",
    "SPEE": "Speech",
    "THEA": "Theater",
    "TUCK": "Tuck School of Business",
    "UKRA": "Ukrainian",
    "WGSS": "Women’s, Gender, and Sexuality Studies",
    "WRIT": "Institute for Writing and Rhetoric",
}


class Command(BaseCommand):
    help = "Populates the database with the latest info from ORC Catalog"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        SCRAPY_DIR = os.path.join(os.getcwd(), "crawler", "spyder")
        os.chdir(SCRAPY_DIR)

        self.stdout.write("Running Scrapy spider...")
        os.system("scrapy crawl orc" + " --logfile=orc.log")
        self.stdout.write("Running Scrapy spider complete")
        self.stdout.write("Populating database with the latest info from ORC Catalog")

        with open("full_courses.json") as f:
            courses_list = load(f)

            for dept in courses_list.keys():
                if len(dept) == 0:
                    d, _ = Department.objects.get_or_create(short_name="COLT")
                    d.long_name = department_mapping.get("COLT")
                else:
                    d, _ = Department.objects.get_or_create(short_name=dept)
                    d.long_name = department_mapping.get(dept)
                    d.save()

                for course in courses_list[dept]:
                    c, _ = Course.objects.get_or_create(
                        code=str(course["code"]),
                        department=d,
                        title=course["course_name"],
                        url=course["course_link"],
                    )
                    c.description = course["desc"]
                    c.number = float(course["code"].split("-")[0])
                    c.save()

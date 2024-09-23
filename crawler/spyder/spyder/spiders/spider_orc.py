"""Crawls the ORC for course information"""

from html import unescape
from json import dumps
import scrapy


class ORCSpider(scrapy.Spider):
    """Crawls the ORC for course information"""

    name = "orc"
    BASEORC = "https://dartmouth.smartcatalogiq.com"
    course_list = {}

    def start_requests(self):
        urls = [
            "https://dartmouth.smartcatalogiq.com/current/orc/departments-programs-undergraduate/"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        """Parse the main page for departments"""
        courses = []

        for department in response.xpath("//div[@id='sc-programlinks']/ul/li/p/a"):
            department_name = department.xpath("text()").get()
            department_link = self.BASEORC + department.xpath("@href").get()
            courses.append(
                {"department_name": department_name, "department_link": department_link}
            )

        with open("courses.json", "w", encoding="utf-8") as file:
            file.write(dumps(courses))

        for course in courses:
            yield scrapy.Request(
                url=course["department_link"],
                callback=self.parse_department,
                meta={"department_name": course["department_name"]},
            )

    def parse_department(self, response):
        """Parse the department page"""
        for course in response.xpath("//div[@id='sc-programlinks']/ul/li/p/a"):
            yield response.follow(
                course,
                callback=self.parse_course,
            )

    def parse_course(self, response):
        """Parse the course page"""

        for course in response.xpath("//ul[@class='sc-child-item-links']/li/a"):
            course_name = unescape(course.xpath("text()").get()).replace(
                "\xa0", " "
            )  # unescape to remove &nbsp;

            dept, class_number, *_ = course_name.split(" ")

            if dept in self.course_list:
                self.course_list[dept].append(
                    {
                        "code": class_number,
                        "course_name": course_name,
                        "course_link": self.BASEORC + course.xpath("@href").get(),
                    }
                )
            else:
                self.course_list[dept] = [
                    {
                        "code": class_number,
                        "course_name": course_name,
                        "course_link": self.BASEORC + course.xpath("@href").get(),
                    }
                ]

        with open("full_courses.json", "w", encoding="utf-8") as file:
            file.write(dumps(self.course_list))

from django.test import TestCase

from .models import Project


class ProjectTechnologyInputTests(TestCase):
    def test_project_technology_input_creates_technology_records(self):
        project = Project.objects.create(
            title="Portfolio Site",
            slug="portfolio-site",
            technology_input="Django, Python, PostgreSQL",
            published=True,
        )

        self.assertEqual(
            set(project.technologies.values_list("name", flat=True)),
            {"Django", "Python", "PostgreSQL"},
        )

    def test_same_technology_input_can_be_used_across_multiple_projects(self):
        first = Project.objects.create(
            title="Portfolio Site",
            slug="portfolio-site",
            technology_input="Django, Python",
            published=True,
        )
        second = Project.objects.create(
            title="Analytics Suite",
            slug="analytics-suite",
            technology_input="Django, Python",
            published=True,
        )

        self.assertEqual(set(first.technologies.values_list("name", flat=True)), {"Django", "Python"})
        self.assertEqual(set(second.technologies.values_list("name", flat=True)), {"Django", "Python"})
        self.assertEqual(first.technologies.count(), 2)
        self.assertEqual(second.technologies.count(), 2)

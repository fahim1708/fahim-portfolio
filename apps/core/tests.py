from io import BytesIO

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from apps.contact.models import ContactInfo, ContactMessage, ContactMedium
from apps.core.models import AboutItem, SiteProfile, Skill, SkillCategory, SocialLink
from apps.projects.models import Project
from apps.research.models import Research


class PublicPageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Project.objects.update_or_create(title="EventUp", defaults={"slug": "eventup", "published": True})
        Research.objects.update_or_create(
            title="Dairy Cattle Heat Detection by Dual-Camera YOLOv8 Ensemble",
            defaults={
                "slug": "dairy-cattle-heat-detection-by-dual-camera-yolov8-ensemble",
                "published": True,
            },
        )

    def test_home_page_responds_successfully(self):
        response = self.client.get(reverse("core:home"))

        self.assertEqual(response.status_code, 200)

    def test_projects_pages_respond_successfully(self):
        list_response = self.client.get(reverse("projects:list"))
        detail_response = self.client.get(reverse("projects:detail", kwargs={"slug": "eventup"}))

        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(detail_response.status_code, 200)

    def test_research_pages_respond_successfully(self):
        list_response = self.client.get(reverse("research:list"))
        detail_response = self.client.get(
            reverse(
                "research:detail",
                kwargs={"slug": "dairy-cattle-heat-detection-by-dual-camera-yolov8-ensemble"},
            )
        )

        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(detail_response.status_code, 200)

    def test_contact_form_stores_valid_message(self):
        response = self.client.post(
            reverse("core:home"),
            {
                "name": "Test Sender",
                "email": "sender@example.com",
                "message": "Hello from a test message.",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 1)


class DynamicProfileTests(TestCase):
    def make_png(self):
        image = Image.new("RGBA", (4, 4), (99, 133, 110, 180))
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        return SimpleUploadedFile("profile.png", buffer.getvalue(), content_type="image/png")

    def test_profile_content_and_transparent_image_render(self):
        profile = SiteProfile.objects.first()
        profile.name = "Admin Managed Name"
        profile.tagline = "Admin managed tagline"
        profile.profile_picture = self.make_png()
        profile.save()

        response = self.client.get(reverse("core:home"))

        self.assertContains(response, "Admin Managed Name")
        self.assertContains(response, "Admin managed tagline")
        self.assertContains(response, "/media/profile/")

    def test_active_about_items_are_dynamic(self):
        AboutItem.objects.create(title="Location", value="Dhaka", display_order=10)
        AboutItem.objects.create(title="Hidden", value="Do not show", is_active=False)

        response = self.client.get(reverse("core:home"))

        self.assertContains(response, "Location")
        self.assertContains(response, "Dhaka")
        self.assertNotContains(response, "Do not show")

    def test_empty_skill_category_is_hidden(self):
        soft_skills = SkillCategory.objects.create(
            name="Soft Skills", slug="soft-skills", display_order=20
        )

        response = self.client.get(reverse("core:home"))
        self.assertNotContains(response, "Soft Skills")

        Skill.objects.create(name="Communication", category=soft_skills)
        response = self.client.get(reverse("core:home"))
        self.assertContains(response, "Soft Skills")
        self.assertContains(response, "Communication")

        Skill.objects.filter(name="Communication").update(is_active=False)
        response = self.client.get(reverse("core:home"))
        self.assertNotContains(response, "Communication")

    def test_header_social_links_are_optional(self):
        response = self.client.get(reverse("core:home"))
        self.assertNotContains(response, 'href="https://github.com/example"')

        SocialLink.objects.create(platform="GitHub", url="https://github.com/example")
        SocialLink.objects.create(platform="LinkedIn", url="https://linkedin.com/in/example")
        response = self.client.get(reverse("core:home"))
        self.assertContains(response, "github.com/example")
        self.assertContains(response, "linkedin.com/in/example")

    def test_social_font_awesome_markup_renders_in_header_and_contact(self):
        SocialLink.objects.create(
            platform="GitHub",
            url="https://github.com/example",
            icon_url_from_font_awesome='<i class="fa-brands fa-github"></i>',
        )

        response = self.client.get(reverse("core:home"))

        self.assertContains(response, 'class="fa-brands fa-github"')
        self.assertContains(response, "social-row")
        self.assertContains(response, '<span>F</span><small>ahim</small>')
        rendered = response.content.decode()
        self.assertGreater(rendered.find("social-row"), rendered.find('id="contact"'))

    def test_contact_information_uses_typed_links_and_visibility(self):
        ContactInfo.objects.create(
            medium=ContactMedium.EMAIL,
            value="hello@example.com",
            icon='<i class="fa-regular fa-envelope"></i>',
        )
        ContactInfo.objects.create(medium=ContactMedium.PHONE, value="+880 1234", is_active=False)

        response = self.client.get(reverse("core:home"))

        self.assertContains(response, "mailto:hello@example.com")
        self.assertContains(response, 'class="fa-regular fa-envelope"')
        self.assertContains(response, "Email")
        self.assertNotContains(response, "+880 1234")

    def test_admin_can_manage_profile_and_content_models(self):
        user_model = get_user_model()
        user = user_model.objects.create_superuser(
            username="admin", email="admin@example.com", password="strong-test-password"
        )
        self.client.force_login(user)

        for model_name in ("siteprofile", "aboutitem", "skillcategory"):
            response = self.client.get(f"/admin/core/{model_name}/")
            self.assertEqual(response.status_code, 200)

        response = self.client.get("/admin/contact/contactinfo/")
        self.assertEqual(response.status_code, 200)

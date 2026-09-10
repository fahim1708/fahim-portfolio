from django.contrib import messages
from django.db.models import Prefetch
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import TemplateView

from apps.contact.forms import ContactMessageForm
from apps.contact.models import ContactInfo
from apps.core.models import AboutItem, SiteProfile, Skill, SkillCategory
from apps.experience.models import Certification, Education, Experience
from apps.projects.models import Project
from apps.research.models import Research


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = SiteProfile.objects.filter(is_active=True).first()
        skill_categories = SkillCategory.objects.filter(is_active=True).prefetch_related(
            Prefetch("skills", queryset=Skill.objects.filter(is_active=True))
        )
        context.update(
            {
                "profile": profile,
                "page_title": f"{profile.name} | {profile.professional_title}" if profile else "Md. Naimuzzaman Fahim | Software Engineer",
                "meta_description": profile.tagline if profile and profile.tagline else "Md. Naimuzzaman Fahim is a Software Engineer focused on web applications, backend systems, APIs, AI-powered applications, and data-driven solutions.",
                "about_items": AboutItem.objects.filter(is_active=True),
                "skill_categories": skill_categories,
                "experiences": Experience.objects.prefetch_related("technologies"),
                "education_items": Education.objects.all(),
                "certifications": Certification.objects.all(),
                "featured_projects": Project.objects.filter(published=True, featured=True).prefetch_related("technologies")[:3],
                "featured_research": Research.objects.filter(published=True, featured=True).prefetch_related("technologies")[:3],
                "contact_info": ContactInfo.objects.filter(is_active=True),
                "contact_form": ContactMessageForm(),
            }
        )
        return context

    def post(self, request, *args, **kwargs):
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks. Your message has been sent.")
            return redirect(f"{reverse('core:home')}#contact")

        context = self.get_context_data(**kwargs)
        context["contact_form"] = form
        messages.error(request, "Please check the highlighted fields and try again.")
        return self.render_to_response(context)


def page_not_found(request, exception):
    return render(request, "404.html", status=404)


def robots_txt(request):
    lines = [
        "User-agent: *",
        "Allow: /",
        f"Sitemap: {request.build_absolute_uri(reverse('core:sitemap'))}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def sitemap_xml(request):
    base_url = request.build_absolute_uri("/")[:-1]
    static_paths = [
        reverse("core:home"),
        reverse("projects:list"),
        reverse("research:list"),
    ]
    project_paths = [project.get_absolute_url() for project in Project.objects.filter(published=True)]
    research_paths = [
        reverse("research:detail", kwargs={"slug": item.slug})
        for item in Research.objects.filter(published=True)
    ]
    urls = static_paths + project_paths + research_paths
    body = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path in urls:
        body.append(f"  <url><loc>{base_url}{path}</loc></url>")
    body.append("</urlset>")
    return HttpResponse("\n".join(body), content_type="application/xml")

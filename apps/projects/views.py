from django.views.generic import DetailView, ListView

from .models import Project


class ProjectListView(ListView):
    model = Project
    template_name = "projects/project_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        return Project.objects.filter(published=True).prefetch_related("technology_entries__technology", "feature_images")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Projects"
        context["meta_description"] = "Selected software engineering, backend, web, AI, and data projects by Md. Naimuzzaman Fahim."
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = "projects/project_detail.html"
    context_object_name = "project"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Project.objects.filter(published=True).prefetch_related("technology_entries__technology", "feature_images")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.object
        context["page_title"] = project.title
        context["meta_description"] = project.short_description or f"{project.title} by Md. Naimuzzaman Fahim."
        return context

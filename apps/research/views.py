from django.views.generic import DetailView, ListView

from .models import Research


class ResearchListView(ListView):
    model = Research
    template_name = "research/research_list.html"
    context_object_name = "research_items"

    def get_queryset(self):
        return Research.objects.filter(published=True).prefetch_related("technologies")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Research"
        context["meta_description"] = "Research work by Md. Naimuzzaman Fahim across intelligent systems, AI, data, and software engineering."
        return context


class ResearchDetailView(DetailView):
    model = Research
    template_name = "research/research_detail.html"
    context_object_name = "research"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Research.objects.filter(published=True).prefetch_related("technologies")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item = self.object
        context["page_title"] = item.title
        context["meta_description"] = item.abstract or f"{item.title} by Md. Naimuzzaman Fahim."
        return context

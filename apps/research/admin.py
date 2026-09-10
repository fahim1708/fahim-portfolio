from django.contrib import admin

from .models import Research


@admin.register(Research)
class ResearchAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "featured", "published")
    list_editable = ("featured", "published")
    list_filter = ("featured", "published", "date")
    search_fields = ("title", "abstract", "methodology", "results", "contribution")
    ordering = ("-date", "title")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "date"
    filter_horizontal = ("technologies",)
    fieldsets = (
        ("Core", {"fields": ("title", "slug", "date", "technologies")}),
        ("Content", {"fields": ("abstract", "methodology", "results", "contribution")}),
        ("Media", {"fields": ("image",)}),
        ("Links", {"fields": ("publication_url", "github_url")}),
        ("Publishing", {"fields": ("featured", "published")}),
    )

from django.contrib import admin

from .models import Project, ProjectImage, ProjectTechnology, Technology


class ProjectTechnologyInline(admin.TabularInline):
    model = ProjectTechnology
    extra = 1
    fields = ("technology", "display_order", "is_active")
    ordering = ("display_order", "id")


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ("image", "alt_text", "display_order", "is_active")
    ordering = ("display_order", "id")


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "display_order")
    list_editable = ("display_order",)
    list_filter = ("category",)
    search_fields = ("name", "icon")
    ordering = ("display_order", "name")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = (ProjectTechnologyInline, ProjectImageInline)
    list_display = (
        "title",
        "category",
        "featured",
        "published",
        "start_date",
        "end_date",
        "display_order",
        "updated_at",
    )
    list_editable = ("featured", "published", "display_order")
    list_filter = ("category", "featured", "published", "start_date", "end_date")
    search_fields = ("title", "short_description", "detailed_description")
    ordering = ("display_order", "title")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "created_at"
    filter_horizontal = ("technologies",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Core", {"fields": ("title", "slug", "category")}),
        ("Content", {"fields": ("short_description", "detailed_description")}),
        ("Media", {"fields": ("thumbnail", "featured_image")}),
        ("Links", {"fields": ("github_url", "live_url")}),
        ("Timeline", {"fields": ("start_date", "end_date")}),
        ("Publishing", {"fields": ("featured", "published", "display_order")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

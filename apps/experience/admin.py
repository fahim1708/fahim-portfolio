from django.contrib import admin

from .models import Certification, Education, Experience


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = (
        "job_title",
        "company",
        "employment_type",
        "location",
        "start_date",
        "end_date",
        "is_featured",
        "display_order",
    )
    list_editable = ("is_featured", "display_order")
    list_filter = ("employment_type", "is_featured", "start_date", "end_date")
    search_fields = ("job_title", "company", "location", "description", "responsibilities")
    ordering = ("display_order", "-start_date")
    date_hierarchy = "start_date"
    filter_horizontal = ("technologies",)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("degree", "institution", "field", "start_date", "end_date", "grade", "display_order")
    list_editable = ("display_order",)
    list_filter = ("institution", "start_date", "end_date")
    search_fields = ("institution", "degree", "field", "grade", "description")
    ordering = ("display_order", "-start_date")
    date_hierarchy = "start_date"


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = (
        "certificate_name",
        "issuing_organization",
        "issue_date",
        "expiration_date",
        "display_order",
    )
    list_editable = ("display_order",)
    list_filter = ("issuing_organization", "issue_date", "expiration_date")
    search_fields = (
        "certificate_name",
        "issuing_organization",
        "credential_id",
        "credential_url",
    )
    ordering = ("display_order", "-issue_date", "certificate_name")
    date_hierarchy = "issue_date"

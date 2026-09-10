from django.contrib import admin
from django.utils.html import format_html

from .models import AboutItem, Resume, SiteProfile, Skill, SkillCategory, SocialLink


@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "professional_title", "is_active", "updated_at")
    list_editable = ("is_active",)
    search_fields = ("name", "professional_title", "tagline", "about_description")
    fieldsets = (
        ("Identity", {"fields": ("name", "profile_picture", "profile_picture_preview", "professional_title")}),
        ("Homepage content", {"fields": ("tagline", "about_headline", "about_description")}),
        ("Footer", {"fields": ("footer_message",)}),
        ("Publishing", {"fields": ("is_active", "updated_at")}),
    )
    readonly_fields = ("updated_at", "profile_picture_preview")

    @admin.display(description="Profile picture")
    def profile_picture_preview(self, obj):
        if not obj.profile_picture:
            return "No image"
        return format_html('<img src="{}" width="120" style="height:auto;" />', obj.profile_picture.url)


@admin.register(AboutItem)
class AboutItemAdmin(admin.ModelAdmin):
    list_display = ("title", "value", "is_active", "display_order")
    list_editable = ("is_active", "display_order")
    list_filter = ("is_active",)
    search_fields = ("title", "value", "icon")
    ordering = ("display_order", "title")


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "display_order")
    list_editable = ("is_active", "display_order")
    list_filter = ("is_active",)
    search_fields = ("name", "slug")
    ordering = ("display_order", "name")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "proficiency", "is_active", "is_featured", "display_order")
    list_editable = ("is_active", "is_featured", "display_order")
    list_filter = ("category", "is_active", "is_featured")
    search_fields = ("name", "icon", "proficiency")
    ordering = ("display_order", "name")


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("platform", "url", "icon_url_from_font_awesome", "is_active", "display_order")
    list_editable = ("is_active", "display_order")
    list_filter = ("is_active",)
    search_fields = ("platform", "url", "icon_url_from_font_awesome")
    ordering = ("display_order", "platform")


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("version", "file", "is_active", "uploaded_at")
    list_editable = ("is_active",)
    list_filter = ("is_active", "uploaded_at")
    search_fields = ("version", "file")
    ordering = ("-uploaded_at",)
    date_hierarchy = "uploaded_at"
    readonly_fields = ("uploaded_at",)

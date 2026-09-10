from django.contrib import admin

from .models import ContactInfo, ContactMessage


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ("display_label", "medium", "value", "icon", "is_active", "display_order")
    list_editable = ("is_active", "display_order")
    list_filter = ("medium", "is_active")
    search_fields = ("value", "icon")
    ordering = ("display_order", "medium")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at", "is_read")
    list_editable = ("is_read",)
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "message")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    readonly_fields = ("name", "email", "message", "created_at")

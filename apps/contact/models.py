from django.db import models


class ContactMedium(models.TextChoices):
    EMAIL = "email", "Email"
    PHONE = "phone", "Phone"


class ContactInfo(models.Model):
    medium = models.CharField(max_length=32, choices=ContactMedium.choices)
    value = models.CharField(max_length=240)
    icon = models.CharField(
        max_length=180,
        blank=True,
        help_text='Paste Font Awesome markup, for example: <i class="fa-regular fa-envelope"></i>',
    )
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "medium"]
        verbose_name = "contact information"
        verbose_name_plural = "contact information"

    @property
    def display_label(self):
        return self.get_medium_display()

    @property
    def icon_markup(self):
        return self.icon

    @property
    def href(self):
        if self.medium == ContactMedium.EMAIL:
            return f"mailto:{self.value}"
        if self.medium == ContactMedium.PHONE:
            return f"tel:{self.value.replace(' ', '')}"
        return self.value

    def __str__(self):
        return f"{self.get_medium_display()}: {self.value}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} <{self.email}>"

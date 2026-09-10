from django.db import models


class SiteProfile(models.Model):
    name = models.CharField(max_length=180)
    profile_picture = models.ImageField(upload_to="profile/", blank=True)
    professional_title = models.CharField(max_length=160, default="Software Engineer")
    tagline = models.TextField(blank=True)
    about_headline = models.CharField(max_length=220, blank=True)
    about_description = models.TextField(blank=True)
    footer_message = models.CharField(max_length=240, blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_active", "-updated_at"]
        verbose_name = "site profile"
        verbose_name_plural = "site profile"

    def save(self, *args, **kwargs):
        if self.is_active:
            SiteProfile.objects.exclude(pk=self.pk).filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class AboutItem(models.Model):
    title = models.CharField(max_length=120)
    value = models.TextField()
    icon = models.CharField(max_length=120, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "title"]

    def __str__(self):
        return self.title


class SkillCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=110, unique=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name_plural = "skill categories"

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=120, unique=True)
    category = models.ForeignKey(SkillCategory, on_delete=models.PROTECT, related_name="skills")
    icon = models.CharField(max_length=120, blank=True)
    proficiency = models.CharField(max_length=80, blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name


class SocialLink(models.Model):
    platform = models.CharField(max_length=80)
    url = models.URLField()
    icon_url_from_font_awesome = models.CharField(
        max_length=180,
        blank=True,
        verbose_name="Icon URL from Font Awesome",
        help_text='Paste Font Awesome markup, for example: <i class="fa-brands fa-github"></i>',
    )
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "platform"]

    def __str__(self):
        return self.platform


class Resume(models.Model):
    file = models.FileField(upload_to="resumes/")
    version = models.CharField(max_length=80)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ["-uploaded_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["is_active"],
                condition=models.Q(is_active=True),
                name="only_one_active_resume",
            )
        ]

    def save(self, *args, **kwargs):
        if self.is_active:
            Resume.objects.exclude(pk=self.pk).filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        status = "active" if self.is_active else "inactive"
        return f"{self.version} ({status})"

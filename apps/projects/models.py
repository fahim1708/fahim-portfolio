from django.db import models
from django.urls import reverse


class TechnologyCategory(models.TextChoices):
    PROGRAMMING = "programming", "Programming"
    BACKEND = "backend", "Backend"
    DATABASE = "database", "Database"
    AI_DATA = "ai_data", "AI & Data"
    DEVELOPMENT_TOOLS = "development_tools", "Development Tools"
    FRONTEND = "frontend", "Frontend"
    MOBILE = "mobile", "Mobile"


class Technology(models.Model):
    name = models.CharField(max_length=120, unique=True)
    icon = models.CharField(max_length=120, blank=True)
    category = models.CharField(max_length=32, choices=TechnologyCategory.choices)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name_plural = "technologies"

    def __str__(self):
        return self.name


class ProjectCategory(models.TextChoices):
    WEB_APPLICATION = "web_application", "Web Application"
    AI_DATA = "ai_data", "AI & Data"
    MOBILE_APPLICATION = "mobile_application", "Mobile Application"
    RESEARCH = "research", "Research"
    OTHER = "other", "Other"


class Project(models.Model):
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True)
    short_description = models.CharField(max_length=260, blank=True)
    detailed_description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to="projects/thumbnails/", blank=True)
    featured_image = models.ImageField(upload_to="projects/featured/", blank=True)
    category = models.CharField(max_length=32, choices=ProjectCategory.choices, blank=True)
    technology_input = models.CharField(
        max_length=500,
        blank=True,
        help_text="Enter technologies separated by commas, e.g. Django, Python, PostgreSQL",
    )
    technologies = models.ManyToManyField(Technology, blank=True, related_name="projects")
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "title"]

    def __str__(self):
        return self.title

    @property
    def ordered_technologies(self):
        return self.technology_entries.select_related("technology").order_by("display_order", "id")

    def get_absolute_url(self):
        return reverse("projects:detail", kwargs={"slug": self.slug})

    def sync_technologies(self):
        if not self.technology_input:
            self.technologies.clear()
            return

        names = []
        for raw_name in self.technology_input.split(","):
            cleaned = raw_name.strip()
            if cleaned:
                names.append(cleaned)

        if not names:
            self.technologies.clear()
            return

        technology_objects = []
        for name in names:
            technology, _ = Technology.objects.get_or_create(
                name=name,
                defaults={"category": TechnologyCategory.PROGRAMMING, "display_order": 0},
            )
            technology_objects.append(technology)

        self.technologies.set(technology_objects)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.sync_technologies()


class ProjectTechnology(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="technology_entries")
    technology = models.ForeignKey(Technology, on_delete=models.CASCADE, related_name="project_entries")
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "id"]
        verbose_name = "project technology"
        verbose_name_plural = "project technologies"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.project.technologies.add(self.technology)

    def delete(self, *args, **kwargs):
        project = self.project
        technology = self.technology
        super().delete(*args, **kwargs)
        project.technologies.remove(technology)

    def __str__(self):
        return f"{self.project.title} - {self.technology.name}"


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="feature_images")
    image = models.ImageField(upload_to="projects/features/")
    alt_text = models.CharField(max_length=180, blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "id"]
        verbose_name = "project feature image"
        verbose_name_plural = "project feature images"

    def __str__(self):
        return f"{self.project.title} image {self.display_order}"

from django.db import models


class Research(models.Model):
    title = models.CharField(max_length=220)
    slug = models.SlugField(max_length=240, unique=True)
    abstract = models.TextField(blank=True)
    methodology = models.TextField(blank=True)
    results = models.TextField(blank=True)
    contribution = models.TextField(blank=True)
    image = models.ImageField(upload_to="research/", blank=True)
    technologies = models.ManyToManyField("projects.Technology", blank=True, related_name="research_items")
    publication_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    date = models.DateField(blank=True, null=True)
    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=False)

    class Meta:
        ordering = ["-date", "title"]
        verbose_name_plural = "research"

    def __str__(self):
        return self.title

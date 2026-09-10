from django.db import models


class EmploymentType(models.TextChoices):
    FULL_TIME = "full_time", "Full-Time"
    PART_TIME = "part_time", "Part-Time"
    CONTRACT = "contract", "Contract"
    INTERNSHIP = "internship", "Internship"
    FREELANCE = "freelance", "Freelance"
    RESEARCH = "research", "Research"


class Experience(models.Model):
    job_title = models.CharField(max_length=160)
    company = models.CharField(max_length=160)
    location = models.CharField(max_length=160, blank=True)
    employment_type = models.CharField(max_length=32, choices=EmploymentType.choices, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    responsibilities = models.TextField(blank=True)
    technologies = models.ManyToManyField("projects.Technology", blank=True, related_name="experiences")
    display_order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)

    class Meta:
        ordering = ["display_order", "-start_date"]

    def __str__(self):
        return f"{self.job_title} at {self.company}"


class Education(models.Model):
    institution = models.CharField(max_length=180)
    degree = models.CharField(max_length=180)
    field = models.CharField(max_length=180, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    grade = models.CharField(max_length=80, blank=True)
    description = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "-start_date"]
        verbose_name_plural = "education"

    def __str__(self):
        return f"{self.degree}, {self.institution}"


class Certification(models.Model):
    certificate_name = models.CharField(max_length=180)
    issuing_organization = models.CharField(max_length=180)
    issue_date = models.DateField(blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    credential_id = models.CharField(max_length=120, blank=True)
    credential_url = models.URLField(blank=True)
    certificate_image = models.ImageField(upload_to="certifications/", blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "-issue_date", "certificate_name"]

    def __str__(self):
        return self.certificate_name

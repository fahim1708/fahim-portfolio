from .models import Resume, SiteProfile, SocialLink


def portfolio_globals(request):
    return {
        "active_resume": Resume.objects.filter(is_active=True).first(),
        "social_links": SocialLink.objects.filter(is_active=True),
        "header_social_links": SocialLink.objects.filter(
            is_active=True,
            platform__iregex=r"^(github|linkedin)$",
        ),
        "active_profile": SiteProfile.objects.filter(is_active=True).first(),
    }

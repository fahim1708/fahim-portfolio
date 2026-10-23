from .models import Resume, SiteProfile, SocialLink


def portfolio_globals(request):
    if getattr(request, "defer_portfolio_data", False):
        return {
            "active_resume": None,
            "social_links": (),
            "header_social_links": (),
            "active_profile": None,
        }

    return {
        "active_resume": Resume.objects.filter(is_active=True).first(),
        "social_links": SocialLink.objects.filter(is_active=True),
        "header_social_links": SocialLink.objects.filter(
            is_active=True,
            platform__iregex=r"^(github|linkedin)$",
        ),
        "active_profile": SiteProfile.objects.filter(is_active=True).first(),
    }

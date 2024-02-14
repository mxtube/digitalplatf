from .models import SiteSettings, Department


def load_settings(request):
    return {'site_settings': SiteSettings.load()}


def departments(request):
    """
    The context for the base.
    Drop-down list of academic buildings menu categories of class schedules.
    :return: list with all department objects
    """
    return {'departments': Department.objects.all()}
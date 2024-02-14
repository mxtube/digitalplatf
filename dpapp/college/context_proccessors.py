from .models import SiteSettings, Department


def load_settings(request):
    """
    The context with the site settings for the database.
    Returns a list with objects.
    :param request:
    :return:
    """
    return {'site_settings': SiteSettings.load()}


def departments(request):
    """
    The context for the base.
    Drop-down list of academic buildings menu categories of class schedules.
    :param request:
    :return: list with all department objects
    """
    return {'departments': Department.objects.all()}
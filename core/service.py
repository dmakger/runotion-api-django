from django.db.models import QuerySet, Count

from core.models import ImportanceLevel, Color
# from project.models import Project, SectionProject


def get_most_important():
    return ImportanceLevel.objects.order_by('-value').first()


def get_color(index: int, colors=None):
    if colors is None:
        colors: list[Color] = list(Color.objects.all().order_by('pk'))
    if not colors:
        return None
    return colors[index % len(colors)]


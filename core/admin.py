from django.contrib import admin

from core.models import ImportanceLevel, Color


#  Уровень важности
class ImportanceLevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'value', 'id']


class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'value', 'id']


admin.site.register(ImportanceLevel, ImportanceLevelAdmin)
admin.site.register(Color, ColorAdmin)

from django.contrib import admin

from core.models import ImportanceLevel


#  Уровень важности
class ImportanceLevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'value']


admin.site.register(ImportanceLevel, ImportanceLevelAdmin)

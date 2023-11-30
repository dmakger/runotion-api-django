from django.db.models import QuerySet


# Удаляет все пустые данные из filter_data
def get_filter_data(filter_data=None):
    if not filter_data:
        return {}

    new_data = {}
    for key, value in filter_data.items():
        if key and value:
            new_data[key] = value
    return new_data


# Возвращает queryset по модели и filter_data
def get_records_from_model(model, filter_data=None, default=None) -> QuerySet:
    updated_filter_data = get_filter_data(filter_data)
    if updated_filter_data:
        return model.objects.filter(**updated_filter_data)
    if default is None:
        return model.objects.all()
    return default


# Возвращает queryset по queryset и filter_data
def get_records_from_queryset(queryset: QuerySet, filter_data=None, default=None) -> QuerySet:
    updated_filter_data = get_filter_data(filter_data)
    if updated_filter_data:
        return queryset.filter(**updated_filter_data)
    if default is None:
        return queryset
    return default



# Получение родительского queryset
def get_parents_records(queryset: QuerySet, model, data: list) -> QuerySet:
    unique_ids = queryset.values_list(*data, flat=True).distinct()
    return model.objects.filter(id__in=unique_ids)

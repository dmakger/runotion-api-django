from django.db import models


#  Получение максимальной позиции
def get_max_position(qs):
    return qs.aggregate(models.Max('position'))['position__max']


#  Получение минимальной позиции
def get_min_position(qs):
    return qs.aggregate(models.Min('position'))['position__min']


# Получение новой позиции
def get_new_position(qs, position):
    if position is None or position == '':
        return len(qs) + 1
    return position


# Исправление всех позиций в qs
def fix_positions(qs):
    position = 1
    for item in qs:
        if item.position != position:
            item.position = position
            item.save(update_fields=['position'])
        position += 1

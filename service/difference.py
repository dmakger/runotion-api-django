import datetime


class DifferenceKeys:
    WITHOUT = 'without'
    LESS = 'sm'
    LARGE = 'lg'
    EQUAL = 'e'
    BETWEEN = 'between'

    # Получение всех значений
    def vars(self):
        return [value for name, value in vars(self.__class__).items() if not name.startswith('_')]


# Создает ключ относительно DifferenceKeys
def creation_key(key=None, digits: list = None, is_equal=False):
    if key is None or key == DifferenceKeys.WITHOUT or key not in DifferenceKeys().vars() \
            or (digits is None or len(digits) == 0):
        return DifferenceKeys.WITHOUT

    if key == DifferenceKeys.BETWEEN:
        return f"{key}{digits[0]}_{digits[1]}"
    if key == DifferenceKeys.EQUAL:
        return f"{key}{digits[0]}"
    equal = DifferenceKeys.EQUAL if is_equal else ''
    return f"{key}{equal}{digits[0]}"


def get_all_keys():
    return {
        DifferenceKeys.WITHOUT: 0,
        creation_key(DifferenceKeys.LESS, [10]): 0,
        creation_key(DifferenceKeys.BETWEEN, [10, 20]): 0,
        creation_key(DifferenceKeys.LARGE, [20]): 0,
    }


def calculate_days(completed_at=None, deadline_at=None):
    if completed_at is None:
        return DifferenceKeys.WITHOUT
    if deadline_at is None:
        deadline_at = datetime.datetime.now()
    difference = completed_at - deadline_at
    days_difference = difference.days

    if days_difference <= 0:
        return DifferenceKeys.WITHOUT
    elif days_difference < 10:
        return creation_key(DifferenceKeys.LESS, [10])
    elif 10 <= days_difference < 20:
        return creation_key(DifferenceKeys.BETWEEN, [10, 20])
    return creation_key(DifferenceKeys.LARGE, [20])

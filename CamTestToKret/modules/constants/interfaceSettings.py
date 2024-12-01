from modules.filters.lowPassFilter import low_pass_filter_gaussian,low_pass_filter_mean, low_pass_filter_box,low_pass_filter_bilateral,low_pass_filter_furie,low_pass_filter_wiener,low_pass_filter_morf_smooth,low_pass_filter_bessel
from modules.filters.hightPassFilter import high_pass_filter_laplacian,high_pass_filter_gradient, high_pass_filter_sobel, high_pass_filter_unsharp_mask
# лучше поменять подход - много мест где надо дублировать/ошибаемся
# +псомотреть как работают импорт файлы чтоб тут избавится от полотна импортов
#не забывать докидывать модули
filter_map = {
    # Низкочастотные фильтры
    "Гауссовый фильтр": (low_pass_filter_gaussian, {'kernel_size': 5}),
    "Среднее значение": (low_pass_filter_mean, {'kernel_size': 3}),
    "Билатеральный фильтр": (low_pass_filter_bilateral, {'diameter': 9, 'sigmaColor': 75, 'sigmaSpace': 75}),
    "Блочный фильтр": (low_pass_filter_box, {'kernel_size': 5}),
    "Винеровский фильтр": (low_pass_filter_wiener, {'kernel_size': 5}),
    "Фурье-фильтр": (low_pass_filter_furie, {'cutoff': 9}),
    "Морфологическое сглаживание": (low_pass_filter_morf_smooth, {'kernel_size': 5}),
    "Бесселев фильтр": (low_pass_filter_bessel, {'cutoff': 5}),

    # Высокочастотные фильтры
    "Лапласиан": (high_pass_filter_laplacian, {'kernel_size': 3}),
    "Собель": (high_pass_filter_sobel, {'kernel_size': 3}),
    "Unsharp Masking": (high_pass_filter_unsharp_mask, {'sigma': 1.0, 'strength': 1.5}),
    "Градиентный фильтр": (high_pass_filter_gradient, {'kernel_size': 3}),
}
# затычка селектов под вильтры
filter_names = ["НЧ фильтр", "ВЧ фильтр", "Полосовой фильтр", "Сегментация"]

# Опции фильтров для выпадающего списка (можно переделать под ключи объекта )
filter_options =  {
    "НЧ фильтр": [
        "Гауссовый фильтр",
        "Среднее значение",
        "Билатеральный фильтр",
        "Блочный фильтр",
        "Винеровский фильтр",
        "Фурье-фильтр",
        "Морфологическое сглаживание",
        "Бесселев фильтр"
    ],
    "ВЧ фильтр": [
        "Лапласиан",
        "Собель",
        "Unsharp Masking",
        "Градиентный фильтр"
    ],
    "Полосовой фильтр": [
       "Затычка ",
        "Затычка ",
    ],
     "Сегментация": [
     "Затычка "
    ]
}
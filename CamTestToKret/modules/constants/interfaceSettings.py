from modules.filters.lowPassFilter import low_pass_filter_gaussian, low_pass_filter_mean, low_pass_filter_bilateral
from modules.filters.hightPassFilter import high_pass_filter_laplacian, high_pass_filter_sobel, high_pass_filter_unsharp_mask

#не забывать докидывать модули

filter_map = {
    "НЧ фильтрация 1": (low_pass_filter_gaussian, {'kernel_size': 5}),
    "НЧ фильтрация 2": (low_pass_filter_mean, {'kernel_size': 3}),
    "НЧ фильтрация 3": (low_pass_filter_bilateral, {'diameter': 9, 'sigmaColor': 75, 'sigmaSpace': 75}),

    "ВЧ фильтрация 1": (high_pass_filter_laplacian, {'kernel_size': 3}),
    "ВЧ фильтрация 2": (high_pass_filter_sobel, {'kernel_size': 3}),
    "ВЧ фильтрация 3": (high_pass_filter_unsharp_mask, {'sigma': 1.0, 'strength': 1.5}),
}
# затычка селектов под вильтры
filter_names = ["НЧ фильтр", "ВЧ фильтр", "Полосовой фильтр", "Сегментация"]

# Опции фильтров для выпадающего списка (можно переделать под ключи объекта )
filter_options = {
    "НЧ фильтр": ["НЧ фильтрация 1", "НЧ фильтрация 2", "НЧ фильтрация 3"],
    "ВЧ фильтр": ["ВЧ фильтрация 1", "ВЧ фильтрация 2", "ВЧ фильтрация 3"],
    "Полосовой фильтр": ["Полосовая фильтрация 1", "Полосовая фильтрация 2"],
    "Сегментация": ["Сегментация 1", "Сегментация 2"]
}
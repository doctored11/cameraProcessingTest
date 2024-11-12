def initialize_active_filters():
    return {}

def update_filter_parameters(active_filters):
    for filter_name, filter_data in active_filters.items():
        params = {}
        for param, input_field in filter_data['params'].items():
            try:
                params[param] = float(input_field.text())
            except ValueError:
                print(f"👨‍🦼‍➡️ неверные параметры '{param}' для фильтра '{filter_name}'.")
                params[param] = float(input_field.placeholderText())
        active_filters[filter_name]['current_params'] = params
    return active_filters

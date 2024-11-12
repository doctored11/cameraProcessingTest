from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QCheckBox, QLineEdit, QPushButton, QSpacerItem, QSizePolicy, QFrame
from modules.constants.interfaceSettings import filter_map, filter_options, filter_names
from modules.constants.styleConstants import BUTTON_STYLE, FILTER_CARD_STYLE, CHECKBOX_STYLE, HEADER_LABEL_STYLE, NUMBER_LABEL_STYLE
from modules.constants.interfaceSettings import filter_options
def create_filter_dropdown(parent, filter_names, on_change_callback):
    layout = QVBoxLayout(parent)
    for filter_name in filter_names:
        combo = QComboBox(parent)
        combo.addItem(filter_name)
        combo.addItems(filter_options[filter_name])
        combo.setStyleSheet(BUTTON_STYLE)
        combo.currentIndexChanged.connect(lambda index, combo=combo: on_change_callback(combo.currentText()))
        layout.addWidget(combo)
    return layout


def create_placeholder_buttons(parent, callback):
    layout = QVBoxLayout()
    row_layout = QHBoxLayout()

    for i in range(4):
        button = QPushButton(f"Заглушка {i + 1}", parent)
        button.setStyleSheet(BUTTON_STYLE)
        button.clicked.connect(lambda _, b=i + 1: callback(b))

        row_layout.addWidget(button)

        if (i + 1) % 2 == 0:
            layout.addLayout(row_layout)
            row_layout = QHBoxLayout()

    if row_layout.count() > 0:
        layout.addLayout(row_layout)

    return layout


def create_update_button(parent, callback):
    update_button = QPushButton("Обновить", parent)
    update_button.setStyleSheet(BUTTON_STYLE)
    update_button.clicked.connect(callback)
    return update_button

def create_filter_card(filter_name, filter_count, filter_function, params):
    filter_frame = QFrame()
    filter_frame.setFrameShape(QFrame.StyledPanel)
    filter_frame.setStyleSheet(FILTER_CARD_STYLE)
    filter_frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

    # Верхняя строка с названием фильтра
    layout = QVBoxLayout(filter_frame)
    layout.setContentsMargins(4, 4, 4, 4)

    header_layout = QHBoxLayout()
    header_layout.setContentsMargins(0, 0, 0, 0)
    header_layout.setSpacing(5)

    number_label = QLabel(f"#{filter_count}")
    number_label.setStyleSheet(NUMBER_LABEL_STYLE)
    header_layout.addWidget(number_label)

    name_label = QLabel(filter_name)
    name_label.setStyleSheet(HEADER_LABEL_STYLE)
    header_layout.addWidget(name_label)
    layout.addLayout(header_layout)

    filter_inputs = {}
    controls_layout = QHBoxLayout()
    controls_layout.setContentsMargins(0, 0, 0, 0)
    controls_layout.setSpacing(4)

    for param, value in params.items():
        input_field = QLineEdit()
        input_field.setPlaceholderText(param)
        input_field.setFixedWidth(60)
        input_field.setStyleSheet("border: 1px solid lightgray; padding: 2px; ")
        input_field.setText(str(value))
        controls_layout.addWidget(input_field)
        filter_inputs[param] = input_field

    checkbox = QCheckBox("Вкл.")
    checkbox.setStyleSheet(CHECKBOX_STYLE)
    controls_layout.addWidget(checkbox)

    layout.addLayout(controls_layout)
    filter_frame.setLayout(layout)

    return filter_frame, filter_inputs, checkbox
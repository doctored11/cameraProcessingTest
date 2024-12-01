import sys
import cv2
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QComboBox, QCheckBox, QLineEdit, QPushButton, QHBoxLayout, QScrollArea, \
    QWidget, QSpacerItem, QSizePolicy, QFrame, QGridLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from modules.camScript import Camera, wait_for_camera
from modules.getHist import initialize_histogram_plot, display_frame_with_histogram
from modules.filters.lowPassFilter import low_pass_filter_gaussian, low_pass_filter_mean, low_pass_filter_bilateral
from modules.constants.interfaceSettings import filter_map, filter_options, filter_names
from modules.view.filterHandler import initialize_active_filters, update_filter_parameters
from modules.view.uiElements import create_filter_dropdown, create_placeholder_buttons, create_update_button, create_filter_card
from modules.constants.styleConstants import  BUTTON_STYLE, FILTER_CARD_STYLE, CHECKBOX_STYLE, HEADER_LABEL_STYLE, NUMBER_LABEL_STYLE
from modules.cameraApp import CameraApp

# Влады́ко Христе́ Бо́же, И́же страстьми́ Свои́ми стра́сти моя́ исцели́вый и я́звами Свои́ми я́звы моя́ уврачева́вый,
# да́руй мне́, мно́го Тебе́ прегреши́вшему, сле́зы умиле́ния; сраствори́ моему́ те́лу от обоня́ния Животворя́щаго Те́ла Твоего́,
# и наслади́ ду́шу мою́ Твое́ю Честно́ю Кро́вию от го́рести, е́юже мя́ сопроти́вник напои́; возвы́си мо́й у́м к Тебе́,
# до́лу пони́кший, и возведи́ от про́пасти поги́бели: я́ко не и́мам покая́ния, не и́мам умиле́ния, не и́мам сле́зы уте́шительныя,
# возводя́щия ча́да ко своему́ насле́дию. Омрачи́хся умо́м в жите́йских страсте́х, не могу́ воззре́ти к Тебе́ в боле́зни,
# не могу́ согре́тися слеза́ми, я́же к Тебе́ любве́. Но, Влады́ко Го́споди Иису́се Христе́, сокро́вище благи́х,
# да́руй мне́ покая́ние всеце́лое и се́рдце люботру́дное во взыска́ние Твое́,
# да́руй мне́ благода́ть Твою́ и обнови́ во мне́ зра́ки Твоего́ о́браза.
# Оста́вих Тя́, не оста́ви мене́; изы́ди на взыска́ние мое́, возведи́ к па́жити Твое́й и сопричти́ мя́ овца́м избра́ннаго Твоего́ ста́да,
# воспита́й мя́ с ни́ми от зла́ка Боже́ственных Твои́х Та́инств, моли́твами Пречи́стыя Твоея́ Ма́тере и все́х святы́х Твои́х.
# Ами́нь.


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1796, 811)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.active_filters = initialize_active_filters()
        main_layout = QtWidgets.QHBoxLayout(self.centralwidget)

        # левая панель с кнопками  - todo (сделать ее выпадающей с боку)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setFixedWidth(291)
        self.frame_2.setStyleSheet("background-color: rgba(165, 165, 165, 155);")
        left_layout = create_filter_dropdown(self.frame_2, filter_names, self.on_filter_selected)

        # пустота между кнопками верхними и нижн
        left_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Кнопки-заглушки в два ряда
        placeholder_buttons = create_placeholder_buttons(self.frame_2, lambda b: print(f"Нажата кнопка Заглушка {b}"))
        left_layout.addLayout(placeholder_buttons)


        # Кнопка "Обновить"
        update_button = create_update_button(self.frame_2, self.update_active_filters)
        left_layout.addWidget(update_button)

        # цнтральная область для видео и фильтров
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        center_layout = QVBoxLayout(self.widget1)


        self.video_label = QLabel(self.widget1)
        self.video_label.setFixedSize(640, 480)
        center_layout.addWidget(self.video_label)

        # Прокручиваемая область для выбранных фильтров
        filter_scroll_area = QScrollArea()
        filter_scroll_area.setWidgetResizable(True)
        filter_widget = QWidget()
        self.filter_container = QGridLayout(filter_widget)
        filter_scroll_area.setWidget(filter_widget)
        center_layout.addWidget(filter_scroll_area)

        # Правая панель с вкладками
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)

        # Вкладка для гистограммы [сделать ее только по запросу]
        self.tab = QtWidgets.QWidget()
        self.tab.layout = QVBoxLayout(self.tab)
        self.fig, self.ax, self.line_r, self.line_g, self.line_b = initialize_histogram_plot()
        self.canvas = FigureCanvas(self.fig)
        self.tab.layout.addWidget(self.canvas)
        self.tabWidget.addTab(self.tab, "Гистограмма")

        # Вторая вкладка для другого отображения
        self.tab_2 = QtWidgets.QWidget()
        self.graphicsView_3 = QtWidgets.QGraphicsView(self.tab_2)
        self.tab_2.layout = QVBoxLayout(self.tab_2)

        self.video_label_2 = QLabel(self.widget1)
        self.video_label_2.setFixedSize(640, 480)
        self.tab_2.layout.addWidget(self.video_label_2)

        # self.tab_2.layout.addWidget(self.graphicsView_3)
        self.tabWidget.addTab(self.tab_2, "Доп. вкладка")


        main_layout.addWidget(self.frame_2)
        main_layout.addWidget(self.widget1, 7)
        main_layout.addWidget(self.tabWidget, 7)

        # Устанавливаем центральный виджет
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Счетчик для нумерации фильтров
        self.filter_count = 1

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "🫐 - Camera (Test)"))

    def on_filter_selected(self, filter_name, combo_box):
        if combo_box.currentIndex() == 0:
            return

        print(f"Выбран фильтр: {filter_name}")

        if filter_name in filter_map:
            unique_filter_id = f"{filter_name}_{self.filter_count}"

            filter_function, params = filter_map[filter_name]
            filter_card, filter_inputs, checkbox = create_filter_card(
                filter_name,
                self.filter_count,
                filter_function,
                params,
                lambda: self.deactivate_filter(unique_filter_id)

            )

            self.active_filters[unique_filter_id] = {
                'function': filter_function,
                'params': filter_inputs,
                'checkbox': checkbox,

            }

            row = (self.filter_count - 1) // 3
            col = (self.filter_count - 1) % 3
            self.filter_container.addWidget(filter_card, row, col)
            self.filter_count += 1

        combo_box.setCurrentIndex(0)

    def update_active_filters(self):
        self.active_filters = update_filter_parameters(self.active_filters)

        print("🫐 Обновленные фильтры:", self.active_filters)

    def deactivate_filter(self, filter_id):
        if filter_id in self.active_filters:
            del self.active_filters[filter_id]
            print(f"Фильтр {filter_id} деактивирован")




def create_interface():
    app = QtWidgets.QApplication(sys.argv)
    window = CameraApp( Ui_MainWindow())
    window.show()
    sys.exit(app.exec_())


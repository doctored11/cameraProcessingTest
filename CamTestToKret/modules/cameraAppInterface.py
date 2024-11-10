import sys
import cv2
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QComboBox, QCheckBox, QLineEdit, QPushButton, QHBoxLayout, QScrollArea, \
    QWidget, QSpacerItem, QSizePolicy, QFrame, QGridLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from modules.camScript import Camera, wait_for_camera
from modules.getHist import initialize_histogram_plot, display_frame_with_histogram
from modules.filters.lowPassFilter import low_pass_filter_gaussian, low_pass_filter_mean, low_pass_filter_bilateral



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


        main_layout = QtWidgets.QHBoxLayout(self.centralwidget)

        # левая панель с кнопками  - todo (сделать ее выпадающей с боку)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setFixedWidth(291)
        self.frame_2.setStyleSheet("background-color: rgba(165, 165, 165, 155);")
        left_layout = QVBoxLayout(self.frame_2)


    #объект под все фильтры - вынести потом в константы
        #наверное ввести диапозон чисел и типы (а то где то есть ограничения ядер и прочего)
        self.filter_map = {
            "НЧ фильтрация 1": (low_pass_filter_gaussian, {'kernel_size': 5}),
            "НЧ фильтрация 2": (low_pass_filter_mean, {'kernel_size': 3}),
            "НЧ фильтрация 3": (low_pass_filter_bilateral, {'diameter': 9, 'sigmaColor': 75, 'sigmaSpace': 75}),

            # и тд
        }

        # затычка селектов под вильтры
        filter_names = ["НЧ фильтр", "ВЧ фильтр", "Полосовой фильтр", "Сегментация"]
        filter_options = {
            "НЧ фильтр": ["НЧ фильтрация 1", "НЧ фильтрация 2","НЧ фильтрация 3"],
            "ВЧ фильтр": ["ВЧ фильтрация 1", "ВЧ фильтрация 2"],
            "Полосовой фильтр": ["Полосовая фильтрация 1", "Полосовая фильтрация 2"],
            "Сегментация": ["Сегментация 1", "Сегментация 2"]
        }

        self.active_filters = {}

        for filter_name in filter_names:
            combo = QComboBox(self.frame_2)
            combo.addItem(filter_name)
            combo.addItems(filter_options[filter_name])
            combo.setStyleSheet("""
                padding: 6px 10px;
                border: 2px solid;
                border-radius: 4px;
                border-color: rgb(25, 17, 117);
                background-color: rgb(25, 18, 83);
                color: rgb(232, 232, 232);
            """)
            combo.currentIndexChanged.connect(lambda index, combo=combo: self.on_filter_selected(combo.currentText()))
            left_layout.addWidget(combo)

        # пустота между кнопками верхними и нижн
        left_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Кнопки-заглушки в два ряда
        button_layout = QHBoxLayout()
        for i in range(4):
            button = QPushButton(f"Заглушка {i + 1}", self.frame_2)
            button.setStyleSheet("""
                padding: 6px 10px;
                border: 2px solid;
                border-radius: 4px;
                border-color: rgb(25, 17, 117);
                background-color: rgb(25, 18, 83);
                color: rgb(232, 232, 232);
            """)
            button.clicked.connect(lambda _, b=i + 1: print(f"Нажата кнопка Заглушка {b}"))
            if i % 2 == 0 and i > 0:
                left_layout.addLayout(button_layout)
                button_layout = QHBoxLayout()
            button_layout.addWidget(button)

        left_layout.addLayout(button_layout)


        # Кнопка "Обновить"
        update_button = QPushButton("Обновить", self.frame_2)
        update_button.setStyleSheet("""
                   padding: 6px 10px;
                   border: 2px solid;
                   border-radius: 4px;
                   border-color: rgb(25, 17, 117);
                   background-color: rgb(25, 18, 83);
                   color: rgb(232, 232, 232);
               """)
        update_button.clicked.connect(self.update_active_filters)
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

    def on_filter_selected(self, filter_name):
        #Todo - в будущем разбить этого мутанта и вынести все в файлы
        # Создаем карточку фильтра с полями только если фильтр есть в filter_map
        print(filter_name)
        if filter_name in self.filter_map:
            filter_function, params = self.filter_map[filter_name]
            filter_frame = QFrame()
            filter_frame.setFrameShape(QFrame.StyledPanel)
            filter_frame.setStyleSheet("""
                background-color: #F5F5F5;
                border: 2px solid rgb(25, 17, 117);
                border-radius: 6px;
                padding: 8px;
                max-width: 280px;
                min-width: 100px;
            """)
            filter_frame.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

            # Layout карточки
            layout = QVBoxLayout(filter_frame)
            layout.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
            layout.setContentsMargins(4, 4, 4, 4)

            # Верхняя строка с названием фильтра
            header_layout = QHBoxLayout()
            header_layout.setContentsMargins(0, 0, 0, 0)
            header_layout.setSpacing(5)

            number_label = QLabel(f"#{self.filter_count}")
            number_label.setStyleSheet("color: orange; font-weight: bold;border:0;")
            header_layout.addWidget(number_label)

            name_label = QLabel(filter_name)
            name_label.setStyleSheet("color: rgb(25, 18, 83); font-weight: bold;border:0;")
            header_layout.addWidget(name_label)
            layout.addLayout(header_layout)

            filter_inputs = {}

            # Нижняя строка с параметрами, только если фильтр существует в filter_map
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
            checkbox.setStyleSheet("border: 0; margin-left: 6px;")
            controls_layout.addWidget(checkbox)

            layout.addLayout(controls_layout)
            filter_frame.setLayout(layout)

            self.active_filters[filter_name] = {'function': filter_function, 'params': filter_inputs,
                                                'checkbox': checkbox}

            row = (self.filter_count - 1) // 3
            col = (self.filter_count - 1) % 3
            self.filter_container.addWidget(filter_frame, row, col)

            # счетчик для нумерации [ todo изменить логику]
            self.filter_count += 1

    def update_active_filters(self):

        for filter_name, filter_data in self.active_filters.items():


            params = {}
            for param, input_field in filter_data['params'].items():
                try:
                    #тут подумать - не всегда работает запасное знач
                    params[param] = float(input_field.text())
                except ValueError:

                    print(
                        f"Некорректное значение для параметра '{param}' в фильтре '{filter_name}', используется значение по умолчанию.")
                    params[param] = float(input_field.placeholderText())
            self.active_filters[filter_name]['current_params'] = params
            print(f"Активный фильтр: {filter_name}, параметры: {params}")





class CameraApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_camera()
        self.update_video()

    def init_camera(self):
        self.camera = Camera(index=0, width=640, height=480)
        wait_for_camera(self.camera)

    # def update_video(self):
    #     frame = self.camera.get_frame()
    #     frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #
    #
    #     display_frame_with_histogram(frame, self.line_r, self.line_g, self.line_b)
    #     self.canvas.draw()
    #
    #
    #     height, width, channel = frame_rgb.shape
    #     bytes_per_line = 3 * width
    #     qt_img = QtGui.QImage(frame_rgb.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
    #     self.video_label.setPixmap(QtGui.QPixmap.fromImage(qt_img))
    #     #потом проходиться по активным фильтрам и выводить Todo! !TODO
    #     # todo тут проходиться по всем активным фильтрам - если их ключ есть в объекте то применить нужный фильтр и вывести измененную картинку
    #     self.video_label_2.setPixmap(QtGui.QPixmap.fromImage(qt_img))
    #
    #
    #     QtCore.QTimer.singleShot(10, self.update_video)

    def update_video(self):
        #почистить!
        frame = self.camera.get_frame()
        processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


        for filter_name, filter_data in self.active_filters.items():
            if filter_data['checkbox'].isChecked() and filter_data.get('current_params') is not None:
                filter_function = filter_data['function']
                params = filter_data['current_params']


                if 'kernel_size' in params and isinstance(params['kernel_size'], float):
                    params['kernel_size'] = int(params['kernel_size'])

                try:

                    processed_frame = filter_function(processed_frame, **params)
                except Exception as e:
                    print(f"Ошибка применения фильтра '{filter_name}': {e}")


        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        qt_img_original = QtGui.QImage(frame.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
        self.video_label.setPixmap(QtGui.QPixmap.fromImage(qt_img_original))


        qt_img_processed = QtGui.QImage(processed_frame.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
        self.video_label_2.setPixmap(QtGui.QPixmap.fromImage(qt_img_processed))


        QtCore.QTimer.singleShot(10, self.update_video)

    def closeEvent(self, event):
        self.camera.release()
        cv2.destroyAllWindows()
        event.accept()


def create_interface():
    app = QtWidgets.QApplication(sys.argv)
    window = CameraApp()
    window.show()
    sys.exit(app.exec_())

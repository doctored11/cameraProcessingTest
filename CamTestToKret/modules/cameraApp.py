from PyQt5 import QtWidgets, QtGui, QtCore
import cv2
from modules.camScript import Camera, wait_for_camera
from modules.view.filterHandler import initialize_active_filters, update_filter_parameters


class CameraApp(QtWidgets.QMainWindow):
    def __init__(self, ui_main_window):
        super().__init__()
        self.ui = ui_main_window
        self.ui.setupUi(self)
        self.init_camera()
        self.update_video()

    def init_camera(self):
        self.camera = Camera(index=1, width=640, height=480)
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
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        processed_frame = frame


        for filter_name, filter_data in self.ui.active_filters.items():
            if filter_data['checkbox'].isChecked() and filter_data.get('current_params') is not None:
                filter_function = filter_data['function']
                params = filter_data['current_params']


                if 'kernel_size' in params and isinstance(params['kernel_size'], float):
                    params['kernel_size'] = int(params['kernel_size'])

                try:

                    processed_frame = filter_function(processed_frame, **params)
                except Exception as e:
                    print(f"🛑 Ошибка применения фильтра '{filter_name}': {e}")


        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        qt_img_original = QtGui.QImage(frame.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
        self.ui.video_label.setPixmap(QtGui.QPixmap.fromImage(qt_img_original))


        qt_img_processed = QtGui.QImage(processed_frame.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
        self.ui.video_label_2.setPixmap(QtGui.QPixmap.fromImage(qt_img_processed))


        QtCore.QTimer.singleShot(10, self.update_video)

    def closeEvent(self, event):
        self.camera.release()
        cv2.destroyAllWindows()
        event.accept()

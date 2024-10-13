import cv2
import threading

class Camera:
    def __init__(self, index=0, width=640, height=480):

        self.index = index
        self.width = width
        self.height = height
        self.cap = None
        self.ready = False
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self.initialize_camera)
        self.thread.start()

    def initialize_camera(self):

        with self.lock:
            self.cap = cv2.VideoCapture(self.index)
            if not self.cap.isOpened():
                raise Exception(f"Не удалось открыть камеру   {self.index}")
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
            self.ready = True
            print(f"камера инициализирована: {self.index}: {self.width}x{self.height}")

    def get_frame(self):

        if not self.ready:
            raise Exception("Камера  не готова")

        with self.lock:
            ret, frame = self.cap.read()
            if not ret:
                raise Exception("Не удалось получить кадр с камеры")
            return frame

    def release(self):

        with self.lock:
            if self.cap is not None:
                self.cap.release()
                self.cap = None
                print("камера освобождена #camFREE")

import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from modules.camScript import Camera, wait_for_camera
from modules.getHist import initialize_histogram_plot, display_frame_with_histogram


def dummy_action():
    print("Кнопка нажата")


def on_closing(root, camera):
    camera.release()
    cv2.destroyAllWindows()
    root.destroy()


def update_video(camera, video_label, line_r, line_g, line_b, canvas):
    frame = camera.get_frame()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    display_frame_with_histogram(frame, line_r, line_g, line_b)
    canvas.draw()

    img = Image.fromarray(frame_rgb)
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)

    video_label.after(10, update_video, camera, video_label, line_r, line_g, line_b, canvas)


def create_interface():
    root = tk.Tk()
    root.title("интерфейс 🫐")
    root.geometry("1200x700")

    camera = Camera(index=0, width=640, height=480)
    wait_for_camera(camera)

    left_frame = tk.Frame(root)
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    video_frame = tk.Frame(left_frame)
    video_frame.pack(fill=tk.BOTH, expand=True)

    video_label = tk.Label(video_frame)
    video_label.pack()


    controls_frame = tk.Frame(left_frame)
    controls_frame.pack(fill=tk.X, pady=10)


#Пока просто заглушку - по месту смотрю
    buttons = [
        "НЧ фильтрация", "ВЧ фильтрация", "Полосовая фильтрация",
        "Цифровое растяжение", "Цифровой кроп", "Сегментация",
        "Распознавание объектов", "Отслеживание движущихся объектов",
        "Сохранить фотографию", "Сохранить видео"
    ]

    for text in buttons:
        btn = ttk.Button(controls_frame, text=text, command=dummy_action)
        btn.pack(fill=tk.X, pady=5)

    close_button = ttk.Button(controls_frame, text="Закрыть", command=lambda: on_closing(root, camera))
    close_button.pack(fill=tk.X, pady=10)

    right_frame = tk.Frame(root)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    fig, ax, line_r, line_g, line_b = initialize_histogram_plot()
    canvas = FigureCanvasTkAgg(fig, master=right_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    update_video(camera, video_label, line_r, line_g, line_b, canvas)

    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root, camera))
    root.mainloop()


create_interface()

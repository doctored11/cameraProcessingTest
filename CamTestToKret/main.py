import cv2

import matplotlib.pyplot as plt
from modules.camScript import Camera, wait_for_camera
from modules.getHist import compute_histogram, initialize_histogram_plot, update_histogram_plot, display_frame_with_histogram
from modules.filters.lowPassFilter import low_pass_filter_gaussian,low_pass_filter_mean, low_pass_filter_bilateral
#и тд - можно в класс обернуть чтобы не тянуть простыню

def main():
    camera = Camera(index=0, width=720, height=560)
    wait_for_camera(camera)

    fig, ax, line_r, line_g, line_b = initialize_histogram_plot()

    try:
        while True:
            # тут жизненный цикл, тут не срать - 1-2 строки под вызов функций(пока отключаем комментарием))


            frame = camera.get_frame()
            cv2.imshow("Напрямую с камеры", frame)

            display_frame_with_histogram(frame, line_r, line_g, line_b)

            # Пример вызова функций фильтрации (Функция не реализованна)
            # filtered_frame = low_pass_filter(frame, параметры )
            # cv2.imshow("Фильтрованное", filtered_frame)






            #
            #
            #

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        camera.release()
        cv2.destroyAllWindows()
        plt.ioff()

if __name__ == "__main__":
    main()

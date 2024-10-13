import cv2
import time
from modules.camScript import Camera
from modules.getHist import compute_histogram, initialize_histogram_plot, update_histogram_plot

def main():
    camera = Camera(index=1, width=240, height=280)

    try:
        while not camera.ready:
            print("Камера  не готова, ждем...")
            time.sleep(5)

        fig, ax, line_r, line_g, line_b = initialize_histogram_plot()

        while True:
            frame = camera.get_frame()
            histograms = compute_histogram(frame)

            cv2.imshow('#11 testCamFrame', frame)

            update_histogram_plot(line_r, line_g, line_b, histograms)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f" ошибка: {e}")
    finally:
        camera.release()
        cv2.destroyAllWindows()
        plt.ioff()

if __name__ == "__main__":
    main()

from tkinter import *
from tkinter import messagebox

import cv2


cap = cv2.VideoCapture(0)

while True:
   ret, img = cap.read()
   cv2.imshow("video", img)
   if cv2.waitKey(10) == 27:
       break

cap.release()
cv2.destroyAllWindows()

def clicked():
    messagebox.showinfo('Ошибка', 'Не подключено')


window = Tk()
window.title("Биг квестчен")
window.geometry('1080x720')
lbl = Label(window, text = "Рабочие кнопочки ну почти...", font=("Times New Roman", 14))
lbl.grid(column=0, row=0)
lbl.place(x=750, y=35)
lbl1 = Label(window, text = "Должно быть видево", font=("Times New Roman", 14))
lbl1.grid(column=0, row=0)
lbl1.place(x=250, y=35)
btn1 = Button(window, text="НЧФ",font=("Times New Roman", 14), command = clicked)
btn1.grid(column=0, row=0)
btn1.place(x=750, y= 60)
#txt = Entry(window,width=10)(непонятно надо оно или не надо)
#txt.grid(column=2, row=0)
btn2 = Button(window, text="Сохранить фото",font=("Times New Roman", 14), command = clicked)
btn2.grid(column=0, row=0)
btn2.place(x=150, y= 550)
btn3 = Button(window, text="Сохранить видео",font=("Times New Roman", 14), command = clicked)
btn3.grid(column=0, row=0)
btn3.place(x=350, y= 550)
btn4 = Button(window, text="ВЧФ",font=("Times New Roman", 14), command = clicked)
btn4.grid(column=0, row=0)
btn4.place(x=950, y= 60)
window.mainloop()
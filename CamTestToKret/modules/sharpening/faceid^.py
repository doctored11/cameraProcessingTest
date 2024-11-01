from tkinter import *
from tkinter import messagebox

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
btn = Button(window, text="НЧФ",font=("Times New Roman", 14), command = clicked)
btn.grid(column=0, row=0)
btn.place(x=750, y= 60)
#txt = Entry(window,width=10)(непонятно надо оно или не надо)
#txt.grid(column=2, row=0)
btn = Button(window, text="Сохранить фото",font=("Times New Roman", 14), command = clicked)
btn.grid(column=0, row=0)
btn.place(x=150, y= 550)
btn = Button(window, text="Сохранить видео",font=("Times New Roman", 14), command = clicked)
btn.grid(column=0, row=0)
btn.place(x=350, y= 550)
btn = Button(window, text="ВЧФ",font=("Times New Roman", 14), command = clicked)
btn.grid(column=0, row=0)
btn.place(x=950, y= 60)
window.mainloop()
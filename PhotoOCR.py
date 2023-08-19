import pytesseract
import customtkinter
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

customtkinter.set_appearance_mode("light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("1100x500")
app.title("Распознаватор")

window = customtkinter.CTk()
window.geometry("350x400")
window.title("Настройки")


def show_image():
    photo_lbl = tk.Label(app)
    filename = filedialog.askopenfilename()
    image = Image.open(filename)
    resize_image = image.resize((400, 300))
    img = ImageTk.PhotoImage(resize_image)
    photo_lbl.configure(image=img)
    photo_lbl.image = img
    photo_lbl.place(x=90, y=100, width=400, height=300)


def open_txt():
    text_file = open('recognized.txt', 'r', encoding='utf-8')
    stuff = text_file.read()
    textbox.insert(END, stuff)
    text_file.close()


def start_recognition():
    filename = filedialog.askopenfilename()
    text = pytesseract.image_to_string(filename)
    with open('recognized.txt', mode='w', encoding='utf-8') as file:
        file.write(text)


def tools():
    window.mainloop()


main_frame1 = customtkinter.CTkFrame(master=window, width=700, height=150)
main_frame1.pack(pady=10, padx=10, fill="both", expand=True)

label_text1 = customtkinter.CTkLabel(master=app, text="Распознавание текста с изображений", font=("Helvetica", 16))
label_text1.place(x=360, y=10)

label_text2 = customtkinter.CTkLabel(master=main_frame1, text="Настройки изображения", font=("Helvetica", 16))
label_text2.place(x=70, y=10)

label_text3 = customtkinter.CTkLabel(master=main_frame1, text="Грамматика", font=("Helvetica", 16))
label_text3.place(x=100, y=130)

label_text4 = customtkinter.CTkLabel(master=main_frame1, text="Язык распознавания", font=("Helvetica", 16))
label_text4.place(x=80, y=280)

frame_photo = customtkinter.CTkFrame(master=app, width=350, height=260)
frame_photo.place(x=57, y=70)

textbox = customtkinter.CTkTextbox(master=app, width=450, height=260)
textbox.place(x=600, y=70)

recognize_btn = customtkinter.CTkButton(master=app, text="Распознать", command=start_recognition)
recognize_btn.place(x=160, y=340)

showtext_btn = customtkinter.CTkButton(app, text="Показать текст", command=open_txt)
showtext_btn.place(x=750, y=340)

photo_btn = customtkinter.CTkButton(app, text="Выбрать Фото", command=show_image)
photo_btn.place(x=160, y=180)

tools_btn = customtkinter.CTkButton(app, text="⚙", font=("Arial", 20, "bold"), command=tools)
tools_btn.place(x=950, y=10)

switch_1 = customtkinter.CTkSwitch(master=main_frame1, text="Извлекать шумы")
switch_1.place(x=20, y=50)

switch_2 = customtkinter.CTkSwitch(master=main_frame1, text="Извлекать зернистость")
switch_2.place(x=20, y=90)

radiobutton_var = customtkinter.IntVar(value=1)

radiobutton_1 = customtkinter.CTkRadioButton(master=main_frame1, text="English", variable=radiobutton_var, value=1)
radiobutton_1.place(x=200, y=320)

radiobutton_2 = customtkinter.CTkRadioButton(master=main_frame1, text="Русский", variable=radiobutton_var, value=2)
radiobutton_2.place(x=50, y=320)

checkbox_1 = customtkinter.CTkCheckBox(master=main_frame1, text="Точки")
checkbox_1.place(x=10, y=170)

checkbox_2 = customtkinter.CTkCheckBox(master=main_frame1, text="Запятые")
checkbox_2.place(x=10, y=210)

checkbox_3 = customtkinter.CTkCheckBox(master=main_frame1, text="Абзац")
checkbox_3.place(x=180, y=170)

checkbox_4 = customtkinter.CTkCheckBox(master=main_frame1, text="Правописание")
checkbox_4.place(x=180, y=210)


app.mainloop()

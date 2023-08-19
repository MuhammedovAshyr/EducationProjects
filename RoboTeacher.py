import os
import customtkinter
import requests
import json
import pyaudio
import wave
import pyttsx3
import speech_recognition as speech_r
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from googletrans import Translator

customtkinter.set_appearance_mode("light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("1100x700")
app.title("Робот-учитель 3000")

CHUNK = 1024  # определяет форму аудио сигнала
FRT = pyaudio.paInt16  # шестнадцатибитный формат задает значение амплитуды
CHAN = 1  # канал записи звука
RT = 44100  # частота
REC_SEC = 5  # длина записи
OUTPUT = "output.wav"

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
# voices[0] - мужской голос
# voices[1] - женский голос


def set_start_rate():
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate-100)


set_start_rate()


def speak(text):
    engine.say(text, "text")
    engine.runAndWait()


def play_file():
    with open("recognized.txt", "r") as file:
        text = file.read()
        speak(text)


def translate_text(text, dest='en'):
    translator = Translator()
    translation = translator.translate(text, dest=dest)
    return translation.text


def save_to_file(text, file_path='recognized.txt'):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)


def open_text():
   file_text = open("user.txt", "r", encoding="utf-8")
   stuff = file_text.read()
   user_text_box.insert(END, stuff)
   file_text.close()


def save_text():
   file_path = "user.txt"
   with open(file_path, "w", encoding="utf-8") as file_text:
       file_text.write(user_text_box.get(1.0, "end-1c"))

   with open(file_path, "r", encoding="utf-8") as file_text:
       text = file_text.read()

   translator = Translator()
   translation = translator.translate(text, dest='en')
   print(f'Перевод текста на английский: "{translation.text}"')

   query = translation.text.replace(" ", "+")
   text_to_translate = f"{translation.text}"
   translated_text = translate_text(text_to_translate)
   file_path = "recognized.txt"
   save_to_file(translated_text, file_path)

   api_key = "AIzaSyCQpbvkcOYRhF5q2FrDNE3iz6maBpqnZUY"
   cx = "210a48a0109f044d0"
   search_url = "https://www.googleapis.com/customsearch/v1"

   headers = {
       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                     "AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/58.0.3029.110 Safari/537.3"}

   params = {
       "key": api_key,
       "cx": cx,
       "q": query,
       "searchType": "image",
       "num": 5,
   }

   response = requests.get(search_url, headers=headers, params=params)

   results = json.loads(response.text)

   if "items" in results:
       images = results["items"]
       for i, image in enumerate(images):
           url = image["link"]
           response = requests.get(url, headers=headers)
           with open(f"photo{i + 1}.jpg", "wb") as f:
               f.write(response.content)
               print(f"Сохранено изображение {i + 1}")
   else:
       print("Изображения не найдены")


def microphone():
    p = pyaudio.PyAudio()

    stream = p.open(format=FRT, channels=CHAN, rate=RT, input=True,
                    frames_per_buffer=CHUNK)  # открываем поток для записи
    frames = []  # формируем выборку данных фреймов
    for i in range(0, int(RT / CHUNK * REC_SEC)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()  # останавливаем и закрываем поток
    stream.close()
    p.terminate()

    w = wave.open(OUTPUT, 'wb')
    w.setnchannels(CHAN)
    w.setsampwidth(p.get_sample_size(FRT))
    w.setframerate(RT)
    w.writeframes(b''.join(frames))
    w.close()

    sample = speech_r.WavFile('C:\\Users\\Ashyr\\PycharmProjects\\Mazurov\\output.wav')

    r = speech_r.Recognizer()

    with sample as audio:
        content = r.record(audio)
        r.adjust_for_ambient_noise(audio)

    user_audio_file = speech_r.AudioFile("output.wav")
    with user_audio_file as source:
        user_audio = r.record(source)
    text = r.recognize_google(user_audio, language='ru-RU')
    with open('recognized.txt', mode='w', encoding='utf-8') as file:
        file.write(text)
    translator = Translator()
    slovo = translator.translate(text, dest='en')
    print(f'Вы сказали: "{text}"')
    print("-")
    print(f'Перевожу на английский: "{slovo.text}"')
    print("-")

    query = slovo.text.replace(" ", "+")
    text_to_translate = f"{slovo.text}"
    translated_text = translate_text(text_to_translate)
    file_path = "recognized.txt"
    save_to_file(translated_text, file_path)

    api_key = "AIzaSyCQpbvkcOYRhF5q2FrDNE3iz6maBpqnZUY"
    cx = "210a48a0109f044d0"
    search_url = "https://www.googleapis.com/customsearch/v1"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/58.0.3029.110 Safari/537.3"}

    params = {
        "key": api_key,
        "cx": cx,
        "q": query,
        "searchType": "image",
        "num": 5,
    }

    response = requests.get(search_url, headers=headers, params=params)

    results = json.loads(response.text)

    if "items" in results:
        images = results["items"]
        for i, image in enumerate(images):
            url = image["link"]
            response = requests.get(url, headers=headers)
            with open(f"photo{i + 1}.jpg", "wb") as f:
                f.write(response.content)
                print(f"Сохранено изображение {i + 1}")
    else:
        print("Изображения не найдены")


image_files = ['photo1.jpg', 'photo2.jpg', 'photo3.jpg', 'photo4.jpg', 'photo5.jpg']
current_image = 0


def change_image():
    photo_lbl = tk.Label(app)
    global current_image
    # открытие следующего изображения
    current_image = (current_image + 1) % len(image_files)
    image = Image.open(image_files[current_image])
    resize_image = image.resize((590, 300))
    img = ImageTk.PhotoImage(resize_image)
    photo_lbl.configure(image=img)
    photo_lbl.image = img
    photo_lbl.place(x=393, y=540, width=590, height=300)
    # вызов этой же функции через 10 секунд
    app.after(5000, change_image)


def show_result_text():
    photo_lbl = tk.Label(app)
    global current_image
    current_image = (current_image + 1) % len(image_files)
    image = Image.open('photo1.jpg')
    resize_image = image.resize((590, 300))
    img = ImageTk.PhotoImage(resize_image)
    photo_lbl.configure(image=img)
    photo_lbl.image = img
    photo_lbl.place(x=393, y=540, width=590, height=300)
    change_image()

    text_file = open('recognized.txt', 'r', encoding='utf-8')
    stuff = text_file.read()
    translate_box.insert(END, stuff)
    text_file.close()


def show_result_microphone():
    photo_lbl = tk.Label(app)
    image = Image.open('photo1.jpg')
    resize_image = image.resize((590, 300))
    img = ImageTk.PhotoImage(resize_image)
    photo_lbl.configure(image=img)
    photo_lbl.image = img
    photo_lbl.place(x=393, y=540, width=590, height=300)
    change_image()

    text_file = open('recognized.txt', 'r', encoding='utf-8')
    stuff = text_file.read()
    translate_box.insert(END, stuff)
    text_file.close()


def show_fullscreen():
    os.startfile('photo1.jpg')
    os.startfile('photo2.jpg')
    os.startfile('photo3.jpg')
    os.startfile('photo4.jpg')
    os.startfile('photo5.jpg')


text_frame = customtkinter.CTkFrame(master=app, width=350, height=200)
text_frame.place(x=50, y=70)

audio_frame = customtkinter.CTkFrame(master=app, width=350, height=200)
audio_frame.place(x=700, y=70)

translated_frame = customtkinter.CTkFrame(master=app, width=500, height=330)
translated_frame.place(x=300, y=360)

title_text = customtkinter.CTkLabel(master=app, text="Робот-учитель v2.0", font=("Helvetica", 16))
title_text.pack()

listen_text = customtkinter.CTkLabel(master=app, text="Прослушать:", font=("Helvetica", 16))
listen_text.place(x=90, y=420)

title_text = customtkinter.CTkLabel(master=app, text="Язык перевода:", font=("Helvetica", 16))
title_text.place(x=490, y=100)

title_text = customtkinter.CTkLabel(master=app, text="Перевести:", font=("Helvetica", 16))
title_text.place(x=510, y=290)

text_bar_text = customtkinter.CTkLabel(master=text_frame, text="Введите слово или предложение:", font=("Helvetica", 16))
text_bar_text.place(x=50, y=10)

audio_bar_text = customtkinter.CTkLabel(master=audio_frame, text="Скажите слово или предложение:", font=("Helvetica", 16))
audio_bar_text.place(x=50, y=10)

translated_bar_text = customtkinter.CTkLabel(master=translated_frame, text="Результат:", font=("Helvetica", 16))
translated_bar_text.place(x=210, y=0)

microphone_button = customtkinter.CTkButton(master=audio_frame, text="🎤", font=("Arial", 60, "bold"), command=microphone)
microphone_button.place(x=105, y=60)

show_button = customtkinter.CTkButton(master=app, text="С текста", command=show_result_text)
show_button.place(x=360, y=320)

show_button = customtkinter.CTkButton(master=app, text="С микрофона", command=show_result_microphone)
show_button.place(x=600, y=320)

open_button = customtkinter.CTkButton(master=app, text="Открыть Файл", command=open_text)
open_button.place(x=70, y=280)

save_button = customtkinter.CTkButton(master=app, text="Сохранить", command=save_text)
save_button.place(x=240, y=280)

user_text_box = customtkinter.CTkTextbox(master=text_frame, width=329, height=150, font=("Times New Roman", 30))
user_text_box.place(x=10, y=40)

translate_box = customtkinter.CTkTextbox(master=translated_frame, width=480, height=35, font=("Times New Roman", 30))
translate_box.place(x=10, y=30)

radiobutton_var = customtkinter.IntVar(value=1)

radiobutton_1 = customtkinter.CTkRadioButton(master=app, text="English", variable=radiobutton_var, value=1)
radiobutton_1.place(x=500, y=190)

radiobutton_2 = customtkinter.CTkRadioButton(master=app, text="Русский", variable=radiobutton_var, value=2)
radiobutton_2.place(x=500, y=150)

play_button = customtkinter.CTkButton(master=app, text="⏵", font=("Arial", 60, "bold"), command=play_file)
play_button.place(x=70, y=450)

fullscreen_button = customtkinter.CTkButton(master=app, text="", command=show_fullscreen)
fullscreen_button.place(x=70, y=600)

app.mainloop()

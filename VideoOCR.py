import datetime
import speech_recognition as sr
import moviepy.editor as mp
import tkinter as tk
import customtkinter
from tkinter import filedialog
from tkinter import *
from tkVideoPlayer import TkinterVideo


customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("900x600")
app.title("Распознаватор")


def update_duration(event):
    duration = vid_player.video_info()["duration"]
    end_time["text"] = str(datetime.timedelta(seconds=duration))
    progress_slider["to"] = duration


def update_scale(event):
    progress_value.set(int(vid_player.current_duration()))


def load_video():
    file_path = filedialog.askopenfilename()

    if file_path:
        vid_player.load(file_path)

        progress_slider.config(to=0, from_=0)
        play_pause_btn["text"] = "Play"
        progress_value.set(0)


def seek(value):
    vid_player.seek(int(value))


def skip(value: int):
    vid_player.seek(int(progress_slider.get())+value)
    progress_value.set(int(progress_slider.get())+value)


def play_pause():
    if vid_player.is_paused():
        vid_player.play()
        play_pause_btn["text"] = "Pause"

    else:
        vid_player.pause()
        play_pause_btn["text"] = "Play"


def video_ended(event):
    progress_slider.set(progress_slider["to"])
    play_pause_btn["text"] = "Play"
    progress_slider.set(0)


def open_txt():
    text_file = open('recognized.txt', 'r', encoding='utf-8')
    stuff = text_file.read()
    text_1.insert(END, stuff)
    text_file.close()


def start_recognition():
    op = filedialog.askopenfilename()
    clip = mp.VideoFileClip(op)

    clip.audio.write_audiofile(r"Converted_audio.wav")
    print("Конвертирование видеофайла завершено")

    audio = sr.AudioFile("Converted_audio.wav")
    print("Идет чтение аудиофайла...")

    r = sr.Recognizer()

    with audio as source:
        audio_file = r.record(source)

    result = r.recognize_google(audio_file, language='ru-RU')

    with open('recognized.txt', mode='w', encoding='utf-8') as file:
        file.write(result)

    print("Готово!")


frame_1 = customtkinter.CTkFrame(master=app)
frame_1.pack(pady=20, padx=20, fill="both", expand=True)

text_1 = customtkinter.CTkTextbox(master=frame_1, width=330, height=240)
text_1.place(x=500, y=50)

# Я пока не понял, как их внедрить:
# radiobutton_var = customtkinter.IntVar(value=1)
#
# radiobutton_1 = customtkinter.CTkRadioButton(master=frame_1, text="English", variable=radiobutton_var, value=1)
# radiobutton_1.place(x=10, y=480)
#
# radiobutton_2 = customtkinter.CTkRadioButton(master=frame_1, text="Русский", variable=radiobutton_var, value=2)
# radiobutton_2.place(x=10, y=450)

open_button = customtkinter.CTkButton(frame_1, text="Показать текст", command=open_txt)
open_button.place(x=690, y=300)

recognize_button = customtkinter.CTkButton(master=frame_1, text="Распознать", command=start_recognition)
recognize_button.place(x=500, y=300)

load_btn = customtkinter.CTkButton(master=frame_1, text="Выбрать файл", command=load_video)
load_btn.place(x=125, y=15)

vid_player = TkinterVideo(scaled=True, master=frame_1, bg="black")
vid_player.place(x=40, y=55, width=410, height=310)

play_pause_btn = customtkinter.CTkButton(master=frame_1, text="Play", command=play_pause)
play_pause_btn.place(x=120, y=380)

skip_plus_5sec = customtkinter.CTkButton(frame_1, text="-5 сек", command=lambda: skip(-5))
skip_plus_5sec.place(x=38, y=346)

start_time = tk.Label(frame_1, text=str(datetime.timedelta(seconds=0)), bg="grey17", fg="white")
start_time.place(x=115, y=410)

progress_value = tk.IntVar(frame_1)

progress_slider = tk.Scale(frame_1, variable=progress_value, from_=0, to=0, orient="horizontal", command=seek,
                           bg="grey17", fg="white")
progress_slider.place(x=40, y=365, width=410)

end_time = tk.Label(frame_1, text=str(datetime.timedelta(seconds=0)), bg="grey17", fg="white")
end_time.place(x=325, y=410)

vid_player.bind("<<Duration>>", update_duration)
vid_player.bind("<<SecondChanged>>", update_scale)
vid_player.bind("<<Ended>>", video_ended)

skip_plus_5sec = customtkinter.CTkButton(frame_1, text="+5 сек", command=lambda: skip(5))
skip_plus_5sec.place(x=205, y=346)

app.mainloop()

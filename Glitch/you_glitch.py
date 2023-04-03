import cv2
import tkinter as tk
from PIL import Image, ImageTk
import time
import numpy as np

window = tk.Tk()

label = tk.Label(window)
label.pack()

def glitch_image(img):
    img_array = np.array(img)
    row, col, channel = img_array.shape
    pixel_shift = np.random.randint(-10, 10, size=(row, col, channel))
    img_array = img_array + pixel_shift.astype(np.int64)
    img_array = img_array.astype(np.uint8)

    channel_shift = np.random.randint(-50, 50, size=(row, col, channel))
    img_array = np.uint8(np.clip(img_array + channel_shift.astype(np.int64), 0, 255))
    img_array = img_array.astype(np.uint8)

    kernel_size = np.random.randint(2, 7)
    img_array = cv2.blur(img_array, (kernel_size, kernel_size))

    return Image.fromarray(img_array)

def button_click(stop_event):
    flash = tk.Label(window, bg='white')
    flash.place(relwidth=1, relheight=1)
    window.update()
    time.sleep(0.5)
    flash.destroy()

    for i in range(45):
        ret, frame = cap.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (1000, 800))

        img = Image.fromarray(frame)
        img_tk = ImageTk.PhotoImage(img)
        label.config(image=img_tk)
        label.image = img_tk

        window.update()

        if i == 44:
            break

    ret, frame = cap.read()
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    img = Image.fromarray(img)
    img = glitch_image(img) 
    img_tk = ImageTk.PhotoImage(img)

    photo_window = tk.Toplevel()
    photo_label = tk.Label(photo_window, image=img_tk)
    photo_label.pack()

    photo_window.wait_window(photo_window)

button = tk.Button(window, text="Take photo", command=lambda: button_click(True))
button.pack()

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (1000, 800))

    img = Image.fromarray(frame)
    img_tk = ImageTk.PhotoImage(img)
    label.config(image=img_tk)
    label.image = img_tk

    window.update()
    
cap.release()
window.destroy()
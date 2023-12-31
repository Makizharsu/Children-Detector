import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
import numpy as np  # Correcting the import statement

# Loading the Model
from keras.models import load_model
model = load_model('Child_Detector.h5')

# Initializing the GUI
top = tk.Tk()
top.geometry('800x600')
top.title('Children Detector')
top.configure(background='black')

# Initializing the labels (1 for age and 1 for Sex)
label = Label(top, background="black", font=('arial', 15, "bold"))
sign_image = Label(top)

# Define Detect function
def Detect(file_path):
    global label_packed
    image = Image.open(file_path)
    image = image.resize((48, 48))
    image = np.expand_dims(image, axis=0)
    image = np.array(image)
    image = np.delete(image, 0, 1)
    image = np.resize(image, (48, 48, 3))
    print(image.shape)
    sex_f = ["Male", "Female"]
    image = np.array([image]) / 255
    pred = model.predict(image)
    age = int(np.round(pred[1][0]))
    sex = int(np.round(pred[0][0]))
    if age < 18:
        label.configure(foreground="sky blue", text="Child detected!")
    else:
        label.configure(foreground="red", text="Not a child!")



# Define Show_detect button function
def show_Detect_button(file_path):
    Detect_b = Button(top, text="Detect Image", command=lambda: Detect(file_path), padx=10, pady=5)
    Detect_b.configure(background="green", foreground='white', font=('arial', 10, 'bold'))
    Detect_b.place(relx=0.79, rely=0.46)  # Corrected the typo here

# Define Upload Image function
def upload_image():
    try:
        file_path = filedialog.askopenfilename()  # Corrected the line to get the file path
        uploaded = Image.open(file_path)
        uploaded.thumbnail(((top.winfo_width() / 2.25), (top.winfo_height() / 2.25)))
        im = ImageTk.PhotoImage(uploaded)

        sign_image.configure(image=im)
        sign_image.image = im
        label.configure(text='')
        show_Detect_button(file_path)
    except Exception as e:
        print(f"Error: {e}")

upload = Button(top, text="Upload an Image", command=upload_image, padx=10, pady=5)
upload.configure(background="Blue", foreground='white', font=('arial', 10, 'bold'))
upload.pack(side='bottom', pady=50)
sign_image.pack(side='bottom', expand=True)
label.pack(side="bottom", expand=True)


heading = Label(top, text="Children Detector", pady=20, font=('arial', 20, "bold"))
heading.configure(background="Black", foreground="White")
heading.pack()

top.mainloop()

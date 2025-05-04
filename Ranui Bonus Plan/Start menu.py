import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import main

def start_app():
    root.quit()  # Close the start menu window
    main.launch_main_app()

root = tk.Tk()
root.title("Start Menu")
root.geometry("1000x600")
root.iconbitmap("logo.ico")

# Load and place background
bg_image = Image.open("Ranui Bonus Plan/background.png").resize((1000, 600))
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)

# Header
header_frame = tk.Frame(root, bg="#333", borderwidth=5, relief=tk.SUNKEN)
header_frame.pack(side=tk.TOP, fill=tk.X)
header_label = tk.Label(header_frame, text="Ranui Bonus Plan", fg="white", bg="black", font=("Arial", 20))
header_label.pack(pady=10)

# Buttons
button_frame = tk.Frame(root, bg="white")
button_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

start_button = ttk.Button(button_frame, text="Start Application", command=start_app)
start_button.pack(pady=10, ipadx=10)

quit_button = ttk.Button(button_frame, text="Quit", command=root.quit)
quit_button.pack(pady=5, ipadx=10)

root.mainloop()


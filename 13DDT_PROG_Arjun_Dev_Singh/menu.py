import tkinter as tk
from PIL import Image, ImageTk

def launch_main_app():
    menu_root.destroy()
    import main  

def quit_app():
    menu_root.destroy()

menu_root = tk.Tk()
menu_root.title("Macleans Navigator")
menu_root.geometry("600x400")
menu_root.configure(bg="white")
menu_root.iconbitmap("images/logo.ico")

# Set background image

bg_image = Image.open("images/bg.png")
bg_image = bg_image.resize((600, 400))
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(menu_root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
bg_label.image = bg_photo

#Load logo image
logo_img = Image.open("images/logo.ico")
logo_img = logo_img.resize((100, 100))
logo_photo = ImageTk.PhotoImage(logo_img)
logo_label = tk.Label(menu_root, image=logo_photo, bg="white")
logo_label.image = logo_photo
logo_label.pack(pady=(30, 10))


# Title under logo
title_label = tk.Label(menu_root, text="Macleans Navigator", font=("Arial", 18, "bold"), bg=None)
title_label.pack()

# Start button
start_button = tk.Button(
    menu_root, text="Start", command=launch_main_app,
    font=("Arial", 14), bg="#10E217", fg="white", padx=20, pady=5)

start_button.pack(pady=15)

# Quit button
quit_button = tk.Button(
    menu_root, text="Quit", command=quit_app,
    font=("Arial", 12), bg="#da0f00", fg="white", padx=20, pady=5)


quit_button.pack()

menu_root.mainloop()


import tkinter as tk
from PIL import Image, ImageTk
from tkinterweb import HtmlFrame

# Create the main window
root = tk.Tk()
root.title("Macleans Navigator")
root.geometry("800x600")
root.iconbitmap("images/logo.ico")
root.configure(bg="blue")

# Set background image
bg_image = Image.open("images/bg2.jpg")
bg_image = bg_image.resize((800, 600))
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
bg_label.image = bg_photo

# Header
header = tk.Label(root, text="Macleans Navigator", bg="white", font=("Arial", 16, "bold"), width=80, pady=10)
header.pack(pady=10)

# Frame for location and destination
input_frame = tk.Frame(root, bg="blue")
input_frame.pack(pady=10)

# location input
your_location = tk.Entry(input_frame, width=30)
your_location.grid(row=0, column=0, padx=5)
your_location_btn = tk.Button(input_frame, text="Enter")
your_location_btn.grid(row=0, column=1, padx=5)

# Destination input
destination = tk.Entry(input_frame, width=30)
destination.grid(row=0, column=2, padx=5)
destination_btn = tk.Button(input_frame, text="Enter")
destination_btn.grid(row=0, column=3, padx=5)

# Embedded Map Area (Leaflet via tkinterweb)
map_frame = HtmlFrame(root, horizontal_scrollbar="auto")
map_frame.load_file("map.html")
map_frame.pack(pady=15, expand=True, fill="both")

# Footer with credits and contact
footer_frame = tk.Frame(root, bg="blue")
footer_frame.pack(pady=20)

credits_btn = tk.Button(footer_frame, text="Credits", width=20)
credits_btn.grid(row=0, column=0, padx=10)

contact_btn = tk.Button(footer_frame, text="Contact Us", width=20)
contact_btn.grid(row=0, column=1, padx=10)

# Start the GUI loop
root.mainloop()

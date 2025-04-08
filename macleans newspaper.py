from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Macleans Newspaper")
root.geometry("1180x644")
root.minsize(width=300, height=300)
root.iconbitmap("logo.ico")

# Header
Header = Frame(root, bg="#333", borderwidth=5, relief=SUNKEN)
Header.pack(side=TOP, fill=X)
headerlabel = Label(Header, text="Macleans Newspaper", padx=10)
headerlabel.pack()

# News 1 Frame
f1 = Frame(root, bg="lightblue", borderwidth=5, relief=SUNKEN)
f1.pack(side=TOP, fill=X, padx=10, pady=10)

# Canvas to control image size
canvas = Canvas(f1, width=100, height=100, bg="lightblue", highlightthickness=0)  # Adjust width & height
canvas.grid(row=0, column=0, padx=10, pady=10, sticky="w")  # Align image left

# Load Image using Tkinter PhotoImage
neutral_image = PhotoImage(file="C:/Users/arjun/Downloads/240802_Porsche-918-Spyder-7.gif")

# Place the image inside the canvas (cropped to fit)
canvas.create_image(25, 25, image =neutral_image, anchor=CENTER)  # Center inside 100x100 canvas

# Add Text Next to Image
text_label = ttk.Label(f1, text="car", wraplength=200)
text_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")  # Place text beside image
# News 2 Frame
f2 = Frame(root, bg="lightblue", borderwidth=5, relief=SUNKEN)
f2.pack(side=TOP, fill=X, padx=10, pady=10)

canvas = Canvas(f2, width=100, height=100, bg="lightblue", highlightthickness=0)  # Adjust width & height
canvas.grid(row=0, column=1, padx=10, pady=10, sticky="w")  # Align image left
neutral_image2 = PhotoImage(file="C:/Users//arjun/Downloads/ezgif.com-animated-gif-maker.gif")
canvas.create_image(25, 25, image =neutral_image2, anchor=CENTER)  # Center inside 100x100 canvas
text_label = ttk.Label(f2, text="car2ljfewfljfljf", wraplength=200)
text_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")  # Place text beside image

#news 3 frame
f3 = Frame(root, bg="lightblue", borderwidth=5, relief=SUNKEN)
f3.pack(side=TOP, fill=X, padx=10, pady=10)

canvas = Canvas(f3, width=100, height=100, bg="lightblue", highlightthickness=0)  # Adjust width & height
canvas.grid(row=0, column=1, padx=10, pady=10, sticky="w")  # Align image left
neutral_image3 = PhotoImage(file="C:/Users/arjun/Downloads/ezgif.com-animated-gif-maker (1).gif")
canvas.create_image(100, 100, image =neutral_image3, anchor=CENTER)  # Center inside 100x100 canvas
text_label = ttk.Label(f3, text="car3", wraplength=200)
text_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")  # Place text beside image

#news 4 frame
f4 = Frame(root, bg="lightblue", borderwidth=5, relief=SUNKEN)
f4.pack(side=TOP, fill=X, padx=10, pady=10)
canvas = Canvas(f4, width=100, height=100, bg="lightblue", highlightthickness=0)  # Adjust width & height
canvas.grid(row=0, column=1, padx=10, pady=10, sticky="w")  # Align image left
neutral_image4 = PhotoImage(file="C:/Users/arjun/Downloads/ezgif.com-animated-gif-maker (1).gif")
canvas.create_image(100, 100, image =neutral_image4, anchor=CENTER)  # Center inside 100x100 canvas
text_label = ttk.Label(f4, text="car4", wraplength=200)
text_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")  # Place text beside image

root.mainloop()


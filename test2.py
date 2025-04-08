from tkinter import ttk

uservalue = StringVar()
passvalue = StringVar()

userentry = Entry(root, textvaruable = uservalue)
passentry = Entry(root, textvariable = passvalue)

userentry.grid(row=0, column=1)
passentry.grid(row=1, colummn=1)

def getvals():
    print(f"the value of username is {uservalue.get()}")
    print(f"the value of password is {passvalue.get()}")

Button(texts="Submit", command=getvals).grid()

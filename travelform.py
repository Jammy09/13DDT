import tkinter as tk
import tkinter as ttk

# Create main window
root = tk.Tk()
root.title("Travel Form")
root.geometry("300x250")

# Labels and Entry fields
tk.Label(root, text="Name").pack()
name_entry = tk.Entry(root)
name_entry.pack()

tk.Label(root, text="Destination").pack()
destination_entry = tk.Entry(root)
destination_entry.pack()

tk.Label(root, text="Date (DD-MM-YYYY)").pack()
date_entry = tk.Entry(root)
date_entry.pack()

tk.Label(root, text="Purpose").pack()
purpose_entry = tk.Entry(root)
purpose_entry.pack()

tk.Label(root, text="Gender").pack()
gender_entry = tk.Entry(root)
gender_entry.pack()

tk.Label(root, text="Age").pack()
age_entry = tk.Entry(root)
age_entry.pack()

tk.Label(root, text="Payment mode").pack()
payment_mode_entry = tk.Entry(root)
payment_mode_entry.pack()

tk.Label(root, text="Contact Number").pack()
contact_entry = tk.Entry(root)
contact_entry.pack()

tk.Label(root, text="Emergency Contact").pack()
emergency_contact_entry = tk.Entry(root)
emergency_contact_entry.pack()

tk.Label(root, text="Want to prebook your meals?").pack()
meal_var = tk.BooleanVar()
meal_checkbox = tk.Checkbutton(root, text="Yes", variable=meal_var)
meal_checkbox.pack()

#Submit button
submit_button = tk.Button(root, text="Submit", command=lambda: submit_form())
submit_button.pack()
# Function to handle form submission
def submit_form():
    name = name_entry.get()
    destination = destination_entry.get()
    date = date_entry.get()
    purpose = purpose_entry.get()
    gender = gender_entry.get()
    age = age_entry.get()
    payment_mode = payment_mode_entry.get()
    contact = contact_entry.get()
    emergency_contact = emergency_contact_entry.get()
    meal_checkbox = meal_var.get()
    print(f"Name: {name}")
    print(f"Destination: {destination}")
    print(f"Date: {date}")
    print(f"Purpose: {purpose}")
    print(f"Gender: {gender}")
    print(f"Age: {age}")
    print(f"Payment Mode: {payment_mode}")
    print(f"Contact: {contact}")
    print(f"Emergency Contact: {emergency_contact}")
    print(f"Meal Prebooking: {meal_checkbox}")



root.mainloop() 
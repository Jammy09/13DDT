import tkinter as tk
from tkinter import ttk, messagebox

# Data Storage (previously in data_storage.py)
children_data = {
    "Nikau": {"balance": 300, "bonus": True},
    "Hana": {"balance": 300, "bonus": True},
    "Tia": {"balance": 300, "bonus": True}
}

def deduct_amount(child_name, amount):
    if child_name in children_data:
        children_data[child_name]["balance"] -= amount
        if children_data[child_name]["balance"] < 0:
            children_data[child_name]["balance"] = 0
        children_data[child_name]["bonus"] = children_data[child_name]["balance"] > 50
        return children_data[child_name]
    return None

def get_child_info(child_name):
    return children_data.get(child_name)

# Main Application
def launch_main_app():
    def update_display():
        for child in ["Nikau", "Hana", "Tia"]:
            info = get_child_info(child)
            balances[child].config(text=f"${info['balance']}")
            bonuses[child].config(text="Yes" if info['bonus'] else "No")

    def handle_deduction():
        try:
            child = selected_child.get()
            amount = float(amount_entry.get())
            if amount < 0:
                raise ValueError
            result = deduct_amount(child, amount)
            if result is None:
                messagebox.showerror("Error", "Invalid child selected.")
            else:
                update_display()
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid positive number.")

    app = tk.Tk()
    app.title("Ranui Bonus Plan - Main")
    app.geometry("600x400")

    ttk.Label(app, text="Select Child:").pack(pady=5)
    selected_child = tk.StringVar()
    child_selector = ttk.Combobox(app, textvariable=selected_child, values=["Nikau", "Hana", "Tia"])
    child_selector.pack(pady=5)

    ttk.Label(app, text="Enter Amount Spent:").pack(pady=5)
    amount_entry = ttk.Entry(app)
    amount_entry.pack(pady=5)

    ttk.Button(app, text="Deduct", command=handle_deduction).pack(pady=10)

    ttk.Label(app, text="Current Balances & Bonus Eligibility", font=("Arial", 12, "bold")).pack(pady=10)
    balances = {}
    bonuses = {}
    for child in ["Nikau", "Hana", "Tia"]:
        frame = ttk.Frame(app)
        frame.pack(pady=2)
        ttk.Label(frame, text=child).grid(row=0, column=0, padx=10)
        balances[child] = ttk.Label(frame, text="$300")
        balances[child].grid(row=0, column=1, padx=10)
        bonuses[child] = ttk.Label(frame, text="Yes")
        bonuses[child].grid(row=0, column=2, padx=10)

    update_display()
    app.mainloop()
if __name__ == "__main__":
    launch_main_app()
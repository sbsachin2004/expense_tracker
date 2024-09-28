import tkinter as tk
from tkinter import messagebox, filedialog
from tkcalendar import DateEntry
from tkinter import ttk
import pandas as pd
import os
from PIL import Image, ImageTk  # Use PIL for image handling

# Initialize the main application window
root = tk.Tk()
root.title("Expense Tracker")

# Set the window size
root.geometry("800x600")
root.resizable(True, True)

# Center the window on the screen
def center_window():
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")

# Global list to store expenses and categories
expenses = []
categories = ["Mobile", "Food", "Snacks", "Electronics"]  # Predefined categories
custom_category_file = "categories.csv"  # File to store custom categories

# File path to store expenses
file_path = "expenses.csv"

# Load background image
background_image = Image.open("background.jpg")  # Replace with your background image file
background_image = background_image.resize((800, 600), Image.Resampling.LANCZOS)  # Resize the image to fit the window
bg_image = ImageTk.PhotoImage(background_image)

# Add the background image as a label
background_label = tk.Label(root, image=bg_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Make sure it covers the entire window

# Function to load custom categories from a file
def load_custom_categories():
    if os.path.exists(custom_category_file):
        try:
            df = pd.read_csv(custom_category_file)
            return df['Category'].tolist()  # Return list of categories
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load custom categories: {str(e)}")
    return []

# Function to save custom categories to a CSV file
def save_custom_categories():
    df = pd.DataFrame(categories, columns=["Category"])  # Convert categories list to DataFrame
    try:
        df.to_csv(custom_category_file, index=False)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save custom categories: {str(e)}")

# Load custom categories at startup
categories += load_custom_categories()

# Function to load expenses from a CSV file
def load_expenses():
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            global expenses
            expenses = df.to_dict("records")
            update_expense_list()
            update_total()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load expenses: {str(e)}")

# Function to save expenses to a CSV file
def save_expenses():
    df = pd.DataFrame(expenses)
    try:
        df.to_csv(file_path, index=False)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save expenses: {str(e)}")

# Function to update the displayed expense list in the Treeview
def update_expense_list():
    for row in tree.get_children():
        tree.delete(row)
    for expense in expenses:
        tree.insert("", "end", values=(expense["Date"], expense["Description"], expense["Quantity"], expense["Amount"], expense["Category"]))

# Function to calculate and update the total expenses
def update_total():
    total_amount = sum(expense["Amount"] for expense in expenses)
    total_label.config(text=f"Total: {total_amount:.2f}")

# Function to add a new expense
def add_expense():
    date = date_entry.get()
    description = description_entry.get()
    quantity = quantity_entry.get().strip()
    amount = amount_entry.get().strip()
    category = category_var.get()

    # Handle custom category input
    custom_category = custom_category_entry.get().strip()
    if custom_category:
        category = custom_category
        if category not in categories:
            categories.append(category)  # Add to categories list
            save_custom_categories()  # Save the new category
            category_combobox['values'] = categories  # Update dropdown with new category
    
    try:
        quantity = int(quantity)
        amount = float(amount.replace(",", "").replace(" ", ""))
        total_amount = quantity * amount
        expenses.append({"Date": date, "Description": description, "Quantity": quantity, "Amount": total_amount, "Category": category})
        update_expense_list()
        update_total()
        save_expenses()

        # Clear input fields
        description_entry.delete(0, tk.END)
        quantity_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        custom_category_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid quantity and amount.")

# Function to delete the selected expense
def delete_expense():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("No selection", "Please select an expense to delete.")
        return

    confirm = messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete the selected expense?")
    if not confirm:
        return

    for item in selected_item:
        values = tree.item(item, "values")
        date, description, quantity, amount, category = values
        for expense in expenses:
            if (expense["Date"] == date and expense["Description"] == description and 
                expense["Quantity"] == int(quantity) and float(expense["Amount"]) == float(amount) and expense["Category"] == category):
                expenses.remove(expense)
                break

    update_expense_list()
    update_total()
    save_expenses()

# Function to export expenses to Excel
def export_to_excel():
    if not expenses:
        messagebox.showwarning("No Data", "No expenses to export.")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", 
                                             filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                                             title="Choose a folder and file name to save")
    
    if not file_path:
        return

    try:
        df = pd.DataFrame(expenses)
        df.to_excel(file_path, index=False)
        messagebox.showinfo("Export Successful", f"Expenses exported to {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export expenses: {str(e)}")

# Frame for controls
frame = tk.Frame(root, bg='lightgray')
frame.pack(fill="both", expand=True, padx=10, pady=10)

# UI Components
tk.Label(frame, text="Date:", bg='lightgray', fg='black', font=("Arial", 12, "bold")).grid(row=0, column=0, padx=10, pady=10, sticky="e")
date_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
date_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(frame, text="Description:", bg='lightgray', fg='black', font=("Arial", 12, "bold")).grid(row=1, column=0, padx=10, pady=10, sticky="e")
description_entry = tk.Entry(frame)
description_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(frame, text="Quantity:", bg='lightgray', fg='black', font=("Arial", 12, "bold")).grid(row=2, column=0, padx=10, pady=10, sticky="e")
quantity_entry = tk.Entry(frame)
quantity_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Label(frame, text="Amount:", bg='lightgray', fg='black', font=("Arial", 12, "bold")).grid(row=3, column=0, padx=10, pady=10, sticky="e")
amount_entry = tk.Entry(frame)
amount_entry.grid(row=3, column=1, padx=10, pady=10)

# Adding Category Dropdown
tk.Label(frame, text="Category:", bg='lightgray', fg='black', font=("Arial", 12, "bold")).grid(row=4, column=0, padx=10, pady=10, sticky="e")
category_var = tk.StringVar()
category_combobox = ttk.Combobox(frame, textvariable=category_var, state="readonly")
category_combobox['values'] = categories  # Load all categories (predefined + custom)
category_combobox.grid(row=4, column=1, padx=10, pady=10)
category_combobox.current(0)

# Custom Category Entry
tk.Label(frame, text="Custom Category (optional):", bg='lightgray', fg='black', font=("Arial", 12, "bold")).grid(row=5, column=0, padx=10, pady=10, sticky="e")
custom_category_entry = tk.Entry(frame)
custom_category_entry.grid(row=5, column=1, padx=10, pady=10)

# Add and Delete Buttons
add_button = tk.Button(frame, text="Add Expense", command=add_expense)
add_button.grid(row=6, column=0, pady=10)

delete_button = tk.Button(frame, text="Delete Expense", command=delete_expense)
delete_button.grid(row=6, column=1, pady=10)

export_button = tk.Button(frame, text="Export to Excel", command=export_to_excel)
export_button.grid(row=6, column=2, pady=10)

# Treeview for displaying expenses
columns = ("Date", "Description", "Quantity", "Amount", "Category")
tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, minwidth=100, width=150)
tree.grid(row=7, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

# Scrollbar for Treeview
scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.grid(row=7, column=3, sticky="ns")

# Total Amount Label
total_label = tk.Label(root, text="Total: 0.00", font=("Arial", 14, "bold"))
total_label.pack(pady=10)

# Load the expenses from file when the app starts
load_expenses()

# Center the window on the screen after initialization
center_window()

# Start the Tkinter main loop
root.mainloop()

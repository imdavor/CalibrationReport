import tkinter as tk
from tkinter import filedialog, ttk
import csv
import os

file_path = ''


def open_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        print(f"Selected file: {file_path}")


def create_report():
    if not file_path:
        print("No file selected!")
        return
    # Create a new window for the report
    report_window = tk.Toplevel(root)
    report_window.title("Report")

    # Create a treeview widget
    tree = ttk.Treeview(report_window, columns=("Point", "X/r", "Y/a", "Z", "R", "D", "L", "W", "A", "f", "When"),
                        show='headings')

    # Define headings
    tree.heading("Point", text="Point")
    tree.heading("X/r", text="X/r")
    tree.heading("Y/a", text="Y/a")
    tree.heading("Z", text="Z")
    tree.heading("R", text="R")
    tree.heading("D", text="D")
    tree.heading("L", text="L")
    tree.heading("W", text="W")
    tree.heading("A", text="A")
    tree.heading("f", text="f")
    tree.heading("When", text="When")

    # Read data from CSV file and insert into the treeview
    try:
        with open(file_path, newline='', encoding='utf-16') as csvfile:
            reader = csv.DictReader(csvfile)
            # Print column names to debug
            print("Column names:", reader.fieldnames)
            for row in reader:
                tree.insert("", tk.END, values=(
                    row['Name'], row['X/r'], row['Y/a'], row['Z'], row['R'], row['D'], row['L'], row['W'], row['A'],
                    row['f'], row['When']))
    except Exception as e:
        print(f"Error reading file: {e}")

    # Pack the treeview widget
    tree.pack(padx=10, pady=10)

    # Add Print and Close buttons to the report window
    print_button = tk.Button(report_window, text="Print", command=lambda: print_report(tree))
    close_button = tk.Button(report_window, text="Zatvori", command=report_window.destroy)

    print_button.pack(pady=5)
    close_button.pack(pady=5)


def print_report(tree):
    # Save the report to a temporary file
    temp_file = "temp_report.txt"

    with open(temp_file, 'w') as f:
        for child in tree.get_children():
            f.write("\t".join(map(str, tree.item(child)["values"])) + "\n")

    # Print the temporary file using the default printer or PDF printer
    os.startfile(temp_file, "print")


# Create the main window
root = tk.Tk()
root.title("Kalibracijski Izvještaj")

# Adjust size
root.geometry("800x600")

# Create buttons
open_button = tk.Button(root, text="Otvori datoteku", command=open_file)
report_button = tk.Button(root, text="Kreiraj report", command=create_report)
print_button = tk.Button(root, text="Print", command=lambda: print_report(tree))
close_button = tk.Button(root, text="Zatvori", command=root.destroy)

# Arrange buttons in the window
open_button.pack(pady=10)
report_button.pack(pady=10)
print_button.pack(pady=10)
close_button.pack(pady=10)

# Run the application
root.mainloop()

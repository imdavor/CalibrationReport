import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import csv
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

file_path = ''


def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        print(f"Selected file: {file_path}")
        create_report(file_path)


def create_report(file_path):
    # Create a new window for the report
    report_window = tk.Toplevel(root)
    report_window.title("Report")

    # Create a treeview widget
    global tree
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
    with open(file_path, newline='', encoding='utf-16') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            tree.insert("", tk.END, values=(
                row['Name'], row['X/r'], row['Y/a'], row['Z'], row['R'], row['D'], row['L'], row['W'], row['A'],
                row['f'], row['When']
            ))

    # Pack the treeview widget
    tree.pack(padx=10, pady=10)

    # Add Print and Close buttons to the report window
    print_button = tk.Button(report_window, text="Print", command=lambda: print_report(file_path))
    close_button = tk.Button(report_window, text="Zatvori", command=report_window.destroy)
    print_button.pack(pady=5)
    close_button.pack(pady=5)


def print_report(file_path, max_widths=None):
    # Specify the PDF file name
    pdf_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not pdf_file:
        return  # If the user cancels the save dialog

    # Create a PDF canvas
    c = canvas.Canvas(pdf_file, pagesize=letter)
    width, height = letter

    # Set initial positions for the content
    x_offset = 50
    y_offset = height - 50
    line_height = 20  # Space between lines

    # Title of the PDF
    c.setFont("Helvetica-Bold", 14)
    c.drawString(x_offset, y_offset, "Calibration Report")
    y_offset -= line_height * 2  # Move down

    # Write column headers
    headers = ["Point", "X/r", "Y/a", "Z", "R", "D", "L", "W", "A", "f", "When"]
    c.setFont("Helvetica-Bold", 12)
    for i, header in enumerate(headers):
        c.drawString(x_offset + sum(max_widths[:i]), y_offset, header)
    y_offset -= line_height  # Move down for the rows

    # Measure and adjust column widths
    max_widths = [0] * len(headers)
    for row_id in tree.get_children():
        row_values = tree.item(row_id)['values']
        for i, value in enumerate(row_values):
            max_widths[i] = max(max_widths[i], c.stringWidth(str(value), "Helvetica", 10))

    for i, width in enumerate(max_widths):
        max_widths[i] = width + 10  # Add some padding

    # Write the data from Treeview with adjusted widths
    c.setFont("Helvetica", 10)
    for row_id in tree.get_children():  # Loop through treeview rows
        row_values = tree.item(row_id)['values']
        for i, value in enumerate(row_values):
            c.drawString(x_offset + sum(max_widths[:i]), y_offset, str(value))
        y_offset -= line_height  # Move to the next row

        # If we reach the bottom of the page, create a new page
        if y_offset < 50:
            c.showPage()  # Save the current page
            y_offset = height - 50  # Reset y_offset for the new page

    # Save the PDF file
    c.save()

    # Notify the user that the PDF has been saved
    messagebox.showinfo("PDF Saved", f"Report saved as {os.path.basename(pdf_file)}")


# Create the main window
root = tk.Tk()
root.title("Kalibracijski Izvještaj")

# Adjust size
root.geometry("800x600")

# Create buttons
open_button = tk.Button(root, text="Otvori datoteku", command=open_file)
report_button = tk.Button(root, text="Kreiraj report", command=lambda: create_report(file_path))
print_button = tk.Button(root, text="Print", command=lambda: print_report(file_path))
close_button = tk.Button(root, text="Zatvori", command=root.destroy)

# Arrange buttons in the window
open_button.pack(pady=10)
report_button.pack(pady=10)
print_button.pack(pady=10)
close_button.pack(pady=10)

# Run the application
root.mainloop()

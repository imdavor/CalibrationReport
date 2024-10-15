import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import csv
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

file_path = ''
report_window = None  # Globalna varijabla za prozor izvještaja


def open_file():
    global file_path, report_window
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        print(f"Odabrana datoteka: {file_path}")
        if report_window:  # Ako prozor izvještaja već postoji, uništi ga
            report_window.destroy()
        report_button.config(state=tk.NORMAL)  # Omogući gumb za kreiranje izvještaja


def create_report(file_path, tkFont=None):
    global report_window
    if report_window:
        report_window.destroy()  # Zatvori prethodni prozor ako postoji

    # Kreiraj novi prozor za izvještaj
    report_window = tk.Toplevel(root)
    report_window.title("Izvještaj")

    # Kreiraj treeview widget za prikaz podataka s dodanim scroll barovima
    frame = ttk.Frame(report_window)
    frame.pack(fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(frame, columns=("Point", "X/r", "Y/a", "R", "D", "When"),
                        show='headings', height=20)

    # Dodaj vertikalni i horizontalni scrollbar
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    vsb.pack(side=tk.RIGHT, fill=tk.Y)
    hsb.pack(side=tk.BOTTOM, fill=tk.X)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Definiraj zaglavlja stupaca
    tree.heading("Point", text="Point")
    tree.heading("X/r", text="X/r")
    tree.heading("Y/a", text="Y/a")
    tree.heading("R", text="R")
    tree.heading("D", text="D")
    tree.heading("When", text="When")

    # Čitaj podatke iz CSV datoteke i ubaci ih u treeview
    try:
        with open(file_path, newline='', encoding='utf-16') as csvfile:
            reader = csv.DictReader(csvfile)
            row_count = 0  # Broji retke
            for row in reader:
                tree.insert("", tk.END, values=(
                    row['Name'], row['X/r'], row['Y/a'],
                    row['R'], row["D"], row['When']
                ))
                row_count += 1
    except Exception as e:
        messagebox.showerror("Greška", f"Neuspjelo čitanje CSV datoteke: {e}")
        return

    # Automatski prilagodi širinu stupaca na temelju najdužeg podatka
    for col in tree['columns']:
        tree.column(col, width=tkFont.Font().measure(col))
        for row_id in tree.get_children():
            cell_value = tree.item(row_id)['values'][tree['columns'].index(col)]
            tree.column(col, width=max(tree.column(col)['width'], tkFont.Font().measure(str(cell_value))))

    # Dodaj gumbe za Print i Zatvori
    print_button = tk.Button(report_window, text="Print", command=lambda: print_report(tree))
    close_button = tk.Button(report_window, text="Zatvori", command=report_window.destroy)
    print_button.pack(pady=5)
    close_button.pack(pady=5)

    report_button.config(state=tk.DISABLED)  # Onemogući ponovno kreiranje izvještaja dok ne odabereš novu datoteku


def print_report(tree):
    # Odabir naziva PDF datoteke
    pdf_file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if not pdf_file:
        return  # Ako korisnik otkaže spremanje

    # Kreiraj PDF
    c = canvas.Canvas(pdf_file, pagesize=letter)
    width, height = letter

    # Početne pozicije za sadržaj
    x_offset = 50
    y_offset = height - 50
    line_height = 20  # Razmak između redaka

    # Naslov PDF-a
    c.setFont("Helvetica-Bold", 14)
    c.drawString(x_offset, y_offset, "Izvještaj kalibracije")
    y_offset -= line_height * 2  # Pomakni dolje

    # Zaglavlja stupaca
    headers = ["Point", "X/r", "Y/a", "R", "D", "When"]
    c.setFont("Helvetica-Bold", 12)
    max_widths = [0] * len(headers)  # Inicijalizacija maksimalnih širina
    for i, header in enumerate(headers):
        c.drawString(x_offset + sum(max_widths[:i]), y_offset, header)
    y_offset -= line_height  # Pomakni dolje za retke

    # Izračunaj širine stupaca
    for row_id in tree.get_children():
        row_values = tree.item(row_id)['values']
        for i, value in enumerate(row_values):
            max_widths[i] = max(max_widths[i], c.stringWidth(str(value), "Helvetica", 10))

    # Podesi širine stupaca
    max_widths = [width + 10 for width in max_widths]

    # Napiši podatke iz Treeview-a s podešenim širinama
    c.setFont("Helvetica", 10)
    for row_id in tree.get_children():  # Prođi kroz retke
        row_values = tree.item(row_id)['values']
        for i, value in enumerate(row_values):
            c.drawString(x_offset + sum(max_widths[:i]), y_offset, str(value))
        y_offset -= line_height  # Sljedeći redak

        # Ako dođeš do dna stranice, kreiraj novu stranicu
        if y_offset < 50:
            c.showPage()  # Spremi trenutnu stranicu
            y_offset = height - 50  # Resetiraj y_offset

    # Spremi PDF datoteku
    c.save()

    # Obavijesti korisnika da je PDF spremljen
    messagebox.showinfo("PDF Spremljen", f"Izvještaj je spremljen kao {os.path.basename(pdf_file)}")


# Kreiraj glavni prozor
root = tk.Tk()
root.title("Kalibracijski Izvještaj")

# Podesi početnu veličinu
root.geometry("800x600")

# Kreiraj gumbe
open_button = tk.Button(root, text="Otvori datoteku", command=open_file)
report_button = tk.Button(root, text="Kreiraj report", state=tk.DISABLED, command=lambda: create_report(file_path))
close_button = tk.Button(root, text="Zatvori", command=root.destroy)

# Postavi gumbe u prozor
open_button.pack(pady=10)
report_button.pack(pady=10)
close_button.pack(pady=10)

# Pokreni aplikaciju
root.mainloop()

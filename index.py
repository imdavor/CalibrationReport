import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import csv
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tkinter.font as tkFont  # Dodaj ovu liniju na početak

file_path = ''
report_window = None  # Globalna varijabla za prozor izvještaja


def open_file():
    global file_path, report_window
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        print(f"Odabrana datoteka: {file_path}")
        filename_label.config(text=f"Datoteka: {os.path.basename(file_path)}")  # Ažuriraj label s imenom datoteke
        if report_window:  # Ako prozor izvještaja već postoji, uništi ga
            report_window.destroy()
        report_button.config(state=tk.NORMAL)  # Omogući gumb za kreiranje izvještaja


def create_report(file_path):
    global report_window
    if report_window:
        report_window.destroy()  # Zatvori prethodni prozor ako postoji

    # Kreiraj novi prozor za izvještaj
    report_window = tk.Toplevel(root)
    report_window.title("Izvještaj")
    report_window.geometry("800x600")  # Postavi početnu veličinu prozora

    # Kreiraj treeview widget za prikaz podataka s dodanim scroll barovima
    frame = ttk.Frame(report_window)
    frame.pack(fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(frame, columns=("Point", "NOMINAL_X", "NOMINAL_Y", "X/r", "Y/a", "Actual _X","Actual _Y", "Error_X", "Error_Y"),
                        show='headings', height=20)

    # Dodaj vertikalni i horizontalni scrollbar
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    vsb.pack(side=tk.RIGHT, fill=tk.Y)
    hsb.pack(side=tk.BOTTOM, fill=tk.X)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # # Povećaj visinu redaka (simuliraj zaglavlje "NOMINAL")
    # tree.insert("", tk.END, values=("NOMINAL", "", "", "", "", ""))  # Dodaj prazan redak s nominalnim zaglavljem

    # Definiraj zaglavlja stupaca
    # tree.heading("Point", text="Point")
    # tree.heading("NOMINAL_X", text="X")
    # tree.heading("NOMINAL_Y", text="Y")
    # tree.heading("X/r", text="X/r")
    # tree.heading("Y/a", text="Y/a")
    # tree.heading("Actual _X", text="Actual _X")
    # tree.heading("Actual _Y", text="Actual _Y")
    # tree.heading("Error_X", text="Error_X")
    # tree.heading("Error_Y", text="Error_Y")
    # tree.heading("X", text="X")
    # tree.heading("Y", text="Y")
    # tree.heading("R", text="R")
    # tree.heading("D", text="D")
    # tree.heading("When", text="When")
    tree.heading("Point", text="Point")
    tree.heading("NOMINAL_X", text="X")
    tree.heading("NOMINAL_Y", text="Y")
    tree.heading("X/r", text="X/r")
    tree.heading("Y/a", text="Y/a")
    tree.heading("Error_X", text="Error X")
    tree.heading("Error_Y", text="Error Y")
    tree.column("Point", width=100)
    tree.column("NOMINAL_X", width=100)
    tree.column("NOMINAL_Y", width=100)
    tree.column("X/r", width=100)
    tree.column("Y/a", width=100)
    tree.column("Error_X", width=100)
    tree.column("Error_Y", width=100)
    

    x_values = [
    0.00000, 28.00000, 56.00000, 84.00000, 112.00000, 139.99900, 167.99900, 195.99900,
    0.00000, 28.00000, 56.00000, 83.99900, 112.00000, 139.99900, 167.99900, 195.99900,
    0.00100, 28.00000, 56.00000, 84.00000, 112.00000, 140.00000, 168.00000, 196.00000,
    0.00100, 28.00000, 56.00100, 84.00000, 112.00100, 140.00000, 168.00000, 196.00000
]
    y_values = [
    0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000, 0.00000,
    28.00000, 28.00000, 28.00000, 28.00000, 28.00000, 28.00000, 28.00000, 28.00000,
    56.00000, 56.00100, 56.00000, 56.00000, 56.00000, 56.00000, 56.00000, 56.00000,
    84.00000, 84.00100, 84.00000, 84.00000, 84.00000, 84.00000, 84.00000, 84.00000
]
    # Čitaj podatke iz CSV datoteke i ubaci ih u treeview
    try:
        with open(file_path, newline='', encoding='utf-16') as csvfile:
            reader = csv.DictReader(csvfile)
            row_count = 0  # Broji retke
            for row in reader:
                if 'Name' in row and 'skew' in row['Name'].lower():
                    continue  # Preskoči red ako sadrži riječ "skew"
                x_error = float(row['X/r']) - x_values[row_count]
                y_error = float(row['Y/a']) - y_values[row_count]
                tree.insert("", tk.END, values=(
                    row['Name'], x_values[row_count], y_values[row_count], row['X/r'], row['Y/a'],
                    x_error, y_error
                ))
                row_count += 1
    except Exception as e:
        messagebox.showerror("Greška", f"Neuspjelo čitanje CSV datoteke: {e}")
        return

    # Automatski prilagodi širinu stupaca na temelju najdužeg podatka
    font = tkFont.Font(family="Helvetica", size=10)  # Inicijaliziraj font
    for col in tree['columns']:
        tree.column(col, width=font.measure(col))
        for row_id in tree.get_children():
            cell_value = tree.item(row_id)['values'][tree['columns'].index(col)]
            tree.column(col, width=max(tree.column(col)['width'], font.measure(str(cell_value))))

    # Prilagodi visinu prozora ovisno o broju redaka
    row_height = 25  # Visina jednog retka (ovisno o fontu i widgetu)
    max_rows_display = 25  # Maksimalan broj redaka za prikaz bez scroll bara
    displayed_rows = min(row_count, max_rows_display)  # Prikazani redci (maksimalno 20)

    window_height = 150 + (displayed_rows * row_height)  # Ukupna visina prozora (150 je za gornje elemente i gumbiće)
    report_window.geometry(f"800x{window_height}")  # Postavi visinu prozora

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

# Label za prikaz imena datoteke
filename_label = tk.Label(root, text="Nije odabrana datoteka", font=("Helvetica", 12))
filename_label.pack(pady=10)  # Postavi label u prozor

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

import tkinter as tk
from tkinter import ttk
import csv

# Učitaj podatke iz "grid.txt"
def ucitaj_grid_podatke():
    with open("grid.txt", "r") as f:
        grid_podaci = f.readlines()[1:]  # izbaci prvi red
    return grid_podaci

# Učitaj podatke iz "mjerenje nakon kalibracije_2.CSV"
def ucitaj_mjerenje_podatke():
    with open("mjerenje nakon kalibracije_2.CSV", newline="", encoding="utf-16") as csvfile:
        reader = csv.DictReader(csvfile)
        mjerenje_podaci = []
        for row in reader:
            if "Name" in row and "Skew" not in row["Name"]:
                mjerenje_podaci.append({k: v for k, v in row.items()})
    return mjerenje_podaci

# Prikaz podataka u tablici
def prikazi_podatke():
    grid_podaci = ucitaj_grid_podatke()
    mjerenje_podaci = ucitaj_mjerenje_podatke()

    tree = ttk.Treeview(root, show='headings', height=33)
    tree["columns"] = ("Name", "NOMINAL_X", "NOMINAL_Y", "X/r", "Y/a", "Error X", "Error Y")

    # Definiraj zaglavlja stupaca
    tree.column("Name", width=100, anchor=tk.CENTER)
    tree.heading("Name", text="Name")

    tree.column("NOMINAL_X", width=100, anchor=tk.CENTER)
    tree.heading("NOMINAL_X", text="NOMINAL_X")

    tree.column("NOMINAL_Y", width=100, anchor=tk.CENTER)
    tree.heading("NOMINAL_Y", text="NOMINAL_Y")

    tree.column("X/r", width=100, anchor=tk.CENTER)
    tree.heading("X/r", text="X/r")

    tree.column("Y/a", width=100, anchor=tk.CENTER)
    tree.heading("Y/a", text="Y/a")

    tree.column("Error X", width=100, anchor=tk.CENTER)
    tree.heading("Error X", text="Error X")

    tree.column("Error Y", width=100, anchor=tk.CENTER)
    tree.heading("Error Y", text="Error Y")

    # Prikaz podataka u tablici
    for i, row in enumerate(grid_podaci):
        dijelovi = row.strip().split(",")
        if len(dijelovi) == 2:
            nominal_x, nominal_y = dijelovi
            if i < len(mjerenje_podaci):
                mjerenje_row = mjerenje_podaci[i]
                error_x = abs(float(mjerenje_row["X/r"]) - float(nominal_x))
                error_y = abs(float(mjerenje_row["Y/a"]) - float(nominal_y))
                tree.insert("", tk.END, values=(
                    mjerenje_row["Name"],
                    format(float(nominal_x), ".4f"),
                    format(float(nominal_y), ".4f"),
                    format(float(mjerenje_row["X/r"]), ".4f"),
                    format(float(mjerenje_row["Y/a"]), ".4f"),
                    format(error_x, ".4f"),
                    format(error_y, ".4f")
                ))
            else:
                tree.insert("", tk.END, values=(
                    "",
                    format(float(nominal_x), ".4f"),
                    format(float(nominal_y), ".4f"),
                    "",
                    "",
                    "",
                    ""
                ))
        else:
            tree.insert("", tk.END, values=(
                "",
                "",
                "",
                "",
                "",
                "",
                ""
            ))
    for i in range(len(mjerenje_podaci) - len(grid_podaci)):
        mjerenje_row = mjerenje_podaci[i + len(grid_podaci)]
        tree.insert("", tk.END, values=(
            mjerenje_row["Name"],
            "",
            "",
            format(float(mjerenje_row["X/r"]), ".4f"),
            format(float(mjerenje_row["Y/a"]), ".4f"),
            "",
            ""
        ))

    tree.pack(fill='both', expand=True)

# Glavni prozor
root = tk.Tk()
root.title("Prikaz podataka")

# Prikaz podataka
prikazi_podatke()

# Pokreni glavni petlju
root.mainloop()



import tkinter as tk
from tkinter import ttk
import csv

# Učitaj podatke iz CSV datoteke
def ucitaj_podatke():
    with open("mjerenje nakon kalibracije_2.CSV", newline="", encoding="utf-16") as csvfile:
        reader = csv.DictReader(csvfile)
        podaci = []
        for row in reader:
            if "Name" in row and "Circle" in row["Name"]:
                podaci.append({"Name": row["Name"], "X/r": row["X/r"], "Y/a": row["Y/a"]})
    return podaci

# Učitaj podatke iz grit.txt
def ucitaj_nominal_podatke():
    with open("grid.txt", "r") as f:
        nominal_podaci = f.readlines()
    return nominal_podaci

# Prikaz podataka u tablici
def prikazi_podatke():
    podaci = ucitaj_podatke()
    nominal_podaci = ucitaj_nominal_podatke()
    tree = ttk.Treeview(root)
    tree["columns"] = ("Point", "NOMINAL_X", "NOMINAL_Y", "Actual X", "Actual Y", "Error_X", "Error_Y")

    # Definiraj zaglavlja stupaca
    tree.column("#0", width=50, stretch=tk.NO)
    tree.heading("#0", text="")

    tree.column("Point", width=50, anchor=tk.CENTER)
    tree.heading("Point", text="Point")

    tree.column("NOMINAL_X", width=100, anchor=tk.CENTER)
    tree.heading("NOMINAL_X", text="NOMINAL_X")

    tree.column("NOMINAL_Y", width=100, anchor=tk.CENTER)
    tree.heading("NOMINAL_Y", text="NOMINAL_Y")

    tree.column("Actual X", width=100, anchor=tk.CENTER)
    tree.heading("Actual X", text="Actual X")

    tree.column("Actual Y", width=100, anchor=tk.CENTER)
    tree.heading("Actual Y", text="Actual Y")

    tree.column("Error_X", width=100, anchor=tk.CENTER)
    tree.heading("Error_X", text="Error X")

    tree.column("Error_Y", width=100, anchor=tk.CENTER)
    tree.heading("Error_Y", text="Error Y")

    # Prikaz podataka u tablici
    for i, row in enumerate(podaci):
        tree.insert("", tk.END, values=(row["Name"], nominal_podaci[i*2].strip(), nominal_podaci[i*2+1].strip(), row["X/r"], row["Y/a"], "", ""))

    tree.pack()

# Glavni prozor
root = tk.Tk()
root.title("Prikaz podataka")

# Prikaz podataka
prikazi_podatke()

# Pokreni glavni petlju
root.mainloop()
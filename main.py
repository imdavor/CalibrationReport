import os
import platform
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

import chardet
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Spacer


def open_folder(path):
    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":  # macOS
        subprocess.Popen(["open", path])
    else:  # pretpostavljamo Linux
        subprocess.Popen(["xdg-open", path])


class CSVApp:
    def __init__(self, local_root):
        self.root = local_root
        self.root.title("CSV Učitavanje i PDF Spremanje")

        self.load_button = tk.Button(local_root, text="Učitaj CSV", command=self.load_csv)
        self.load_button.pack(pady=10)

        self.save_button = tk.Button(local_root, text="Spremi kao PDF", command=self.save_pdf)
        self.save_button.pack(pady=10)

        self.close_button = tk.Button(local_root, text="Zatvori", command=local_root.quit)
        self.close_button.pack(pady=10)

        self.data = None

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'rb') as f:
                result = chardet.detect(f.read())
                encoding = result['encoding']
            try:
                # Učitavanje CSV datoteke i isključivanje određenih kolumni
                self.data = pd.read_csv(file_path, encoding=encoding)
                columns_to_drop = ['Z', 'R', 'D', 'L', 'W', 'A', 'f', 'When']
                self.data.drop(columns=[col for col in columns_to_drop if col in self.data.columns], inplace=True)
                # Preimenuj kolumne
                self.data.rename(columns={'Name': 'Point', 'X/r': 'Nominal X/r', 'Y/a': 'Nominal Y/a'}, inplace=True)

                messagebox.showinfo("Uspjeh", "CSV datoteka učitana!")
            except Exception as e:
                messagebox.showerror("Greška", f"Nije moguće učitati datoteku: {e}")

    def load_grid_data(self, file_path):
        try:
            grid_data = pd.read_csv(file_path)
            return grid_data  # Vraća DataFrame
        except Exception as e:
            messagebox.showerror("Greška", f"Nije moguće učitati grid datoteku: {e}")
            return None

    def save_pdf(self):
        if self.data is not None:
            pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if pdf_path:
                try:
                    # Učitavanje podataka iz grid.txt
                    grid_data = self.load_grid_data(os.path.join(os.path.dirname(__file__),'grid.txt'))

                    # Provjerite da li je grid_data uspješno učitan
                    if grid_data is None:
                        return

                    # Stvaranje PDF dokumenta
                    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
                    elements = []

                    # Dodavanje loga na desnu stranu
                    logo_path = "logo.png"  # Promijenite ovo na stvarnu putanju do vašeg loga
                    logo = Image(logo_path, width=2 * inch, height=2 * inch)

                    # Koristimo Table za pozicioniranje loga
                    logo_table = Table([[logo]], colWidths=[doc.width])
                    logo_table.setStyle(TableStyle([
                        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 0.25 * inch),  # Mali odmak s desne strane
                    ]))

                    elements.append(Spacer(1, -1 * inch))  # Dodaje prazan prostor prije loga
                    elements.append(logo_table)

                    # Dodavanje malog razmaka ispod loga
                    elements.append(Spacer(1, 0.25 * inch))

                    # Dodavanje zaglavlja s crnom pozadinom
                    header_data = [["Topomatika d.o.o."]]  # Naziv tvrtke
                    header_table = Table(header_data, colWidths=[doc.width])
                    header_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, -1), colors.black),
                        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, -1), 14),
                        ('TOPPADDING', (0, 0), (-1, -1), 1),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                    ]))
                    elements.append(header_table)
                    elements.append(Spacer(1, 0 * inch))  # Razmak ispod zaglavlja

                    # Dodavanje prvog novog reda
                    new_row_1_data = [["Dep. Service/Calibration"]]  # Sadržaj prvog reda
                    new_row_1_table = Table(new_row_1_data, colWidths=[doc.width])
                    new_row_1_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
                        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                        ('FONTSIZE', (0, 0), (-1, -1), 8),
                        ('TOPPADDING', (0, 0), (-1, -1), 2),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                    ]))
                    elements.append(new_row_1_table)
                    elements.append(Spacer(1, 0.1 * inch))  # Razmak ispod prvog novog reda

                    # Dodavanje drugog novog reda
                    new_row_2_data = [["Measurement values (mm)"]]  # Sadržaj drugog reda
                    new_row_2_table = Table(new_row_2_data, colWidths=[doc.width])
                    new_row_2_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, -1), colors.white),
                        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Oblique'),  # Kurzivni tekst
                        ('FONTSIZE', (0, 0), (-1, -1), 12),
                        ('TOPPADDING', (0, 0), (-1, -1), 8),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ]))
                    elements.append(new_row_2_table)
                    elements.append(Spacer(1, 0.1 * inch))  # Razmak ispod drugog novog reda

                    # Spajanje X i Y vrijednosti u novu strukturu podataka
                    data = [["Point", "Nominal X", "Nominal Y"] + self.data.columns.tolist()[1:]]  # Dodavanje zaglavlja
                    for i, row in enumerate(grid_data.values.tolist()):
                        if i < len(self.data):
                            data.append([row[0], row[1], row[2]] + self.data.iloc[i].tolist()[1:])

                    table = Table(data)
                    table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 12),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica'),
                        ('FONTSIZE', (0, 0), (-1, 0), 10),
                        ('TOPPADDING', (0, 0), (-1, -1), 2),  # Smanjite padding iznad redova
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),  # Smanjite padding ispod redova
                        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                    ]))
                    elements.append(table)

                    # Spremanje PDF-a
                    doc.build(elements)
                    messagebox.showinfo("Uspjeh", "PDF je spremljen!")

                    # Otvaranje foldera gdje je datoteka spremljena
                    folder_path = os.path.dirname(pdf_path)
                    open_folder(folder_path)
                except Exception as e:
                    messagebox.showerror("Greška", f"Nije moguće spremiti PDF: {e}")
        else:
            messagebox.showwarning("Upozorenje", "Prvo učitaj CSV datoteku!")


if __name__ == "__main__":
    root = tk.Tk()
    # Postavite veličinu prozora
    width = 300
    height = 300
    root.geometry(f"{width}x{height}")

    # Izračunajte poziciju za centriranje
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # Postavite poziciju prozora
    root.geometry(f"{width}x{height}+{x}+{y}")
    app = CSVApp(root)
    root.mainloop()

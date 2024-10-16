import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import reportlab as plt


class CSVApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CSV Učitavanje i PDF Spremanje")

        self.load_button = tk.Button(root, text="Učitaj CSV", command=self.load_csv)
        self.load_button.pack(pady=10)

        self.save_button = tk.Button(root, text="Spremi kao PDF", command=self.save_pdf)
        self.save_button.pack(pady=10)

        self.close_button = tk.Button(root, text="Zatvori", command=root.quit)
        self.close_button.pack(pady=10)

        self.data = None

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                self.data = pd.read_csv(file_path)
                messagebox.showinfo("Uspjeh", "CSV datoteka učitana!")
            except Exception as e:
                messagebox.showerror("Greška", f"Nije moguće učitati datoteku: {e}")

    def save_pdf(self):
        if self.data is not None:
            pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if pdf_path:
                try:
                    # Generiraj grafikon za PDF
                    plt.figure(figsize=(10, 6))
                    plt.table(cellText=self.data.values, colLabels=self.data.columns, cellLoc='center', loc='center')
                    plt.axis('off')
                    plt.savefig(pdf_path, bbox_inches='tight')
                    plt.close()
                    messagebox.showinfo("Uspjeh", "PDF je spremljen!")
                except Exception as e:
                    messagebox.showerror("Greška", f"Nije moguće spremiti PDF: {e}")
        else:
            messagebox.showwarning("Upozorenje", "Prvo učitaj CSV datoteku!")


if __name__ == "__main__":
    root = tk.Tk()
    app = CSVApp(root)
    root.mainloop()

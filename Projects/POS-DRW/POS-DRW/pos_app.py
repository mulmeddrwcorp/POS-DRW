import tkinter as tk
from tkinter import ttk
import csv
import os
from tkinter import messagebox

# Contoh data produk statis
def load_products_from_csv(filename):
    products = []
    errors = []
    if not os.path.exists(filename):
        errors.append(f"File {filename} tidak ditemukan. Daftar produk kosong.")
        return products, errors
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                products.append({
                    'id': row['ID_Produk'],
                    'name': row['Nama_Produk'],
                    'price': int(row['Harga'])
                })
            except Exception as e:
                errors.append(f"Baris tidak valid: {row}, error: {e}")
    return products, errors

PRODUCTS = load_products_from_csv('produk.csv')

class POSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("POS Sederhana")
        self.geometry("600x400")
        self.resizable(False, False)
        self.cart = []
        self.products, self.load_errors = load_products_from_csv('produk.csv')
        if self.load_errors:
            messagebox.showerror("Error Produk", "\n".join(self.load_errors))
        self.create_widgets()

    def create_widgets(self):
        # Frame utama
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Frame kiri: Daftar Produk
        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ttk.Label(left_frame, text="Daftar Produk", font=("Arial", 12, "bold")).grid(row=0, column=0, pady=5, sticky="ew")
        self.product_listbox = tk.Listbox(left_frame, height=15)
        self.product_listbox.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        for product in self.products:
            self.product_listbox.insert(tk.END, f"{product['name']} - Rp{product['price']}")
        self.product_listbox.bind("<Double-Button-1>", self.on_product_click)
        add_btn = tk.Button(
            left_frame,
            text="Tambah ke Keranjang",
            command=self.add_to_cart,
            font=("Arial", 14, "bold"),
            height=2,
            width=20
        )
        add_btn.grid(row=2, column=0, pady=15, sticky="ew")
        left_frame.rowconfigure(1, weight=1)
        left_frame.columnconfigure(0, weight=1)

        # Frame kanan: Keranjang Belanja
        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        ttk.Label(right_frame, text="Keranjang Belanja", font=("Arial", 12, "bold")).grid(row=0, column=0, pady=5, sticky="ew")
        self.cart_listbox = tk.Listbox(right_frame, height=12)
        self.cart_listbox.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.total_label = ttk.Label(right_frame, text="Total Harga: Rp0", font=("Arial", 12, "bold"))
        self.total_label.grid(row=2, column=0, pady=(10, 5), sticky="ew")
        hitung_btn = ttk.Button(right_frame, text="Hitung Total", command=self.hitung_total)
        hitung_btn.grid(row=3, column=0, pady=(0, 5), sticky="ew")
        selesai_btn = ttk.Button(right_frame, text="Selesaikan & Cetak Struk", command=self.selesaikan_dan_cetak_struk)
        selesai_btn.grid(row=4, column=0, pady=(0, 10), sticky="ew")
        right_frame.rowconfigure(1, weight=1)
        right_frame.columnconfigure(0, weight=1)

    def add_to_cart(self):
        selected = self.product_listbox.curselection()
        if not selected:
            return
        idx = selected[0]
        product = self.products[idx]
        self.cart.append(product)
        self.cart_listbox.insert(tk.END, f"{product['name']} - Rp{product['price']}")

    def on_product_click(self, event):
        self.add_to_cart()

    def hitung_total(self):
        total = sum(item['price'] for item in self.cart)
        self.total_label.config(text=f"Total Harga: Rp{total}")

    def selesaikan_dan_cetak_struk(self):
        import datetime
        if not self.cart:
            return
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total = sum(item['price'] for item in self.cart)
        filename = f"struk_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("Struk Belanja\n")
            f.write(f"Waktu: {now}\n\n")
            f.write("Daftar Belanja:\n")
            for item in self.cart:
                f.write(f"- {item['name']} : Rp{item['price']}\n")
            f.write(f"\nTotal Harga: Rp{total}\n")
            f.write("\nTerima kasih!\n")
        # Reset keranjang dan total
        self.cart.clear()
        self.cart_listbox.delete(0, tk.END)
        self.total_label.config(text="Total Harga: Rp0")

if __name__ == "__main__":
    app = POSApp()
    app.mainloop() 
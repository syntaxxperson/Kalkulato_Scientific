import tkinter as tk
import math

# Fungsi untuk menangani input tombol
def klik_tombol(nilai):
    entri_layar.insert(tk.END, nilai)

# Fungsi untuk menghapus layar secara total (Clear)
def hapus_layar():
    entri_layar.delete(0, tk.END)

# Fungsi untuk menghapus satu karakter terakhir (Backspace)
def hapus_satu():
    posisi_sekarang = entri_layar.get()
    entri_layar.delete(0, tk.END)
    entri_layar.insert(tk.END, posisi_sekarang[:-1])

# Fungsi untuk menghitung hasil evaluasi matematika
def hitung():
    try:
        ekspresi = entri_layar.get()
        
        # Mengganti simbol visual menjadi fungsi matematika Python yang valid
        ekspresi = ekspresi.replace('x', '*')
        ekspresi = ekspresi.replace('^', '**')
        ekspresi = ekspresi.replace('π', 'math.pi')
        ekspresi = ekspresi.replace('e', 'math.e')
        
        # Mengevaluasi string ekspresi secara aman menggunakan fungsi matematika
        hasil = eval(ekspresi, {"__builtins__": None}, {
            "math": math,
            "sin": lambda x: math.sin(math.radians(x)),
            "cos": lambda x: math.cos(math.radians(x)),
            "tan": lambda x: math.tan(math.radians(x)),
            "log": math.log10
        })
        
        hapus_layar()
        entri_layar.insert(tk.END, str(hasil))
    except Exception as e:
        hapus_layar()
        entri_layar.insert(tk.END, "Tidak Valid")

# Inisialisasi jendela utama
app = tk.Tk()
app.title("Kalkulator Scientific")
app.geometry("400x550")
app.configure(bg="#202020")

# Input Layar Utama
entri_layar = tk.Entry(app, font=("Arial", 22), borderwidth=0, justify="right", fg="#ffffff", bg="#202020", insertbackground="white")
entri_layar.pack(fill=tk.BOTH, ipadx=8, ipady=20, padx=10, pady=10) 

# Frame khusus untuk menampung tombol agar rapi
frame_tombol = tk.Frame(app, bg="#202020")
frame_tombol.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

# Tata Letak Tombol (Layout Grid)
tombol_layout = [
    ['sin(', 'cos(', 'tan(', 'C'],
    ['log(', '^', ')', "⌫"],
    ['π', 'e', '(', '/'],
    ['7', '8', '9', 'x'],
    ['4', '5', '6','-'],
    ['1', '2', '3', '+'],
    ['0', '', '.','=']
]

# Konfigurasi warna tombol agar lebih estetis
warna_tombol = {
    "angka": {"bg": "#3b3b3b", "fg": "#ffffff"},
    "operator": {"bg": "#f39c12", "fg": "#ffffff"},
    "fungsi": {"bg": "#7f8c8d", "fg": "#ffffff"},
    "hapus": {"bg": "#c0392b", "fg": "#ffffff"}
}

# Membuat dan menyusun tombol ke dalam Grid secara dinamis
for baris_idx, baris in enumerate(tombol_layout):
    for kolom_idx, teks in enumerate(baris):
        if not teks:
            continue
            
        # Menentukan gaya warna berdasarkan jenis fungsi tombol
        if teks in ['C', '⌫']:
            gaya = warna_tombol["hapus"]
        elif teks in ['=', '+', '-', 'x', '/']:
            gaya = warna_tombol["operator"]
        elif teks.isdigit() or teks == '.':
            gaya = warna_tombol["angka"]
        else:
            gaya = warna_tombol["fungsi"]
            
        # Mengatur ukuran jangkauan kolom (column span) khusus tombol 0 dan '='
        colspan = 1
        rowspan = 1
        if teks == '0':
            colspan = 2
        elif teks == '=':
            rowspan = 4
            
        # Fungsi aksi spesifik untuk masing-masing tombol
        if teks == 'C':
            aksi = hapus_layar
        elif teks == '⌫':
            aksi = hapus_satu
        elif teks == '=':
            aksi = hitung
        else:
            aksi = lambda t=teks: klik_tombol(t)
            
        btn = tk.Button(frame_tombol, text=teks, font=("Arial", 14, "bold"), 
                        bg=gaya["bg"], fg=gaya["fg"], borderwidth=0, cursor="hand2", command=aksi)
        btn.grid(row=baris_idx, column=kolom_idx, columnspan=colspan, rowspan=rowspan, sticky="nsew", padx=3, pady=3)

# Mengatur agar tombol fleksibel mengikuti ukuran jendela saat di-resize
for i in range(7):
    frame_tombol.rowconfigure(i, weight=1)
for j in range(4):
    frame_tombol.columnconfigure(j, weight=1)

# Menjalankan aplikasi
app.mainloop()

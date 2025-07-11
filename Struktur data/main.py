import csv
from collections import deque

produk_dict = {}  # Hash Map
antrian_pembeli = deque()  # Queue
histori_transaksi = []  # Stack

# CSV
def load_produk():
    try:
        with open("produk.csv", mode="r", newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                produk_dict[int(row['id'])] = {
                    'nama': row['nama'],
                    'harga': int(row['harga']),
                    'stok': int(row['stok'])
                }
    except FileNotFoundError:
        with open("produk.csv", mode="w", newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'nama', 'harga', 'stok'])

def simpan_produk():
    with open("produk.csv", mode="w", newline='', encoding='utf-8') as file:
        fieldnames = ['id', 'nama', 'harga', 'stok']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for id_produk, data in produk_dict.items():
            writer.writerow({
                'id': id_produk,
                'nama': data['nama'],
                'harga': data['harga'],
                'stok': data['stok']
            })

# ===== CRUD Produk =====
def tambah_produk():
    try:
        id_produk = int(input("Masukkan ID produk: "))
        if id_produk in produk_dict:
            print("ID sudah digunakan.")
            return
        nama = input("Nama produk: ")
        harga = int(input("Harga: "))
        stok = int(input("Stok: "))
        produk_dict[id_produk] = {'nama': nama, 'harga': harga, 'stok': stok}
        simpan_produk()
        print("Produk berhasil ditambahkan.")
    except ValueError:
        print("Input tidak valid.")

def tampilkan_produk():
    if not produk_dict:
        print("Belum ada produk.")
        return
    print("\n=== Daftar Produk ===")
    for id_produk, data in produk_dict.items():
        print(f"ID: {id_produk} | Nama: {data['nama']} | Harga: {data['harga']} | Stok: {data['stok']}")
    print()

def ubah_produk():
    try:
        id_produk = int(input("Masukkan ID produk yang ingin diubah: "))
        if id_produk not in produk_dict:
            print("Produk tidak ditemukan.")
            return
        nama = input("Nama baru: ")
        harga = int(input("Harga baru: "))
        stok = int(input("Stok baru: "))
        produk_dict[id_produk] = {'nama': nama, 'harga': harga, 'stok': stok}
        simpan_produk()
        print("Produk berhasil diubah.")
    except ValueError:
        print("Input tidak valid.")

def hapus_produk():
    try:
        id_produk = int(input("Masukkan ID produk yang ingin dihapus: "))
        if id_produk in produk_dict:
            del produk_dict[id_produk]
            simpan_produk()
            print("Produk berhasil dihapus.")
        else:
            print("Produk tidak ditemukan.")
    except ValueError:
        print("Input tidak valid.")

# ===== Antrian Pembeli =====
def tambah_antrian():
    nama = input("Masukkan nama pembeli: ")
    antrian_pembeli.append(nama)
    print(f"{nama} masuk ke antrian.")

def layani_pembeli():
    if not antrian_pembeli:
        print("Tidak ada pembeli dalam antrian.")
        return

    nama = antrian_pembeli.popleft()
    print(f"\nMelayani {nama}")
    tampilkan_produk()
    try:
        id_produk = int(input("ID produk yang dibeli: "))
        jumlah = int(input("Jumlah: "))
        if id_produk in produk_dict:
            if produk_dict[id_produk]['stok'] >= jumlah:
                produk_dict[id_produk]['stok'] -= jumlah
                total = produk_dict[id_produk]['harga'] * jumlah
                print(f"Pembelian sukses. Total: Rp {total}")

                # Catat transaksi (Stack)
                transaksi = {
                    'pembeli': nama,
                    'produk': produk_dict[id_produk]['nama'],
                    'jumlah': jumlah,
                    'total': total
                }
                histori_transaksi.append(transaksi)

                simpan_produk()
            else:
                print("Stok tidak cukup.")
        else:
            print("Produk tidak ditemukan.")
    except ValueError:
        print("Input tidak valid.")

# ===== Histori Transaksi =====
def lihat_histori_transaksi():
    if not histori_transaksi:
        print("Belum ada transaksi.")
        return
    print("\n=== Histori Transaksi (Terbaru di atas) ===")
    for i, transaksi in enumerate(reversed(histori_transaksi), 1):
        print(f"{i}. {transaksi['pembeli']} membeli {transaksi['jumlah']}x {transaksi['produk']} - Total: Rp {transaksi['total']}")
    print()

# ===== Menu Utama =====
def menu():
    load_produk()
    while True:
        print("""
=== Manajemen Toko Roti ===
1. Tampilkan Produk
2. Tambah Produk
3. Ubah Produk
4. Hapus Produk
5. Tambah Antrian Pembeli
6. Layani Pembeli
7. Lihat Histori Transaksi
8. Keluar
        """)
        pilihan = input("Pilih menu (1-8): ")
        if pilihan == '1':
            tampilkan_produk()
        elif pilihan == '2':
            tambah_produk()
        elif pilihan == '3':
            ubah_produk()
        elif pilihan == '4':
            hapus_produk()
        elif pilihan == '5':
            tambah_antrian()
        elif pilihan == '6':
            layani_pembeli()
        elif pilihan == '7':
            lihat_histori_transaksi()
        elif pilihan == '8':
            print("Terima kasih telah menggunakan sistem manajemen toko roti.")
            break
        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    menu()

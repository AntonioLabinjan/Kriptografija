import tkinter as tk
from tkinter import filedialog
import barcode
from barcode.writer import ImageWriter
import qrcode

def generiraj_barkod():
    tekst = unos_polje.get()
    tip_barkoda = vrsta_barkoda.get()

    # Odabir klase barkoda ovisno o odabranom tipu
    if tip_barkoda == "EAN-13":
        kod = barcode.get_barcode_class('ean13')
    elif tip_barkoda == "Code128":
        kod = barcode.get_barcode_class('code128')
    else:
        status_label.config(text="Nepodržana vrsta barkoda")
        return

    # Provjera da li je klasa barkoda uspješno dohvaćena
    if kod is None:
        status_label.config(text="Greška pri dohvaćanju klase barkoda")
        return

    # Generiranje barkoda i spremanje slike
    kod_instance = kod(tekst, writer=ImageWriter())
    img = kod_instance.render()

    save_path = filedialog.asksaveasfilename(defaultextension=".png")
    if save_path:
        img.save(save_path)
        status_label.config(text="Barkod je uspješno spremljen u datoteku {}".format(save_path))

def generiraj_qr_kod():
    tekst = tekst_unos.get()

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(tekst)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    save_path = filedialog.asksaveasfilename(defaultextension=".png")
    if save_path:
        img.save(save_path)
        status_label.config(text=f"QR kod je uspješno spremljen u datoteku {save_path}")

# Stvaranje Tkinter aplikacije
root = tk.Tk()
root.title("Generator barkoda i QR koda")

# Polje za unos teksta za barkod
barkod_label = tk.Label(root, text="Unesite tekst za generiranje barkoda:")
barkod_label.pack()
unos_polje = tk.Entry(root)
unos_polje.pack()

# Odabir vrste barkoda
vrsta_barkoda_label = tk.Label(root, text="Odaberite vrstu barkoda:")
vrsta_barkoda_label.pack()
vrsta_barkoda = tk.StringVar()
vrsta_barkoda.set("EAN-13")  # Postavljamo početnu vrijednost
vrste_barkoda_optionmenu = tk.OptionMenu(root, vrsta_barkoda, "EAN-13", "Code128")
vrste_barkoda_optionmenu.pack()

# Gumb za generiranje barkoda
generiraj_barkod_gumb = tk.Button(root, text="Generiraj barkod", command=generiraj_barkod)
generiraj_barkod_gumb.pack()

# Polje za unos teksta za QR kod
qr_label = tk.Label(root, text="Unesite tekst ili URL za generiranje QR koda:")
qr_label.pack()
tekst_unos = tk.Entry(root)
tekst_unos.pack()

# Gumb za generiranje QR koda
generiraj_qr_gumb = tk.Button(root, text="Generiraj QR kod", command=generiraj_qr_kod)
generiraj_qr_gumb.pack()

# Statusna oznaka
status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()

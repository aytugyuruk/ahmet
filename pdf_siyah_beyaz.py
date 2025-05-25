import os
import tempfile
from tkinter import Tk, filedialog, messagebox, Button, Label
from pdf2image import convert_from_path
from PIL import Image, ImageEnhance
import pikepdf

# Uygulama klasöründeki poppler yolunu belirle
UYGULAMA_KLASORU = os.path.dirname(os.path.abspath(__file__))
POPLER_YOLU = os.path.join(UYGULAMA_KLASORU, "poppler-windows", "Library", "bin")

def sec_ve_donustur():
    pdf_yolu = filedialog.askopenfilename(title="PDF Seç", filetypes=[("PDF dosyaları", "*.pdf")])
    if not pdf_yolu:
        return

    try:
        messagebox.showinfo("İşlem Başladı", "PDF dönüştürülüyor. Lütfen bekleyin...")

        # Poppler path ile birlikte dönüştür
        sayfalar = convert_from_path(pdf_yolu, dpi=200, poppler_path=POPLER_YOLU)

        with tempfile.TemporaryDirectory() as tmpdir:
            img_paths = []
            for i, sayfa in enumerate(sayfalar):
                gri = sayfa.convert("L")  # Gri tonlama
                parlaklik = ImageEnhance.Brightness(gri).enhance(1.5)  # Parlaklık artır
                img_yolu = os.path.join(tmpdir, f"sayfa_{i}.png")
                parlaklik.save(img_yolu)
                img_paths.append(img_yolu)

            # PDF'e çevir
            pdf_cikti = os.path.join(tmpdir, "cikti.pdf")
            Image.open(img_paths[0]).save(
                pdf_cikti, save_all=True, append_images=[Image.open(p) for p in img_paths[1:]]
            )

            # Kullanıcıdan kayıt yeri al
            kayit_yolu = filedialog.asksaveasfilename(
                title="Kaydet", defaultextension=".pdf", filetypes=[("PDF dosyaları", "*.pdf")]
            )
            if not kayit_yolu:
                return

            with pikepdf.open(pdf_cikti) as pdf:
                pdf.save(kayit_yolu)

        messagebox.showinfo("Tamamlandı", "PDF başarıyla siyah-beyaza dönüştürüldü!")

    except Exception as e:
        messagebox.showerror("Hata", f"Bir hata oluştu:\n{e}")

# Arayüz
pencere = Tk()
pencere.title("PDF Siyah Beyaz Dönüştürücü")
pencere.geometry("400x150")

etiket = Label(pencere, text="PDF'yi siyah-beyaz ve parlak hale dönüştür", font=("Arial", 12))
etiket.pack(pady=20)

buton = Button(pencere, text="PDF Seç ve Dönüştür", command=sec_ve_donustur, bg="#4CAF50", fg="white", padx=10, pady=5)
buton.pack()

pencere.mainloop()
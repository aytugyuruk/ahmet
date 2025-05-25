import os
import tempfile
from tkinter import Tk, filedialog, messagebox, Button, Label
from pdf2image import convert_from_path
from PIL import Image, ImageEnhance
import pikepdf

def sec_ve_donustur():
    pdf_yolu = filedialog.askopenfilename(title="PDF Seç", filetypes=[("PDF dosyaları", "*.pdf")])
    if not pdf_yolu:
        return

    try:
        messagebox.showinfo("İşlem Başladı", "PDF dönüştürülüyor. Lütfen bekleyin...")

        # PDF'i görüntülere dönüştür
        sayfalar = convert_from_path(pdf_yolu, dpi=200)

        # Geçici klasör
        with tempfile.TemporaryDirectory() as tmpdir:
            img_paths = []
            for i, sayfa in enumerate(sayfalar):
                # Siyah beyaz ve parlaklık ayarı
                gri = sayfa.convert("L")  # Gri tonlamaya çevir
                parlaklik = ImageEnhance.Brightness(gri).enhance(1.5)  # Parlaklık artır
                img_yolu = os.path.join(tmpdir, f"sayfa_{i}.png")
                parlaklik.save(img_yolu)
                img_paths.append(img_yolu)

            # Görselleri yeni PDF olarak birleştir
            pdf_cikti = os.path.join(tmpdir, "cikti.pdf")
            Image.open(img_paths[0]).save(
                pdf_cikti, save_all=True, append_images=[Image.open(p) for p in img_paths[1:]]
            )

            # pikepdf ile optimize et ve kaydet
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

# Basit Arayüz
pencere = Tk()
pencere.title("PDF Siyah Beyaz Dönüştürücü")
pencere.geometry("400x150")

etiket = Label(pencere, text="PDF'yi siyah-beyaz ve parlak hale dönüştür", font=("Arial", 12))
etiket.pack(pady=20)

buton = Button(pencere, text="PDF Seç ve Dönüştür", command=sec_ve_donustur, bg="#4CAF50", fg="white", padx=10, pady=5)
buton.pack()

pencere.mainloop()
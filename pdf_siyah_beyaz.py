#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF Siyah Beyaz Dönüştürücü
Uygulamayı Yapan: Aytuğ Yürük
"""

import os
import sys
import tempfile
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pdf2image import convert_from_path
from PIL import Image, ImageEnhance
import pikepdf
from tkinter.font import Font

class PDFSiyahBeyazUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Siyah Beyaz Dönüştürücü")
        self.root.geometry("600x450")
        
        # Renk paleti
        self.ana_renk = "#3F51B5"  # Koyu mavi
        self.ikincil_renk = "#7986CB"  # Açık mavi
        self.vurgu_renk = "#FF4081"  # Pembe
        self.arka_plan = "#F5F5F5"  # Açık gri
        self.metin_renk = "#212121"  # Koyu gri
        self.buton_renk = "#3F51B5"  # Koyu mavi
        self.buton_hover = "#303F9F"  # Daha koyu mavi
        
        self.root.configure(bg=self.arka_plan)
        
        # Özel fontlar
        self.baslik_font = Font(family="Helvetica", size=18, weight="bold")
        self.buton_font = Font(family="Helvetica", size=11)
        self.etiket_font = Font(family="Helvetica", size=10)
        self.durum_font = Font(family="Helvetica", size=9, slant="italic")
        
        # Ana çerçeve
        self.ana_frame = tk.Frame(root, bg=self.arka_plan, padx=20, pady=20)
        self.ana_frame.pack(fill=tk.BOTH, expand=True)
        
        # Üst kısım - Başlık ve logo
        self.ust_frame = tk.Frame(self.ana_frame, bg=self.arka_plan)
        self.ust_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Uygulama başlığı
        self.baslik = tk.Label(
            self.ust_frame, 
            text="PDF Siyah Beyaz Dönüştürücü", 
            font=self.baslik_font,
            bg=self.arka_plan,
            fg=self.ana_renk
        )
        self.baslik.pack(pady=(10, 5))
        
        # Alt başlık
        self.alt_baslik = tk.Label(
            self.ust_frame,
            text="PDF dosyalarınızı kolayca siyah-beyaz formata dönüştürün",
            font=self.etiket_font,
            bg=self.arka_plan,
            fg=self.metin_renk
        )
        self.alt_baslik.pack(pady=(0, 5))
        
        # Geliştirici bilgisi
        self.gelistirici = tk.Label(
            self.ust_frame,
            text="Geliştiren: Aytuğ Yürük",
            font=self.durum_font,
            bg=self.arka_plan,
            fg=self.ikincil_renk
        )
        self.gelistirici.pack(pady=(0, 10))
        
        # Ayırıcı çizgi
        self.ayirici = ttk.Separator(self.ana_frame, orient="horizontal")
        self.ayirici.pack(fill=tk.X, pady=(0, 20))
        
        # Orta kısım - Dosya seçimi
        self.orta_frame = tk.Frame(self.ana_frame, bg=self.arka_plan)
        self.orta_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Dosya seçme butonu
        self.dosya_sec_buton = tk.Button(
            self.orta_frame, 
            text="PDF Dosyası Seç", 
            command=self.pdf_dosyasi_sec,
            font=self.buton_font,
            bg=self.buton_renk,
            fg="white",
            activebackground=self.buton_hover,
            activeforeground="white",
            padx=15,
            pady=8,
            relief=tk.FLAT,
            cursor="hand2"
        )
        self.dosya_sec_buton.pack(side=tk.LEFT, padx=(0, 10))
        
        # Seçilen dosya adı etiketi
        self.dosya_frame = tk.Frame(self.orta_frame, bg=self.arka_plan, bd=1, relief=tk.SOLID, padx=10, pady=8)
        self.dosya_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.dosya_adi_etiket = tk.Label(
            self.dosya_frame, 
            text="Henüz dosya seçilmedi", 
            font=self.etiket_font,
            bg=self.arka_plan,
            fg=self.metin_renk,
            anchor="w"
        )
        self.dosya_adi_etiket.pack(fill=tk.X)
        
        # Ayarlar çerçevesi
        self.ayarlar_frame = tk.LabelFrame(self.ana_frame, text="Görüntü Ayarları", bg=self.arka_plan, fg=self.ana_renk, font=self.etiket_font, padx=15, pady=15)
        self.ayarlar_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Kontrast değeri ayarı
        self.kontrast_frame = tk.Frame(self.ayarlar_frame, bg=self.arka_plan)
        self.kontrast_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.kontrast_etiket = tk.Label(
            self.kontrast_frame, 
            text="Kontrast:", 
            font=self.etiket_font,
            bg=self.arka_plan,
            fg=self.metin_renk,
            width=10,
            anchor="w"
        )
        self.kontrast_etiket.pack(side=tk.LEFT, padx=(0, 5))
        
        self.kontrast_deger = tk.DoubleVar(value=2.0)
        self.kontrast_slider = ttk.Scale(
            self.kontrast_frame,
            from_=1.0,
            to=3.0,
            orient=tk.HORIZONTAL,
            variable=self.kontrast_deger,
            length=300
        )
        self.kontrast_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.kontrast_deger_etiket = tk.Label(
            self.kontrast_frame,
            textvariable=self.kontrast_deger,
            font=self.etiket_font,
            bg=self.arka_plan,
            fg=self.metin_renk,
            width=3
        )
        self.kontrast_deger_etiket.pack(side=tk.LEFT, padx=(5, 0))
        
        # Parlaklık değeri ayarı
        self.parlaklik_frame = tk.Frame(self.ayarlar_frame, bg=self.arka_plan)
        self.parlaklik_frame.pack(fill=tk.X)
        
        self.parlaklik_etiket = tk.Label(
            self.parlaklik_frame, 
            text="Parlaklık:", 
            font=self.etiket_font,
            bg=self.arka_plan,
            fg=self.metin_renk,
            width=10,
            anchor="w"
        )
        self.parlaklik_etiket.pack(side=tk.LEFT, padx=(0, 5))
        
        self.parlaklik_deger = tk.DoubleVar(value=1.0)
        self.parlaklik_slider = ttk.Scale(
            self.parlaklik_frame,
            from_=0.5,
            to=2.0,
            orient=tk.HORIZONTAL,
            variable=self.parlaklik_deger,
            length=300
        )
        self.parlaklik_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.parlaklik_deger_etiket = tk.Label(
            self.parlaklik_frame,
            textvariable=self.parlaklik_deger,
            font=self.etiket_font,
            bg=self.arka_plan,
            fg=self.metin_renk,
            width=3
        )
        self.parlaklik_deger_etiket.pack(side=tk.LEFT, padx=(5, 0))
        
        # Alt kısım - Dönüştürme butonu ve durum
        self.alt_frame = tk.Frame(self.ana_frame, bg=self.arka_plan)
        self.alt_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Dönüştürme butonu
        self.donustur_buton = tk.Button(
            self.alt_frame, 
            text="Dönüştür", 
            command=self.pdf_donustur,
            font=self.buton_font,
            bg=self.vurgu_renk,
            fg="white",
            activebackground="#E91E63",  # Daha koyu pembe
            activeforeground="white",
            padx=20,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.donustur_buton.pack(pady=(0, 10))
        
        # Durum çerçevesi
        self.durum_frame = tk.Frame(self.alt_frame, bg=self.arka_plan, bd=1, relief=tk.SOLID, padx=10, pady=8)
        self.durum_frame.pack(fill=tk.X)
        
        # Durum etiketi
        self.durum_etiket = tk.Label(
            self.durum_frame, 
            text="Dönüştürme işlemi için lütfen bir PDF dosyası seçin", 
            font=self.durum_font,
            bg=self.arka_plan,
            fg=self.metin_renk
        )
        self.durum_etiket.pack()
        
        # Dosya yolu değişkeni
        self.pdf_dosya_yolu = None
        
    def pdf_dosyasi_sec(self):
        """PDF dosyası seçme işlemi"""
        dosya_yolu = filedialog.askopenfilename(
            title="PDF Dosyası Seç",
            filetypes=[("PDF Dosyaları", "*.pdf")]
        )
        
        if dosya_yolu:
            self.pdf_dosya_yolu = dosya_yolu
            dosya_adi = os.path.basename(dosya_yolu)
            self.dosya_adi_etiket.config(text=f"Seçilen dosya: {dosya_adi}")
            self.donustur_buton.config(state=tk.NORMAL)
            self.durum_etiket.config(text="Dosya seçildi. Dönüştürmek için 'Dönüştür' butonuna tıklayın.")
    
    def pdf_donustur(self):
        """PDF dosyasını siyah beyaz hale dönüştürme işlemi"""
        if not self.pdf_dosya_yolu:
            messagebox.showerror("Hata", "Lütfen önce bir PDF dosyası seçin!")
            return
        
        try:
            self.durum_etiket.config(text="Dönüştürme işlemi başladı...", fg=self.ana_renk)
            self.root.update()
            
            # Çıktı dosya yolunu belirle
            orijinal_dosya_adi = os.path.basename(self.pdf_dosya_yolu)
            dosya_adi, dosya_uzantisi = os.path.splitext(orijinal_dosya_adi)
            cikti_dosya_adi = f"{dosya_adi}_siyah_beyaz{dosya_uzantisi}"
            
            # Kaydetme yeri seç
            cikti_dosya_yolu = filedialog.asksaveasfilename(
                title="Dönüştürülmüş Dosyayı Kaydet",
                initialfile=cikti_dosya_adi,
                defaultextension=".pdf",
                filetypes=[("PDF Dosyaları", "*.pdf")]
            )
            
            if not cikti_dosya_yolu:
                self.durum_etiket.config(text="İşlem iptal edildi.", fg="#F44336")
                return
            
            # Kontrast ve parlaklık faktörlerini al
            kontrast_faktoru = self.kontrast_deger.get()
            parlaklik_faktoru = self.parlaklik_deger.get()
            
            # Geçici dizin oluştur
            with tempfile.TemporaryDirectory() as temp_dir:
                # PDF'yi görüntülere dönüştür
                self.durum_etiket.config(text="PDF sayfaları görüntülere dönüştürülüyor...", fg=self.ana_renk)
                self.root.update()
                
                # Windows icin poppler yolunu kontrol et
                try:
                    # Poppler yollarini kontrol et
                    poppler_paths = [
                        # EXE ile ayni dizinde
                        os.path.join(os.path.dirname(os.path.abspath(sys.executable)), "poppler-windows"),
                        # Mevcut calisma dizininde
                        os.path.join(os.getcwd(), "poppler-windows"),
                        # Script ile ayni dizinde
                        os.path.join(os.path.dirname(os.path.abspath(__file__)), "poppler-windows"),
                        # PyInstaller _MEIPASS
                        os.path.join(getattr(sys, '_MEIPASS', ''), "poppler-windows"),
                        # Dist klasorunde
                        os.path.join(os.path.dirname(os.path.abspath(sys.executable)), "dist", "poppler-windows"),
                        # Ust dizinde
                        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "poppler-windows"),
                    ]
                    
                    # Mevcut olan ilk poppler yolunu bul
                    poppler_path = None
                    for path in poppler_paths:
                        if os.path.exists(path):
                            poppler_path = path
                            print(f"Poppler bulundu: {path}")
                            break
                    
                    # Poppler yolu bulunamadiysa
                    if not poppler_path:
                        # Tum dizin yapisini goster
                        print("Poppler bulunamadi. Dizin yapisi:")
                        for path in poppler_paths:
                            print(f"Kontrol edilen yol: {path} - Var mi: {os.path.exists(path)}")
                        
                        # Eger Windows'ta calisiyorsak ve poppler bulunamadiysa
                        if sys.platform.startswith('win'):
                            # Poppler'i indirme ve kurma islemini baslat
                            messagebox.showinfo("Bilgi", "Poppler bulunamadi. Otomatik olarak indirilecek.")
                            self.durum_etiket.config(text="Poppler indiriliyor...", fg=self.ana_renk)
                            self.root.update()
                            
                            # Gecici dizin olustur
                            temp_poppler_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "poppler-windows")
                            os.makedirs(temp_poppler_dir, exist_ok=True)
                            
                            # Poppler'i indir
                            import urllib.request
                            import zipfile
                            
                            poppler_url = "https://github.com/oschwartz10612/poppler-windows/releases/download/v23.08.0-0/Release-23.08.0-0.zip"
                            zip_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "poppler.zip")
                            
                            try:
                                urllib.request.urlretrieve(poppler_url, zip_path)
                                
                                # Zip dosyasini cikar
                                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                                    zip_ref.extractall(os.path.dirname(os.path.abspath(__file__)))
                                
                                # Zip dosyasini sil
                                if os.path.exists(zip_path):
                                    os.remove(zip_path)
                                
                                poppler_path = temp_poppler_dir
                                self.durum_etiket.config(text="Poppler indirildi.", fg=self.ana_renk)
                                self.root.update()
                            except Exception as download_error:
                                messagebox.showerror("Hata", f"Poppler indirilemedi: {str(download_error)}")
                                raise e
                        else:
                            # Windows degilse
                            messagebox.showerror("Hata", "Poppler bulunamadi. Lutfen 'poppler-windows' klasorunun uygulama ile ayni dizinde oldugundan emin olun.")
                            raise e
                    
                    # PDF'yi goruntulere donustur
                    pdf_sayfalar = convert_from_path(self.pdf_dosya_yolu, poppler_path=poppler_path)
                except Exception as e:
                    # Hata goster
                    messagebox.showerror("Hata", f"PDF islenirken hata olustu: {str(e)}")
                    self.durum_etiket.config(text=f"Hata: {str(e)}", fg="#F44336")
                    raise e
                
                # Her sayfayı işle
                self.durum_etiket.config(text="Sayfalar siyah beyaz hale dönüştürülüyor...", fg=self.ana_renk)
                self.root.update()
                
                islenmiş_sayfalar = []
                for i, sayfa in enumerate(pdf_sayfalar):
                    # Görüntüyü siyah beyaz yap (doygunluğu sıfırla)
                    siyah_beyaz = sayfa.convert("L")  # L modu: grayscale
                    
                    # Parlaklığı ayarla
                    parlaklik_faktoru = self.parlaklik_deger.get()
                    parlaklik_artirici = ImageEnhance.Brightness(siyah_beyaz)
                    parlaklik_ayarlanmis = parlaklik_artirici.enhance(parlaklik_faktoru)
                    
                    # Kontrastı artır
                    kontrast_artirici = ImageEnhance.Contrast(parlaklik_ayarlanmis)
                    kontrast_arttirilmis = kontrast_artirici.enhance(kontrast_faktoru)
                    
                    # Geçici dosya olarak kaydet
                    gecici_sayfa_yolu = os.path.join(temp_dir, f"sayfa_{i}.png")
                    kontrast_arttirilmis.save(gecici_sayfa_yolu, "PNG")
                    islenmiş_sayfalar.append(gecici_sayfa_yolu)
                
                # İşlenmiş görüntüleri yeni bir PDF'ye dönüştür
                self.durum_etiket.config(text="Yeni PDF oluşturuluyor...", fg=self.ana_renk)
                self.root.update()
                
                # İlk sayfayı yükle
                ilk_sayfa = Image.open(islenmiş_sayfalar[0])
                ilk_sayfa_rgb = ilk_sayfa.convert("RGB")
                
                # Diğer sayfaları yükle
                diger_sayfalar = []
                for sayfa_yolu in islenmiş_sayfalar[1:]:
                    sayfa = Image.open(sayfa_yolu)
                    sayfa_rgb = sayfa.convert("RGB")
                    diger_sayfalar.append(sayfa_rgb)
                
                # PDF olarak kaydet
                ilk_sayfa_rgb.save(
                    cikti_dosya_yolu,
                    "PDF",
                    resolution=100.0,
                    save_all=True,
                    append_images=diger_sayfalar
                )
                
                self.durum_etiket.config(text=f"İşlem tamamlandı! Dosya kaydedildi: {os.path.basename(cikti_dosya_yolu)}", fg="#4CAF50")
                
                # Dönüştürme tamamlandıktan sonra başka bir dosya seçme seçeneği
                self.donustur_buton.config(state=tk.DISABLED)
                self.dosya_adi_etiket.config(text="Başka bir dosya seçmek için 'PDF Dosyası Seç' butonuna tıklayın")
                
                # Dosyayı göster
                messagebox.showinfo(
                    "İşlem Tamamlandı", 
                    f"PDF dosyası başarıyla dönüştürüldü ve kaydedildi:\n{cikti_dosya_yolu}"
                )
                
        except Exception as e:
            self.durum_etiket.config(text=f"Hata oluştu: {str(e)}", fg="#F44336")
            messagebox.showerror("Hata", f"İşlem sırasında bir hata oluştu:\n{str(e)}")


def ana_stil_ayarla():
    """ttk widget'ları için stil ayarları"""
    style = ttk.Style()
    style.theme_use('clam')  # Temel tema
    
    # Scale (slider) stili
    style.configure("TScale", background="#F5F5F5")
    style.map("TScale",
              background=[('active', '#F5F5F5')],
              troughcolor=[('active', '#7986CB'), ('!active', '#C5CAE9')])
    
    # Pencere başlık çubuğunda geliştirici bilgisi
    # Not: Bu özellik bazı platformlarda çalışmayabilir

if __name__ == "__main__":
    root = tk.Tk()
    ana_stil_ayarla()
    app = PDFSiyahBeyazUygulamasi(root)
    root.mainloop()

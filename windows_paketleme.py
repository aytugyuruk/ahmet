#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows icin PDF Siyah Beyaz Donusturucu paketleme scripti
Yazan: Aytug Yuruk
"""

# Karakter kodlamasi sorununu coz
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import os
import shutil
import subprocess
import zipfile
import urllib.request
from pathlib import Path

# Proje dizini
PROJE_DIZINI = os.path.dirname(os.path.abspath(__file__))

def poppler_indir():
    """Windows için Poppler indirme ve ayarlama"""
    print("Poppler Windows sürümü indiriliyor...")
    
    # Poppler Windows sürümü için URL
    poppler_url = "https://github.com/oschwartz10612/poppler-windows/releases/download/v23.08.0-0/Release-23.08.0-0.zip"
    
    # Poppler dizini
    poppler_dizini = os.path.join(PROJE_DIZINI, "poppler-windows")
    
    # Eğer poppler-windows dizini zaten varsa, silme
    if os.path.exists(poppler_dizini):
        print("Mevcut poppler-windows dizini temizleniyor...")
        shutil.rmtree(poppler_dizini)
    
    # Geçici zip dosyası
    zip_dosyasi = os.path.join(PROJE_DIZINI, "poppler-windows.zip")
    
    try:
        # Poppler'ı indir
        print(f"İndiriliyor: {poppler_url}")
        urllib.request.urlretrieve(poppler_url, zip_dosyasi)
        
        # Zip dosyasını çıkart
        print("Zip dosyası çıkartılıyor...")
        with zipfile.ZipFile(zip_dosyasi, 'r') as zip_ref:
            zip_ref.extractall(PROJE_DIZINI)
        
        # Zip dosyasını sil
        os.remove(zip_dosyasi)
        
        print("Poppler başarıyla indirildi ve ayarlandı.")
        return True
    except Exception as e:
        print(f"Poppler indirme hatası: {e}")
        return False

def exe_olustur():
    """Basit bir paketleme yaparak EXE yerine ZIP dosyasi olustur"""
    print("Windows icin paket olusturuluyor...")
    
    # Proje dizinini yazdir
    print(f"Proje dizini: {PROJE_DIZINI}")
    
    try:
        # Dist klasorunu olustur
        dist_path = os.path.join(PROJE_DIZINI, 'dist')
        os.makedirs(dist_path, exist_ok=True)
        
        # Calistirilabilir batch dosyasi olustur
        batch_path = os.path.join(dist_path, 'PDF_Siyah_Beyaz_Donusturucu.bat')
        with open(batch_path, 'w') as f:
            f.write('@echo off\n')
            f.write('echo PDF Siyah Beyaz Donusturucu baslatiliyor...\n')
            f.write('python pdf_siyah_beyaz.py\n')
            f.write('pause\n')
        
        # Gerekli dosyalari dist klasorune kopyala
        print("Gerekli dosyalar kopyalaniyor...")
        
        # Ana Python dosyasini kopyala
        shutil.copy(os.path.join(PROJE_DIZINI, 'pdf_siyah_beyaz.py'), dist_path)
        
        # requirements.txt dosyasini kopyala
        if os.path.exists(os.path.join(PROJE_DIZINI, 'requirements.txt')):
            shutil.copy(os.path.join(PROJE_DIZINI, 'requirements.txt'), dist_path)
        
        # Poppler klasorunu kopyala
        poppler_src = os.path.join(PROJE_DIZINI, 'poppler-windows')
        poppler_dst = os.path.join(dist_path, 'poppler-windows')
        if os.path.exists(poppler_src):
            if os.path.exists(poppler_dst):
                shutil.rmtree(poppler_dst)
            shutil.copytree(poppler_src, poppler_dst)
        
        # Kurulum talimatlari dosyasi olustur
        readme_path = os.path.join(dist_path, 'BENI_OKU.txt')
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write('PDF Siyah Beyaz Donusturucu - Kurulum Talimatlari\n')
            f.write('=============================================\n\n')
            f.write('1. Python 3.8 veya daha yeni bir surumu yukleyin (https://www.python.org/downloads/)\n')
            f.write('2. Komut istemini acin ve bu klasore gelin\n')
            f.write('3. Asagidaki komutu calistirarak gerekli kutuphaneleri yukleyin:\n')
            f.write('   pip install -r requirements.txt\n\n')
            f.write('4. Uygulamayi baslatmak icin PDF_Siyah_Beyaz_Donusturucu.bat dosyasina cift tiklayin\n')
        
        # ZIP dosyasi olustur
        zip_path = os.path.join(dist_path, 'PDF_Siyah_Beyaz_Donusturucu.zip')
        print(f"ZIP dosyasi olusturuluyor: {zip_path}")
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Batch dosyasini ekle
            zipf.write(batch_path, os.path.basename(batch_path))
            
            # Ana Python dosyasini ekle
            zipf.write(os.path.join(dist_path, 'pdf_siyah_beyaz.py'), 'pdf_siyah_beyaz.py')
            
            # requirements.txt dosyasini ekle
            if os.path.exists(os.path.join(dist_path, 'requirements.txt')):
                zipf.write(os.path.join(dist_path, 'requirements.txt'), 'requirements.txt')
            
            # BENI_OKU.txt dosyasini ekle
            zipf.write(readme_path, os.path.basename(readme_path))
            
            # Poppler klasorunu ekle
            if os.path.exists(poppler_dst):
                for root, dirs, files in os.walk(poppler_dst):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path, os.path.relpath(file_path, dist_path))
        
        print(f"Paket basariyla olusturuldu: {zip_path}")
        
        # Dist klasorunu listele
        print(f"Dist klasoru icerigi ({dist_path}):")
        for dosya in os.listdir(dist_path):
            dosya_yolu = os.path.join(dist_path, dosya)
            dosya_boyutu = os.path.getsize(dosya_yolu) if os.path.isfile(dosya_yolu) else "<klasor>"
            print(f"  - {dosya} ({dosya_boyutu} byte)")
        
        return True
    except Exception as e:
        print(f"Paket olusturma hatasi: {e}")
        # Dist klasorunu olustur ve hata dosyasi ekle
        dist_path = os.path.join(PROJE_DIZINI, 'dist')
        os.makedirs(dist_path, exist_ok=True)
        with open(os.path.join(dist_path, "error.txt"), "w") as f:
            f.write(f"Paketleme hatasi: {str(e)}")
        print(f"Hata dosyasi olusturuldu: {os.path.join(dist_path, 'error.txt')}")
        return False

def kurulum_dosyasi_olustur():
    """İsteğe bağlı: Inno Setup ile kurulum dosyası oluştur"""
    print("Bu işlevi Windows'ta Inno Setup yüklü olduğunda kullanabilirsiniz.")
    print("Inno Setup ile kurulum dosyası oluşturmak için Windows'ta bu scripti çalıştırın.")

def main():
    """Ana islev"""
    print("PDF Siyah Beyaz Donusturucu - Windows Paketleme Araci")
    print("=" * 50)
    
    # Windows'ta degilsek uyari ver
    if not sys.platform.startswith('win'):
        print("UYARI: Bu script Windows'ta calistirilmalidir.")
        print("Su anda Windows disinda bir platformdasiniz.")
        print("Windows'ta bu scripti calistirarak EXE dosyasi olusturabilirsiniz.")
        
        devam_et = input("Yine de devam etmek istiyor musunuz? (e/h): ")
        if devam_et.lower() != 'e':
            print("Islem iptal edildi.")
            return
    
    # Poppler indir
    if not poppler_indir():
        print("Poppler indirilemedi. İşlem iptal ediliyor.")
        return
    
    # EXE oluştur
    if not exe_olustur():
        print("EXE dosyası oluşturulamadı. İşlem iptal ediliyor.")
        return
    
    print("\nPaketleme islemi tamamlandi!")
    print("=" * 50)
    print("Kullanim Talimatlari:")
    print("1. 'dist' klasorundeki 'PDF_Siyah_Beyaz_Donusturucu.exe' dosyasini Windows'ta calistirabilirsiniz.")
    print("2. Bu EXE dosyasini istediginiz Windows bilgisayarina kopyalayabilirsiniz.")
    print("3. Kurulum gerektirmez, dogrudan calistirabilir.")
    print("=" * 50)

if __name__ == "__main__":
    main()

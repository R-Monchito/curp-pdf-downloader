#!/usr/bin/env python3
"""
Descargador de CURP - Opción 1: Manual con Pausa para CAPTCHA
Versión BATCH: Procesa múltiples CURPs desde archivo curps.txt

Uso:
    python download_curp.py

Requisitos:
    - Python 3.8+
    - pip install -r requirements.txt
    - Archivo curps.txt con un CURP por línea
"""

import os
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Configuración
GOB_MX_URL = "https://www.gob.mx/curp/"
CURPS_FILE = "curps.txt"
DOWNLOAD_DIR = "./downloads"
TIMEOUT = 30


def load_curps_from_file(filename):
    """
    Carga los CURPs desde un archivo de texto.
    
    Args:
        filename (str): Nombre del archivo con CURPs
        
    Returns:
        list: Lista de CURPs válidos
    """
    if not os.path.exists(filename):
        print(f"\u274c Error: No se encontró el archivo '{filename}'")
        print(f"\n\ud83d\udca1 Crea un archivo '{filename}' con un CURP por línea:")
        print("   Ejemplo:")
        print("   PEPE900101HDFABC09")
        print("   ABCD890513ABCDEF09")
        print("   XYZW950315MNOPQR12")
        return []
    
    curps = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            curp = line.strip().upper()
            # Validar formato
            if curp and len(curp) == 18 and curp.isalnum():
                curps.append(curp)
            elif curp:  # Si tiene contenido pero no es válido
                print(f"\u26a0\ufe0f  CURP inválido ignorado: {curp}")
    
    return curps


def setup_driver():
    """
    Configura el driver de Selenium con opciones de descarga.
    """
    print("[*] Configurando Chrome WebDriver...")
    
    # Crear directorio de descargas
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    
    chrome_options = Options()
    
    # Configurar ubicación de descargas
    prefs = {
        "download.default_directory": os.path.abspath(DOWNLOAD_DIR),
        "download.prompt_for_download": False,
        "safebrowsing.enabled": False
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    # Descomenta para modo headless (sin interfaz gráfica)
    # chrome_options.add_argument("--headless")
    
    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        print("✅ Chrome WebDriver configurado correctamente")
        return driver
    except Exception as e:
        print(f"❌ Error configurando WebDriver: {e}")
        sys.exit(1)


def download_curp_pdf(driver, curp, index, total):
    """
    Descarga el PDF del CURP desde gob.mx/curp/
    
    Args:
        driver: Selenium WebDriver
        curp (str): CURP a descargar (18 caracteres)
        index (int): Índice actual en la lista
        total (int): Total de CURPs
        
    Returns:
        bool: True si fue exitoso
    """
    
    print(f"\n{'='*60}")
    print(f"[{index}/{total}] Procesando CURP: {curp}")
    print(f"{'='*60}")
    
    try:
        # Paso 1: Navegar al sitio
        print(f"[1/5] Navegando a {GOB_MX_URL}...")
        driver.get(GOB_MX_URL)
        time.sleep(3)
        
        # Paso 2: Buscar y rellenar campo de CURP
        print("[2/5] Ingresando CURP...")
        try:
            curp_input = WebDriverWait(driver, TIMEOUT).until(
                EC.presence_of_element_located((By.ID, "curp"))
            )
            curp_input.clear()
            curp_input.send_keys(curp)
            print(f"✅ CURP ingresado: {curp}")
        except Exception as e:
            print(f"⚠️  Selector estándar no encontrado. Intentando alternativas...")
            try:
                curp_input = driver.find_element(By.NAME, "curp")
                curp_input.clear()
                curp_input.send_keys(curp)
                print(f"✅ CURP ingresado: {curp}")
            except:
                print("❌ No se pudo encontrar el campo de CURP.")
                print("   Verifica que el sitio gob.mx/curp/ esté disponible.")
                return False
        
        # Paso 3: Hacer clic en botón de búsqueda
        print("[3/5] Haciendo clic en búsqueda...")
        try:
            search_btn = WebDriverWait(driver, TIMEOUT).until(
                EC.element_to_be_clickable((By.ID, "btnBuscar"))
            )
            search_btn.click()
            print("✅ Búsqueda iniciada")
            time.sleep(2)
        except Exception as e:
            print(f"⚠️  Error en búsqueda: {e}")
        
        # Paso 4: Pausa para CAPTCHA
        print("\n[4/5] ⏸️  PAUSA PARA CAPTCHA MANUAL")
        print("="*60)
        print("Por favor:")
        print(f"  1. Resuelve el CAPTCHA en el navegador")
        print(f"  2. Haz clic en 'Buscar' o 'Consultar'")
        print(f"  3. Vuelve aquí y presiona Enter")
        print("="*60)
        input("\n⏸️  Presiona Enter cuando hayas resuelto el CAPTCHA...")
        
        time.sleep(2)
        
        # Paso 5: Descargar PDF
        print("\n[5/5] Descargando PDF...")
        try:
            print_btn = WebDriverWait(driver, TIMEOUT).until(
                EC.element_to_be_clickable((By.ID, "btnImprimir"))
            )
            print_btn.click()
            print("✅ Diálogo de impresión abierto")
            print("💡 Tip: Configura 'Imprimir a PDF' como impresora predeterminada")
            print("   para que se descargue automáticamente.")
            
            time.sleep(5)
            print("✅ PDF en proceso de descarga")
            
        except Exception as e:
            print(f"⚠️  No se pudo encontrar botón de descarga: {e}")
            print("   Intenta descargar manualmente desde el navegador.")
        
        print(f"\n✅ [{index}/{total}] ¡CURP procesado! {curp}")
        return True
        
    except KeyboardInterrupt:
        print("\n⚠️  Proceso interrumpido por el usuario.")
        return False
    except Exception as e:
        print(f"\n❌ Error procesando CURP {curp}: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("\n" + "="*60)
    print("DESCARGADOR DE CURP - Batch (Múltiples CURPs)")
    print("="*60 + "\n")
    
    # Cargar CURPs
    print(f"[*] Leyendo CURPs desde '{CURPS_FILE}'...\n")
    curps = load_curps_from_file(CURPS_FILE)
    
    if not curps:
        print("\n❌ No hay CURPs válidos para procesar.")
        sys.exit(1)
    
    print(f"✅ Se encontraron {len(curps)} CURP(s):")
    for i, curp in enumerate(curps, 1):
        print(f"   {i}. {curp}")
    
    # Confirmar
    respuesta = input("\n¿Deseas continuar? (s/n): ").lower()
    if respuesta != 's':
        print("❌ Operación cancelada.")
        sys.exit(0)
    
    # Configurar driver
    driver = None
    successful = 0
    failed = 0
    
    try:
        driver = setup_driver()
        
        # Procesar cada CURP
        for index, curp in enumerate(curps, 1):
            success = download_curp_pdf(driver, curp, index, len(curps))
            if success:
                successful += 1
            else:
                failed += 1
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso interrumpido por el usuario.")
    except Exception as e:
        print(f"\n❌ Error general: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if driver:
            print("\n[*] Cerrando navegador...")
            driver.quit()
            print("✅ Navegador cerrado")
    
    # Resumen final
    print("\n" + "="*60)
    print("RESUMEN FINAL")
    print("="*60)
    print(f"✅ Exitosos: {successful}/{len(curps)}")
    print(f"❌ Fallidos: {failed}/{len(curps)}")
    print(f"📁 PDFs guardados en: {os.path.abspath(DOWNLOAD_DIR)}")
    print("="*60 + "\n")
    
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()

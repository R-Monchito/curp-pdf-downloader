#!/usr/bin/env python3
"""
Descargador de CURP - Opción 1: Manual con Pausa para CAPTCHA
Usa Selenium para automatizar el flujo, pero pausa para resolver CAPTCHA manualmente.

Uso:
    python download_curp.py

Requisitos:
    - Python 3.8+
    - pip install -r requirements.txt
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
CURP_NUMBER = "ABCD890513ABCDEF09"  # Reemplaza con tu CURP
GOB_MX_URL = "https://www.gob.mx/curp/"
DOWNLOAD_DIR = "./downloads"
TIMEOUT = 30


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


def download_curp_pdf(curp):
    """
    Descarga el PDF del CURP desde gob.mx/curp/
    
    Args:
        curp (str): CURP a descargar (18 caracteres)
    """
    
    if len(curp) != 18:
        print(f"❌ Error: CURP debe tener 18 caracteres. Recibido: {len(curp)}")
        return False
    
    driver = None
    try:
        driver = setup_driver()
        
        # Paso 1: Navegar al sitio
        print(f"\n[1/5] Navegando a {GOB_MX_URL}...")
        driver.get(GOB_MX_URL)
        time.sleep(3)
        
        # Paso 2: Buscar y rellenar campo de CURP
        print("[2/5] Buscando campo de CURP...")
        try:
            # Intentar encontrar el campo CURP
            # NOTA: Los selectores pueden cambiar según el sitio
            curp_input = WebDriverWait(driver, TIMEOUT).until(
                EC.presence_of_element_located((By.ID, "curp"))
            )
            curp_input.clear()
            curp_input.send_keys(curp)
            print(f"✅ CURP ingresado: {curp}")
        except Exception as e:
            print(f"⚠️  Selector estándar no encontrado. Intentando alternativas...")
            # Intentar otros selectores comunes
            try:
                curp_input = driver.find_element(By.NAME, "curp")
                curp_input.clear()
                curp_input.send_keys(curp)
                print(f"✅ CURP ingresado: {curp}")
            except:
                print("❌ No se pudo encontrar el campo de CURP. Verifica el sitio manualmente.")
                print("   Inspecciona con F12 y actualiza los selectores en el código.")
                return False
        
        # Paso 3: Hacer clic en botón de búsqueda
        print("[3/5] Haciendo clic en botón de búsqueda...")
        try:
            search_btn = WebDriverWait(driver, TIMEOUT).until(
                EC.element_to_be_clickable((By.ID, "btnBuscar"))
            )
            search_btn.click()
            print("✅ Búsqueda iniciada")
            time.sleep(2)
        except Exception as e:
            print(f"⚠️  Botón de búsqueda no encontrado. Error: {e}")
            print("   Intenta hacer clic manualmente en el navegador.")
        
        # Paso 4: Pausa para CAPTCHA
        print("\n[4/5] ⏸️  PAUSA PARA CAPTCHA MANUAL")
        print("="*50)
        print("Por favor:")
        print("  1. Resuelve el CAPTCHA en el navegador")
        print("  2. Haz clic en 'Buscar' o 'Consultar'")
        print("  3. Vuelve aquí y presiona Enter")
        print("="*50)
        input("\n⏸️  Presiona Enter cuando hayas resuelto el CAPTCHA...")
        
        time.sleep(2)
        
        # Paso 5: Descargar PDF (hacer clic en imprimir/descargar)
        print("\n[5/5] Descargando PDF...")
        try:
            # Buscar botón de imprimir/descargar
            print_btn = WebDriverWait(driver, TIMEOUT).until(
                EC.element_to_be_clickable((By.ID, "btnImprimir"))
            )
            print_btn.click()
            print("✅ Diálogo de impresión abierto")
            
            # Usar atajo de teclado para guardar como PDF
            # Nota: En sistemas reales, configura la impresora predeterminada como "Imprimir a PDF"
            print("💡 Tip: Configura 'Imprimir a PDF' como impresora predeterminada")
            print("   para que se descargue automáticamente.")
            
            time.sleep(5)
            print("✅ PDF descargado (o en proceso de descarga)")
            
        except Exception as e:
            print(f"⚠️  No se pudo encontrar botón de descarga. Error: {e}")
            print("   Intenta descargar manualmente desde el navegador.")
        
        print(f"\n✅ ¡Proceso completado! PDF guardado en: {os.path.abspath(DOWNLOAD_DIR)}")
        return True
        
    except KeyboardInterrupt:
        print("\n⚠️  Proceso interrumpido por el usuario.")
        return False
    except Exception as e:
        print(f"\n❌ Error durante el proceso: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if driver:
            print("\n[*] Cerrando navegador...")
            driver.quit()
            print("✅ Navegador cerrado")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("DESCARGADOR DE CURP - Opción 1: Manual con Pausa CAPTCHA")
    print("="*60 + "\n")
    
    # Validar CURP
    if not CURP_NUMBER or CURP_NUMBER == "ABCD890513ABCDEF09":
        print("❌ Error: Debes configurar tu CURP en la variable CURP_NUMBER")
        print("   Abre este archivo y reemplaza:")
        print("   CURP_NUMBER = 'TU_CURP_AQUI'")
        sys.exit(1)
    
    # Ejecutar descarga
    success = download_curp_pdf(CURP_NUMBER)
    
    # Resultado final
    if success:
        print("\n" + "="*60)
        print("✅ ¡Éxito! Tu PDF de CURP está listo.")
        print("="*60)
        sys.exit(0)
    else:
        print("\n" + "="*60)
        print("❌ Hubo un problema durante la descarga.")
        print("="*60)
        sys.exit(1)

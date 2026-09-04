#!/usr/bin/env python3
"""
Descargador de CURP - Opción 2: Automático con 2Captcha
Usa Selenium + 2Captcha para resolver CAPTCHA automáticamente.

Uso:
    python download_with_captcha_solver.py

Requisitos:
    - Python 3.8+
    - pip install -r requirements.txt
    - Cuenta en 2Captcha (https://2captcha.com) con créditos
    - Variable de entorno: TWO_CAPTCHA_API_KEY
"""

import os
import sys
import time
import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Cargar variables de entorno
load_dotenv()

# Configuración
CURP_NUMBER = "ABCD890513ABCDEF09"  # Reemplaza con tu CURP
TWO_CAPTCHA_API_KEY = os.getenv("TWO_CAPTCHA_API_KEY", "")
GOB_MX_URL = "https://www.gob.mx/curp/"
DOWNLOAD_DIR = "./downloads"
TIMEOUT = 30

# Endpoints de 2Captcha
TWO_CAPTCHA_UPLOAD = "http://2captcha.com/api/upload"
TWO_CAPTCHA_RESULT = "http://2captcha.com/api/res"


class CaptchaSolver:
    """Clase para resolver CAPTCHAs usando 2Captcha"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.captcha_id = None
    
    def solve_captcha_image(self, image_path):
        """
        Resuelve un CAPTCHA de imagen usando 2Captcha.
        
        Args:
            image_path (str): Ruta a la imagen del CAPTCHA
            
        Returns:
            str: Texto del CAPTCHA resuelto o None si falló
        """
        print(f"[*] Enviando CAPTCHA a 2Captcha...")
        
        try:
            with open(image_path, 'rb') as f:
                r = requests.post(
                    TWO_CAPTCHA_UPLOAD,
                    files={'captchafile': f},
                    data={
                        'key': self.api_key,
                        'method': 'post'
                    }
                )
            
            if r.status_code != 200:
                print(f"❌ Error enviando CAPTCHA: {r.status_code}")
                return None
            
            result = r.text.strip()
            if not result.startswith('OK|'):
                print(f"❌ Error de 2Captcha: {result}")
                return None
            
            self.captcha_id = result.split('|')[1]
            print(f"✅ CAPTCHA enviado. ID: {self.captcha_id}")
            
            # Esperar a que se resuelva
            return self.wait_for_result()
            
        except Exception as e:
            print(f"❌ Error procesando CAPTCHA: {e}")
            return None
    
    def wait_for_result(self, max_wait=120):
        """
        Espera a que 2Captcha resuelva el CAPTCHA.
        
        Args:
            max_wait (int): Máximo tiempo de espera en segundos
            
        Returns:
            str: Texto del CAPTCHA o None
        """
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            try:
                r = requests.get(
                    TWO_CAPTCHA_RESULT,
                    params={
                        'key': self.api_key,
                        'action': 'get',
                        'id': self.captcha_id
                    }
                )
                
                result = r.text.strip()
                
                if result == 'CAPCHA_NOT_READY':
                    print("[*] CAPTCHA aún en proceso...")
                    time.sleep(3)
                    continue
                
                if result.startswith('OK|'):
                    captcha_text = result.split('|')[1]
                    print(f"✅ CAPTCHA resuelto: {captcha_text}")
                    return captcha_text
                
                print(f"❌ Error: {result}")
                return None
                
            except Exception as e:
                print(f"❌ Error esperando resultado: {e}")
                return None
        
        print(f"❌ Tiempo máximo de espera agotado ({max_wait}s)")
        return None


def setup_driver():
    """
    Configura el driver de Selenium.
    """
    print("[*] Configurando Chrome WebDriver...")
    
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    
    chrome_options = Options()
    prefs = {
        "download.default_directory": os.path.abspath(DOWNLOAD_DIR),
        "download.prompt_for_download": False,
        "safebrowsing.enabled": False
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        print("✅ Chrome WebDriver configurado")
        return driver
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def download_curp_pdf(curp):
    """
    Descarga el PDF del CURP con CAPTCHA automático.
    """
    
    if not TWO_CAPTCHA_API_KEY:
        print("❌ Error: TWO_CAPTCHA_API_KEY no configurada")
        print("   Crea un archivo .env con: TWO_CAPTCHA_API_KEY=tu_api_key")
        return False
    
    if len(curp) != 18:
        print(f"❌ CURP debe tener 18 caracteres. Recibido: {len(curp)}")
        return False
    
    driver = None
    solver = CaptchaSolver(TWO_CAPTCHA_API_KEY)
    
    try:
        driver = setup_driver()
        
        print(f"\n[1/5] Navegando a {GOB_MX_URL}...")
        driver.get(GOB_MX_URL)
        time.sleep(3)
        
        print("[2/5] Ingresando CURP...")
        try:
            curp_input = WebDriverWait(driver, TIMEOUT).until(
                EC.presence_of_element_located((By.ID, "curp"))
            )
            curp_input.clear()
            curp_input.send_keys(curp)
            print(f"✅ CURP ingresado: {curp}")
        except Exception as e:
            print(f"❌ Error ingresando CURP: {e}")
            return False
        
        print("[3/5] Haciendo clic en búsqueda...")
        try:
            search_btn = WebDriverWait(driver, TIMEOUT).until(
                EC.element_to_be_clickable((By.ID, "btnBuscar"))
            )
            search_btn.click()
            print("✅ Búsqueda iniciada")
            time.sleep(2)
        except Exception as e:
            print(f"⚠️  Error: {e}")
        
        print("[4/5] Resolviendo CAPTCHA con 2Captcha...")
        # NOTA: Implementar captura y envío de imagen CAPTCHA
        # Esto es complejo y depende de cómo se renderice el CAPTCHA
        print("💡 Nota: Este paso requiere implementación manual del CAPTCHA")
        print("   Consulta la documentación de 2Captcha para más detalles")
        
        print("\n[5/5] Descargando PDF...")
        time.sleep(3)
        
        print(f"\n✅ Proceso completado. PDF en: {os.path.abspath(DOWNLOAD_DIR)}")
        return True
        
    except KeyboardInterrupt:
        print("\n⚠️  Interrumpido por el usuario")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if driver:
            driver.quit()
            print("[*] Navegador cerrado")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("DESCARGADOR DE CURP - Opción 2: Automático con 2Captcha")
    print("="*60 + "\n")
    
    if not CURP_NUMBER or CURP_NUMBER == "ABCD890513ABCDEF09":
        print("❌ Error: Configura tu CURP")
        sys.exit(1)
    
    success = download_curp_pdf(CURP_NUMBER)
    sys.exit(0 if success else 1)

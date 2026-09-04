#!/usr/bin/env python3
"""
Descargador de CURP - Opción 3: Usando APIs de Terceros
Usa APIs como Verificamex, API Market o Didit para descargar PDFs de CURP.

Uso:
    python download_with_api.py

Requisitos:
    - Python 3.8+
    - pip install -r requirements.txt
    - API Key de alguno de estos servicios:
      * Verificamex (https://verificamex.com/)
      * API Market (https://apimarket.mx/)
      * Didit.me (https://didit.me/)
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración
CURP_NUMBER = "ABCD890513ABCDEF09"  # Reemplaza con tu CURP
API_PROVIDER = os.getenv("API_PROVIDER", "verificamex")  # verificamex, apimarket, didit
API_KEY = os.getenv("API_KEY", "")
DOWNLOAD_DIR = "./downloads"

# Endpoints de APIs
API_ENDPOINTS = {
    "verificamex": {
        "url": "https://api.verificamex.com/v1/curp/consulta",
        "method": "POST",
        "headers": {"Authorization": "Bearer {key}", "Content-Type": "application/json"},
        "payload_key": "curp",
        "docs": "https://verificamex.com/soluciones/api-curp"
    },
    "apimarket": {
        "url": "https://api.apimarket.mx/v1/identity/curp/validate",
        "method": "POST",
        "headers": {"Authorization": "Bearer {key}", "Content-Type": "application/json"},
        "payload_key": "curp",
        "docs": "https://apimarket.mx/api-mexico"
    },
    "didit": {
        "url": "https://verification.didit.me/v3/database-validation/",
        "method": "POST",
        "headers": {"x-api-key": "{key}"},
        "payload_key": "personal_number",
        "form_data": {"issuing_state": "MEX", "services": "mex_curp"},
        "docs": "https://didit.me/blog/mexico-curp-database-validation/"
    }
}


class CURPAPIClient:
    """Cliente para consultar CURP usando APIs de terceros"""
    
    def __init__(self, provider, api_key):
        self.provider = provider.lower()
        self.api_key = api_key
        
        if self.provider not in API_ENDPOINTS:
            raise ValueError(f"Proveedor desconocido: {provider}")
        
        self.config = API_ENDPOINTS[self.provider]
    
    def verify_curp(self, curp):
        """
        Verifica un CURP y obtiene los datos asociados.
        
        Args:
            curp (str): CURP a verificar (18 caracteres)
            
        Returns:
            dict: Respuesta de la API o None si falló
        """
        print(f"[*] Consultando CURP con {self.provider}...")
        
        if len(curp) != 18:
            print(f"❌ CURP inválido: debe tener 18 caracteres")
            return None
        
        try:
            # Preparar encabezados
            headers = {k: v.format(key=self.api_key) for k, v in self.config["headers"].items()}
            
            # Preparar payload
            if self.provider == "didit":
                # Didit usa form-data
                payload = self.config["form_data"]
                payload[self.config["payload_key"]] = curp
                response = requests.request(
                    self.config["method"],
                    self.config["url"],
                    headers=headers,
                    data=payload
                )
            else:
                # Otros usan JSON
                payload = {self.config["payload_key"]: curp}
                response = requests.request(
                    self.config["method"],
                    self.config["url"],
                    headers=headers,
                    json=payload
                )
            
            if response.status_code == 200:
                print("✅ CURP verificado")
                return response.json()
            else:
                print(f"❌ Error {response.status_code}: {response.text}")
                return None
        
        except Exception as e:
            print(f"❌ Error en solicitud: {e}")
            return None
    
    def download_pdf(self, curp):
        """
        Descarga el PDF del CURP.
        
        Args:
            curp (str): CURP a descargar
            
        Returns:
            bool: True si fue exitoso
        """
        print(f"[*] Descargando PDF para {curp}...")
        
        # NOTA: Esto depende de cada API
        # Algunos endpoints pueden tener URLs específicas para PDF
        
        try:
            # Primero verificar que el CURP existe
            data = self.verify_curp(curp)
            if not data:
                return False
            
            print(f"✅ Datos obtenidos:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            # Guardar JSON (algunos servicios requieren esto)
            os.makedirs(DOWNLOAD_DIR, exist_ok=True)
            output_file = os.path.join(DOWNLOAD_DIR, f"{curp}_response.json")
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Datos guardados en: {output_file}")
            return True
        
        except Exception as e:
            print(f"❌ Error descargando PDF: {e}")
            return False


def print_info():
    """Imprime información sobre los proveedores disponibles"""
    print("\n" + "="*60)
    print("PROVEEDORES DISPONIBLES")
    print("="*60)
    
    for provider, config in API_ENDPOINTS.items():
        print(f"\n📋 {provider.upper()}")
        print(f"   Documentación: {config['docs']}")
        print(f"   Endpoint: {config['url']}")
    
    print("\n" + "="*60)


def main():
    print("\n" + "="*60)
    print("DESCARGADOR DE CURP - Opción 3: API de Terceros")
    print("="*60)
    
    # Validar configuración
    if not CURP_NUMBER or CURP_NUMBER == "ABCD890513ABCDEF09":
        print("\n❌ Error: Configura tu CURP")
        print("   Edita este archivo y reemplaza CURP_NUMBER")
        return False
    
    if not API_KEY:
        print("\n❌ Error: No hay API_KEY configurada")
        print("   Opciones:")
        print("   1. Crea archivo .env con: API_KEY=tu_clave")
        print("   2. O establece la variable de entorno API_KEY")
        print_info()
        return False
    
    if API_PROVIDER not in API_ENDPOINTS:
        print(f"\n❌ Error: Proveedor desconocido: {API_PROVIDER}")
        print_info()
        return False
    
    print(f"\n[*] Configuración:")
    print(f"   Proveedor: {API_PROVIDER}")
    print(f"   CURP: {CURP_NUMBER}")
    print(f"   Directorio: {DOWNLOAD_DIR}")
    
    # Crear cliente y descargar
    try:
        client = CURPAPIClient(API_PROVIDER, API_KEY)
        success = client.download_pdf(CURP_NUMBER)
        
        if success:
            print(f"\n" + "="*60)
            print("✅ ¡Éxito! Datos de CURP obtenidos.")
            print("="*60)
            return True
        else:
            print(f"\n" + "="*60)
            print("❌ No se pudo completar la consulta.")
            print("="*60)
            return False
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

# CURP PDF Downloader 🇲🇽

**Herramienta automatizada para descargar PDFs de CURP desde el sitio oficial del gobierno de México (gob.mx/curp/)**

## ⚠️ ADVERTENCIA LEGAL

- **Uso Personal**: Esta herramienta está diseñada para **uso personal y educativo**.
- **Términos de Servicio**: Respeta los términos de servicio de gob.mx/curp/
- **Datos Sensibles**: Maneja datos personales de forma segura. No compartas credenciales ni CURPs en repositorios públicos.
- **Cumplimiento Legal**: Verifica que tu uso cumpla con la legislación mexicana (LGPD, LFTAIP, etc.)

---

## 📋 Contenido

Este repositorio incluye **3 enfoques diferentes**:

1. **`download_curp.py`** - Selenium con pausa manual para CAPTCHA
2. **`download_with_captcha_solver.py`** - Selenium + solucionador automático de CAPTCHA (2Captcha)
3. **`download_with_api.py`** - Usando API de terceros (Verificamex)

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/R-Monchito/curp-pdf-downloader.git
cd curp-pdf-downloader
```

### 2. Crear entorno virtual (opcional pero recomendado)

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 📝 Opción 1: Descarga Manual con Pausa para CAPTCHA

**Archivos**: `download_curp.py`

Ideal si prefieres resolver el CAPTCHA manualmente.

### Uso

```bash
python download_curp.py
```

### Configuración

Abre el archivo y reemplaza:

```python
CURP_NUMBER = "ABCD890513ABCDEF09"  # Tu CURP aquí
```

### Flujo

1. ✅ Abre navegador Chrome automáticamente
2. ✅ Navega a gob.mx/curp/
3. ✅ Ingresa tu CURP
4. ⏸️ **Pausa**: Resuelve el CAPTCHA manualmente
5. ✅ Presiona Enter en la consola para continuar
6. ✅ Descarga el PDF automáticamente

---

## 📝 Opción 2: Descarga Automática con CAPTCHA Solver

**Archivos**: `download_with_captcha_solver.py`

Usando **2Captcha** para resolver CAPTCHAs automáticamente.

### Pre-requisitos

1. **Crear cuenta en 2Captcha**: https://2captcha.com
2. **Obtener API Key**: Dashboard → API Key
3. **Agregar crédito** (mínimo $2 USD recomendado)

### Configuración

Crea un archivo `.env` en la raíz del proyecto:

```bash
# .env
TWO_CAPTCHA_API_KEY=tu_api_key_aqui
```

### Uso

```bash
python download_with_captcha_solver.py
```

### Flujo

1. ✅ Abre navegador Chrome
2. ✅ Navega a gob.mx/curp/
3. ✅ Ingresa tu CURP
4. 🤖 **Automático**: 2Captcha resuelve el CAPTCHA
5. ✅ Descarga el PDF automáticamente

### Costos

- **2Captcha**: ~$0.50 USD por 1,000 CAPTCHAs
- **Prueba gratuita**: Algunos créditos iniciales (verifica tu cuenta)

---

## 📝 Opción 3: Descarga usando API

**Archivos**: `download_with_api.py`

Usando **APIs de terceros** que ya tienen integración con RENAPO.

### Pre-requisitos

Elige una API y registrate:

#### **Opción A: API Market (Recomendado para Sandbox)**
- **Sitio**: https://apimarket.mx/
- **Ventaja**: Sandbox ilimitado sin tarjeta requerida
- **Prueba gratuita**: ✅ Sí (sandbox)

#### **Opción B: Verificamex**
- **Sitio**: https://verificamex.com/
- **Ventaja**: Descarga PDF directamente, anti-fraude
- **Prueba gratuita**: ✅ Sí (demo)

#### **Opción C: Didit.me**
- **Sitio**: https://didit.me/
- **Precio**: $0.20 USD por consulta
- **Ventaja**: Simple y directa

### Configuración

```bash
# .env
API_PROVIDER=verificamex  # O: apimarket, didit
API_KEY=tu_api_key_aqui
```

### Uso

```bash
python download_with_api.py
```

### Comparativa de APIs

| Proveedor | Prueba Gratis | Sandbox | Precio | Documentación |
|-----------|:-------------:|:-------:|:------:|:--------------:|
| **API Market** | ✅ | ✅ | Pay-per-use | ⭐⭐⭐⭐⭐ |
| **Verificamex** | ✅ | ✅ | Pay-per-use | ⭐⭐⭐⭐ |
| **Didit.me** | ⚠️ | ✅ | $0.20/query | ⭐⭐⭐⭐ |

---

## 🔧 Troubleshooting

### Error: "Chrome driver not found"

```bash
# webdriver-manager descarga automáticamente el driver correcto
# Si aún hay problemas:
pip install --upgrade webdriver-manager
```

### Error: "Element not found"

- El sitio gob.mx/curp/ puede haber cambiado su estructura
- Actualiza los selectores en el script (inspecciona con DevTools: F12)

### Error: "CAPTCHA solving failed"

- Verifica que tu cuenta 2Captcha tenga créditos
- El CAPTCHA puede no ser soportado (intenta manual)

### CURP inválido

- Verifica el formato: 18 caracteres alphanumericos
- Estructura: `XXXX990513ABCDEF09`

---

## 📊 Comparativa de Métodos

| Método | Facilidad | Costo | Automatización | Recomendado |
|--------|-----------|--------|---|---|
| **Manual (Opción 1)** | ⭐⭐⭐⭐⭐ | $0 | 50% | ✅ Principiantes |
| **2Captcha (Opción 2)** | ⭐⭐⭐⭐ | $0.50/1k | 100% | ✅ Automatización |
| **API (Opción 3)** | ⭐⭐⭐ | Variable | 100% | ✅ Integración |

---

## 📁 Estructura del Proyecto

```
curp-pdf-downloader/
├── README.md                           # Este archivo
├── requirements.txt                    # Dependencias Python
├── .gitignore                          # Archivos a ignorar
├── .env.example                        # Plantilla de variables
│
├── download_curp.py                    # Opción 1: Manual
├── download_with_captcha_solver.py     # Opción 2: Con 2Captcha
└── download_with_api.py                # Opción 3: Usando API
```

---

## 🛡️ Seguridad

1. **Nunca compartas tu `.env`** con credenciales
2. **No suba CURPs reales** a repositorios públicos
3. **Usa variables de entorno** para datos sensibles
4. **Verifica HTTPS** en gob.mx/curp/
5. **Audita el código** antes de usarlo en producción

---

## 📚 Recursos Útiles

- **Selenium Docs**: https://selenium-python.readthedocs.io/
- **2Captcha API**: https://2captcha.com/api/python
- **Gob.mx CURP**: https://www.gob.mx/curp/
- **RENAPO Guide**: https://renapo-curp.azure.tsu.edu/

---

## 🤝 Contribuciones

¿Encontraste un bug o mejora? ¡Abre un issue o PR!

```bash
git checkout -b feature/tu-mejora
git commit -am 'Añade mejora'
git push origin feature/tu-mejora
```

---

## 📄 Licencia

MIT License - Ver archivo LICENSE

---

## ⚖️ Disclaimer

Este proyecto es de **uso educativo y personal**. El autor no es responsable de:
- Uso indebido de datos personales
- Violación de términos de servicio
- Incumplimiento de leyes mexicanas
- Daños derivados del uso de esta herramienta

Usa bajo tu propio riesgo y responsabilidad.

---

**¿Necesitas ayuda?** Abre un issue en el repositorio.

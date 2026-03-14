# MÉTODO FINAL: Generador Automático de Reportes Meta Ads

**Creado:** 2026-03-14 21:32 UTC  
**Status:** PLANTILLA LISTA PARA IMPLEMENTAR  
**Próxima Fase:** Python Script de Automatización (Opción B)

---

## 🎯 OBJETIVO

Crear un **script Python único** que:
1. Reciba `campaign_id` como parámetro
2. Extraiga **TODOS** los datos de Meta API automáticamente
3. Genere `data.json` + `video-analysis.json`
4. Cree `index.html` reporte automático
5. Commit + push a GitHub en 1 comando

**Tiempo de ejecución:** ~2 minutos  
**Tiempo de desarrollo:** ~2-3 horas

---

## 📋 DATOS REQUERIDOS (2 FUENTES)

### 1️⃣ data.json (Histórico Diario)

**Estructura:**
```json
{
  "daily": [
    {
      "date": "2026-03-02",
      "spend": 13.40,
      "impressions": 716,
      "clicks": 8,
      "leads": 1,
      "cpl": 13.40
    },
    // ... más días
  ]
}
```

**Fuente:** Meta API `campaign_id/insights`
```
GET /v18.0/{campaign_id}
fields: insights.date_preset(last_30d).fields(spend,impressions,clicks,actions).time_increment(1)
```

**Extracción:**
- `spend`: campo `spend`
- `impressions`: campo `impressions`
- `clicks`: campo `clicks`
- `leads`: filtrar `actions[]` donde `action_type == "lead"` exactamente
- `cpl`: `spend / leads`

**Validación:**
- 12-30 registros (uno por día)
- SUM(spend) debe coincidir con Meta API total
- SUM(leads) debe coincidir con Meta API total

---

### 2️⃣ video-analysis.json (Por Ad Set)

**Estructura:**
```json
[
  {
    "ad_id": "23849578901",
    "ad_name": "Ad 1 Pablo",
    "adset_id": "120239305936170322",
    "adset_name": "Marketing/España/Open+",
    "spend": 3.15,
    "impressions": 195,
    "clicks": 2,
    "plays": 350,
    "plays_25": 35,
    "plays_50": 25,
    "plays_75": 18,
    "plays_100": 12,
    "leads": 1,
    "cpl": 3.15,
    "cpm": 16.15
  },
  // ... más ad sets
]
```

**Fuente:** Meta API por Ad Set
```
GET /v18.0/{campaign_id}/adsets
fields: id,name,insights.date_preset(last_30d).fields(spend,impressions,clicks,actions,video_play_actions,video_25_percentiles_viewed_actions,video_50_percentiles_viewed_actions,video_75_percentiles_viewed_actions,video_complete_watched_actions)

GET /v18.0/{adset_id}/ads
fields: id,name,insights.date_preset(last_30d).fields(spend,impressions,clicks,actions,video_play_actions,...)
```

**Extracción:**
- `ad_id`: campo `id` del ad
- `ad_name`: campo `name` del ad
- `adset_id`: ID del ad set padre
- `adset_name`: nombre del ad set (ej: "Marketing/España/Open+")
- `spend`: campo `spend`
- `impressions`: campo `impressions`
- `clicks`: campo `clicks`
- `plays`: valor en `video_play_actions[0].value`
- `plays_25`: valor en `video_25_percentiles_viewed_actions[0].value`
- `plays_50`: valor en `video_50_percentiles_viewed_actions[0].value`
- `plays_75`: valor en `video_75_percentiles_viewed_actions[0].value`
- `plays_100`: valor en `video_complete_watched_actions[0].value`
- `leads`: filtrar `actions[]` donde `action_type == "lead"`
- `cpl`: `spend / leads` (o 0 si leads = 0)
- `cpm`: `(spend / impressions) * 1000`

**Validación:**
- SUM(plays) debe ser lógico (>= leads)
- Retención decreciente: plays > plays_25 > plays_50 > plays_75 > plays_100
- CPL realista (no valores extremos)

---

## 🔧 ESTRUCTURA DEL SCRIPT PYTHON

**Nombre archivo:** `generate_dashboard.py`  
**Ubicación:** `/home/ubuntu/.openclaw/workspace/meta-ads-reports/`

```python
#!/usr/bin/env python3

import requests
import json
import sys
import os
from datetime import datetime, timedelta

class MetaDashboardGenerator:
    def __init__(self, campaign_id, campaign_name, token):
        self.campaign_id = campaign_id
        self.campaign_name = campaign_name
        self.token = token
        self.base_url = "https://graph.facebook.com/v18.0"
        
    def get_daily_data(self):
        """Extrae data.json con time_increment(1)"""
        # Consultar Meta API
        # Procesar respuestas
        # Retornar array de {date, spend, impressions, clicks, leads}
        pass
    
    def get_ad_set_data(self):
        """Extrae video-analysis.json por ad set"""
        # Listar ad sets de la campaña
        # Para cada ad set, listar ads
        # Para cada ad, extraer insights + video metrics
        # Retornar array de {ad_id, ad_name, adset_id, adset_name, ...}
        pass
    
    def validate_data(self):
        """Valida consistencia entre data.json y video-analysis.json"""
        # SUM(video-analysis spend) ≈ SUM(data daily spend)
        # SUM(video-analysis leads) == SUM(data daily leads)
        # Retornar True si valida, False si hay discrepancia
        pass
    
    def save_json_files(self, daily_data, ad_set_data):
        """Guarda data.json y video-analysis.json"""
        pass
    
    def generate_html(self):
        """Lee template HTML existente y lo copia"""
        # El HTML es genérico, no requiere cambios
        # Solo asegurarse de que carga los JSON correctos
        pass
    
    def run(self):
        """Pipeline completo"""
        print(f"🚀 Generando dashboard para: {self.campaign_name}")
        
        daily = self.get_daily_data()
        print(f"✅ {len(daily)} días extraídos")
        
        ad_sets = self.get_ad_set_data()
        print(f"✅ {len(ad_sets)} ad sets extraídos")
        
        if self.validate_data():
            print("✅ Validación exitosa")
            self.save_json_files(daily, ad_sets)
            self.generate_html()
            print("✅ Dashboard generado")
        else:
            print("❌ Validación fallida - revisar discrepancias")

# Uso
if __name__ == "__main__":
    campaign_id = sys.argv[1]  # ej: 120239305936170318
    campaign_name = sys.argv[2]  # ej: "Test Manual SEO Local Pablo"
    token = os.getenv("META_TOKEN")
    
    gen = MetaDashboardGenerator(campaign_id, campaign_name, token)
    gen.run()
```

**Ejecución:**
```bash
export META_TOKEN="EAAPi9VdL1IgBQ..."
python3 generate_dashboard.py 120239305936170318 "Test Manual SEO Local Pablo"
```

---

## 🎨 TEMPLATE HTML

**El HTML actual (`index.html`) es 100% genérico y reutilizable.**

No requiere cambios porque:
- Lee datos de `data.json` y `video-analysis.json` vía fetch
- Todos los cálculos son dinámicos (JavaScript)
- No tiene valores hardcodeados
- Responsive auto-detect funciona siempre

**Para nueva campaña:**
- Copiar `index.html` tal cual
- Reemplazar `data.json` con nuevos datos
- Reemplazar `video-analysis.json` con nuevos datos
- Listo

---

## 📝 CHECKLIST VALIDACIÓN (ANTES DE PUBLICAR)

Para cada nuevo reporte:

- [ ] **data.json** tiene 12-30 días
- [ ] **SUM(daily spend)** ≈ **SUM(ad_set spend)** (diferencia < €1)
- [ ] **SUM(daily leads)** == **SUM(ad_set leads)** (exacto)
- [ ] **Retención decreciente:** plays > plays_25 > plays_50 > plays_75 > plays_100
- [ ] **CPL realista:** no valores < €1 o > €100
- [ ] **CPM realista:** entre €3-€20 típicamente
- [ ] **Action_type == "lead" exacto** (no variaciones)
- [ ] **Gráfico CPL diario:** incluye todos los días (con "Sin datos" en días sin conversiones)
- [ ] **KPI arriba:** dinámico desde data.json
- [ ] **Semana 1 vs Semana 2:** comparativa correcta
- [ ] **Cache clear:** Ctrl+F5 en navegador
- [ ] **GitHub Pages:** actualización en 2-3 minutos

---

## 🔄 VERSIONADO Y GIT

**Estructura:**
```
/meta-ads-reports/
├── README.md (instrucciones)
├── METODO-GENERADOR-REPORTES.md (este archivo)
├── generate_dashboard.py (Python script)
├── index.html (template - genérico)
├── data.json (datos diarios)
├── video-analysis.json (datos ad sets)
└── adset-mapping.json (opcional - nombres audiencias)
```

**Git commits:**
```bash
# Después de generar:
git add data.json video-analysis.json
git commit -m "📊 NUEVA CAMPAÑA: [Nombre] - [Período] | €[spend] | [leads] leads | CPL €[cpl]"
git push origin master
```

---

## 🎯 PRÓXIMA CAMPAÑA - PROCESO

1. **Obtener Campaign ID** (de Meta Ads Manager)
2. **Ejecutar script:**
   ```bash
   python3 generate_dashboard.py [campaign_id] "[campaign_name]"
   ```
3. **Validar salida** (checklist arriba)
4. **Git commit + push**
5. **Esperar 2-3 min** (GitHub Pages update)
6. **URL:** https://herramientas-annalit.github.io/meta-ads-reports/[campaign_name]/

---

## 📊 EJEMPLO: Test Manual SEO Local Pablo (ACTUAL)

**Campaign ID:** 120239305936170318  
**Período:** 2-13 Marzo 2026  
**Datos:**
- Spend: €223.70
- Leads: 20
- CPL: €11.18
- Ad Sets: 9 (3 creativos × 3 audiencias)

**Archivos generados:**
- `data.json`: 12 registros diarios
- `video-analysis.json`: 9 registros (ad sets)
- `index.html`: Reporte con 4 tabs

---

## ✅ STATUS ACTUAL

- [x] **Diseño HTML:** 100% completo y testado
- [x] **Data.json:** Estructura validada
- [x] **video-analysis.json:** Estructura validada
- [x] **Cálculos:** Todos dinámicos y correctos
- [x] **Responsive:** Funciona móvil/tablet/desktop
- [ ] **Python script:** PENDIENTE (será Opción B)

---

**Próximo paso:** Crear `generate_dashboard.py` (2-3 horas)  
**Después:** Una campaña + script = Dashboard automático en 2 minutos

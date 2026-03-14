# 📊 PLANTILLA: Reporte Ejecutivo Meta Ads Campaign

## Estructura del Reporte

**Componentes clave:**

1. **TAB 1: General**
   - 4 KPIs principales (Inversión, Leads, CPL, CTR)
   - 4 gráficos de evolución (Acumulado, CPL tendencia, Gasto diario, Leads diarios)
   - Alertas críticas (ej: audience fatigue)
   - 3 recomendaciones inmediatas

2. **TAB 2: Creativos**
   - Tabla agregada (sum de todos los ad sets por creativo)
   - Embudo de conversión (mejor creativo)
   - Curva de retención %
   - 2 gráficos divididos:
     - Efectivos (con leads): Presupuesto vs Leads, color=CPL
     - En test (sin leads): Presupuesto vs CPM

3. **TAB 3: Ad Sets**
   - Tabla desglosada: Audiencia | Creativo | Presupuesto | Plays | Leads | CPL | Retención 25% | CPM | Acción
   - Cada fila = 1 ad set (creativo + audiencia)
   - Acciones color-coded: ✅ Escalar, ⚠️ Monitor, ❌ Pausar, 🟡 Test

4. **TAB 4: Proyecciones**
   - 3 escenarios de escala (actual, recomendado, agresivo)
   - Gráfico: Presupuesto diario → Ingresos/mes (con 3 CPLs)
   - 4 pasos para escalar

## Datos Requeridos

```json
{
  "campaign": {
    "id": "120239305936170318",
    "name": "Test Manual SEO Local Pablo",
    "status": "ACTIVE",
    "start_date": "2026-03-02",
    "end_date": "2026-03-14"
  },
  "daily_data": "data.json",
  "creative_data": "video-analysis.json",
  "adset_mapping": "adset-mapping.json"
}
```

### data.json (Diario)
```json
{
  "daily": [
    {"date": "2026-03-02", "spend": 13.4, "impressions": 716, "clicks": 7, "leads": 1, "cpl": 13.4},
    ...
  ]
}
```

### video-analysis.json (Por Ad Set)
```json
[
  {
    "ad_id": "120239309083090318",
    "ad_name": "Ad 2 Pablo",
    "spend": 133.25,
    "impressions": 16851,
    "plays": 11562,
    "plays_25": 1079,
    "plays_50": 469,
    "plays_75": 264,
    "plays_100": 117,
    "leads": 13,
    "cpl": 10.25,
    "cpm": 7.91,
    "retention_25": 9.33
  },
  ...
]
```

### adset-mapping.json (Nombres de Audiencias)
```json
{
  "120239309083090318": "Audiencia H - Premium (CPM optimizado)",
  "120239308508030318": "Audiencia A - Negocios (CPM bajo)",
  ...
}
```

## Cálculos Clave

| Métrica | Fórmula |
|---------|---------|
| CPL | spend / leads |
| CPM | (spend / impressions) × 1000 |
| CTR | (clicks / impressions) × 100 |
| Hook (0-3s) | retention_25 × 1.2 |
| Lead Rate % | (leads / plays) × 100 |
| ROI (asumido) | (leads × $50/lead) / spend |

## Cómo Generarlo

### Opción 1: Automática (Python)
```bash
python3 meta_ads_reporter.py \
  --campaign-id 120239305936170318 \
  --output meta-ads-reports/
```

### Opción 2: Manual
1. Exportar datos de Meta API
2. Generar `data.json` (histórico diario)
3. Generar `video-analysis.json` (métricas ad set)
4. Crear `adset-mapping.json` (nombres audiencias)
5. Abrir `index.html` en navegador

## Uso para Comparativas

Para comparar 2+ campañas:
1. Generar reporte individual de cada campaña
2. Guardar en carpetas separadas:
   - `/meta-ads-reports/campaign-1/`
   - `/meta-ads-reports/campaign-2/`
3. Crear página de **comparación transversal**:
   - CPL promedio por campaña
   - ROI proyectado
   - Creativos ganadores (top 3)
   - Audiencias más efectivas
   - Recomendaciones cruzadas

## Template HTML

El archivo `index.html` es totalmente reutilizable.
Solo necesita actualizar:
- `data.json`
- `video-analysis.json`
- `adset-mapping.json`

El JS se auto-adapta y carga los nuevos datos.

---

**Estado:** ✅ Plantilla v1 — Lista para escalado de reportes
**Último actualizado:** 2026-03-14 14:48 UTC

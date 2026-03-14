# 🤖 AGENTE GENERADOR DE REPORTES META ADS

**Plantilla Maestra para Generar Reportes Automáticos de Campañas Meta Ads**

---

## 📋 FLUJO COMPLETO (No Olvidar)

### **PASO 1: ENTRADA**
```
Usuario dice: "Haz reporte de [Nombre Campaña]"
```

**Extraer del usuario:**
- ✅ Nombre campaña (o ID)
- ✅ Período (últimos 7 días, 30 días, custom)
- ✅ Divisa (EUR, USD, etc.)

### **PASO 2: VALIDACIÓN EN META**
```bash
1. Extraer Campaign ID desde Meta API
2. Verificar que campaña EXISTE y está ACTIVE
3. Listar TODOS los ad sets (conjuntos) activos
4. Por cada ad set: listar TODOS los ads (anuncios)
5. Validar estructura: Campaña → Ad Sets → Ads (mínimo 1)
```

**Comando Python:**
```python
# Extrae estructura completa sin asumir nada
GET /campaign_id/adsets
GET /adset_id/ads
GET /ad_id/insights (últimos 30 días)
```

### **PASO 3: EXTRACCIÓN DE DATOS**

**Datos requeridos por ANUNCIO:**
```json
{
  "ad_id": "XXXX",
  "adset_id": "XXXX", 
  "adset_name": "Nombre exacto desde Meta",
  "ad_name": "Nombre exacto desde Meta",
  "status": "ACTIVE|PAUSED",
  
  "spend": float (€),
  "impressions": int,
  "clicks": int,
  "video_play": int,
  "video_p25_watched": int,
  "video_p50_watched": int,
  "video_p75_watched": int,
  "video_p100_watched": int,
  "leads": int,
  
  "cpm": float (€ per 1000 impressions),
  "cpl": float (€ per lead),
  "ctr": float (%)
}
```

**Datos requeridos por AD SET (targeting):**
```json
{
  "adset_id": "XXXX",
  "adset_name": "Nombre",
  "edad_min": int,
  "edad_max": int,
  "sexo": "Todos|Hombre|Mujer",
  "ubicacion": "País/Región",
  "intereses": ["array", "de", "intereses"]
}
```

**Datos diarios (histórico):**
```json
{
  "date": "YYYY-MM-DD",
  "spend": float,
  "leads": int,
  "impressions": int,
  "clicks": int,
  "cpl": float
}
```

### **PASO 4: VALIDACIÓN DE DATOS**

**Verificar:**
```
✅ Sum of daily.spend = campaign.spend (tolerancia ±1%)
✅ Sum of ads.leads = campaign.leads (exacto)
✅ Sum of ads.impressions = campaign.impressions (exacto)
✅ No NaN, no NULL, no valores negativos
✅ CPL = spend / leads (recalcular si falta)
✅ CPM = (spend / impressions) * 1000
✅ CPC = spend / clicks
✅ CTR = (clicks / impressions) * 100
```

**Si falla:** PARAR y alertar al usuario

### **PASO 5: GENERACIÓN DE ARCHIVOS**

**Crear 4 archivos JSON:**

1. **`data.json`** (histórico diario)
   - Periodo: 2-14 Marzo, 1-30 Marzo, etc.
   - Campos: date, spend, impressions, clicks, leads, cpl
   - 13-30 registros (1 por día)

2. **`video-analysis.json`** (por anuncio)
   - 1 registro por anuncio (todos)
   - Incluye: adset_id, adset_name, age, targeting, retention %

3. **`adset-mapping.json`** (targeting metadata)
   - Key: adset_id
   - Value: {name, edad_min, edad_max, sexo, ubicacion, intereses}

4. **`index.html`** (dashboard)
   - Generado desde template
   - 4 pestañas: General | Creativos | Ad Sets | Proyecciones

### **PASO 6: CÁLCULOS & MÉTRICAS**

**KPI GLOBALES:**
```
Total Spend: €X.XX
Total Leads: N
Avg CPL: €X.XX
Avg CTR: X.XX%
Avg CPM: €X.XX
```

**SEMANAL:**
```
Semana 1 (2-8): €X | N leads | CPL €X | CPM €X
Semana 2 (9-14): €X | N leads | CPL €X | CPM €X
Comparativa: ±X% spend | ±X% leads | ±X% CPL
Fatiga: 🟢 NORMAL | 🟡 ALTA | 🔴 CRÍTICA
```

**POR CREATIVO (agregado de todos ad sets):**
```
Creativo X:
  - Total spend: €X
  - Total leads: N
  - CPL: €X
  - Status: ✅ GANADOR | ⚠️ EN TEST | ❌ PAUSA
```

**POR AD SET (público/targeting):**
```
Small Business:
  - Ad 1: X plays, N leads, CPL €X, Hook X%
  - Ad 2: X plays, N leads, CPL €X, Hook X%
  - Ad 3: X plays, N leads, CPL €X, Hook X%
```

### **PASO 7: GENERACIÓN HTML**

**4 TABS (pestañas):**

**TAB 1: GENERAL**
- 4 KPI cards: Spend, Leads, CPL, CTR
- Gráfico 1: Evolución acumulada (dual Y-axis: € + leads)
- Gráfico 2: CPL diario (tendencia)
- Gráfico 3: Gasto diario (barras)
- Tarjeta Semanal: Sem 2 grande, Sem 1 pequeño debajo
- Acciones recomendadas (3 tarjetas)

**TAB 2: CREATIVOS**
- Tabla agregada (sum de todos ad sets por creativo)
  Columnas: Creativo | Plays | Presupuesto | Hook % | 25-100% | Leads | CPL | Acción
- Gráfico: Embudo de conversión (7 pasos)
- 2 tablas separadas:
  - Creativos con leads (efectivos)
  - Creativos sin leads (en test)

**TAB 3: AD SETS (Audiencias)**
- Tabla completa (1 fila = 1 anuncio)
  Columnas: Audiencia | Edad | Sexo | Ubicación | Intereses | Creativo | Plays | Presupuesto | Hook% | 25-100% | Leads | CPL | CPM | Acción
- Color-coded: Hook % verde/naranja/rojo
- Acciones: ✅ Escalar | ⚠️ Monitor | ❌ Pausar | 🟡 Test

**TAB 4: PROYECCIONES**
- 3 escenarios (Actual, Recomendado, Agresivo)
- Gráfico: Presupuesto diario → Ingresos mensuales
- Múltiples CPLs: €9, €11.59, €15
- 4 pasos para escalar

### **PASO 8: VALIDACIÓN FINAL**

```
✅ Dashboard genera sin errores
✅ Todos los gráficos muestran datos correctos
✅ Colores se aplican correctamente
✅ Tabla de audiencias tiene 9 anuncios (o N correctos)
✅ Sumas match con Meta API totales
✅ URLs de GitHub Pages funcional
```

### **PASO 9: COMMIT & PUSH**

```bash
git add -A
git commit -m "📊 Reporte [Campaña] - [Fecha]

✅ Datos validados:
- Spend: €X
- Leads: N
- Período: 2-14 Marzo
- Ad Sets: 3
- Anuncios: 9

📝 Próximas partes: ..."

git push origin master
```

### **PASO 10: NOTIFICACIÓN AL USUARIO**

```
✅ Dashboard generado: https://github.com/.../meta-ads-reports
📊 Datos validados: €231.84 | 20 leads | 9 anuncios
📅 Período: 2-14 Marzo 2026
🎯 Próximos pasos: [listar]
```

---

## 🛠️ HERRAMIENTAS REQUERIDAS

**Meta API:**
- Campaign ID (input usuario)
- Access Token (guardado seguro)
- Campos: insights, adsets, ads, targeting, actions

**Python Script:**
```python
generate_report.py

Argumentos:
  --campaign-name "Nombre Campaña"
  --campaign-id "XXXXX" (alternativo)
  --period "last_30d" | "last_7d" | "2026-03-02:2026-03-14"
  --currency "EUR" | "USD"
  --output "./reports/"
```

**Archivos base:**
- `PLANTILLA-REPORTE.md` (referencia)
- `index.html` (template)
- `data.json` (histórico)
- `video-analysis.json` (anuncios)
- `adset-mapping.json` (targeting)

---

## 📝 CHECKLIST POR REPORTE

- [ ] Usuario proporciona nombre campaña
- [ ] Extraigo Campaign ID desde Meta
- [ ] Listo ad sets (conjuntos) activos
- [ ] Listo ads (anuncios) por ad set
- [ ] Extraigo insights + targeting (Meta API)
- [ ] Calculo CPL, CPM, CTR, Hook %, retención
- [ ] Valido: sumas match, sin duplicados, sin NaN
- [ ] Genero 4 archivos JSON
- [ ] Genero HTML con 4 tabs
- [ ] Verifico: gráficos, colores, tablas
- [ ] Git: commit + push
- [ ] Notificación usuario con link + datos

---

## 🚀 PRÓXIMO REPORTE

Cuando usuario pida reporte de otra campaña:

1. Repetir PASOS 1-10
2. Cambiar solo: campaign_name, period
3. Validación automática (PASOS 2-4)
4. NO olvidar: edad, sexo, ubicación, intereses en ad sets
5. NO olvidar: 9 anuncios (3 creativos × 3 públicos) si aplica

---

**Última actualización**: 2026-03-14 16:55 UTC
**Agente**: Generador de Reportes Meta Ads
**Status**: ✅ PLANTILLA LISTA

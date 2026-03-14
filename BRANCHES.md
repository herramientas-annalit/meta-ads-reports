# Estructura de Ramas - Meta Ads Dashboard

## 🌳 Ramas Principales

### `master` (PRODUCCIÓN)
- ✅ **ESTABLE** - Lo que está en vivo en GitHub Pages
- Solo cambios que funcionan 100%
- Dashboard live: https://herramientas-annalit.github.io/meta-ads-reports/

### `develop` (TESTING)
- 🟡 **En prueba** - Próxima versión a lanzar
- Aquí probar cambios grandes antes de merge a master
- Un paso antes de producción

### `feature/comparativa-creativos` (DESARROLLO)
- 🔵 **En desarrollo** - Nuevas características
- Donde trabajamos en features nuevas
- Cuando esté lista → PR a develop

### `bugfix/responsive-mobile` (ARREGLOS)
- 🟠 **En arreglo** - Fixes y patches
- Bugs encontrados
- Cuando esté listo → PR a develop

---

## 📋 WORKFLOW (Cómo trabajar)

### Paso 1: Crear rama para nuevo feature
```bash
git checkout -b feature/nombre-feature
```

### Paso 2: Trabajar y hacer commits
```bash
# Cambios
git add .
git commit -m "Descripción del cambio"
git push origin feature/nombre-feature
```

### Paso 3: Crear Pull Request en GitHub
- GitHub te mostrará: "Create a Pull Request"
- Elige: `feature/nombre-feature` → `develop`
- Describe qué hiciste
- Espera a revisión

### Paso 4: Si funciona
- Merge a `develop`
- Probar en develop (testing)
- Si todo ok → PR `develop` → `master`
- Live en producción ✅

### Paso 5: Si tiene bugs
- Documentar en `.CHANGELOG.md`
- Crear `bugfix/nombre-issue`
- Arreglar → PR a develop
- Reintentarlo

---

## 👀 Cómo VER en GitHub

### Dashboard de ramas:
1. Va a: https://github.com/herramientas-annalit/meta-ads-reports
2. Click en "1 Branch"
3. Ves todas las ramas

### Ver Pull Requests:
1. Click en "Pull Requests"
2. Ve todas las PRs abiertas
3. Reviews pendientes

### Ver commits por rama:
1. Click en dropdown "master"
2. Selecciona otra rama
3. Ve commits de esa rama

---

## 🎯 ESTADO ACTUAL

| Rama | Estado | Commits | Uso |
|------|--------|---------|-----|
| `master` | ✅ STABLE | 43 | Producción live |
| `develop` | 🟡 TESTING | 43 | Siguiente release |
| `feature/comparativa-creativos` | 🔵 TODO | 0 | Trabajar aquí |
| `bugfix/responsive-mobile` | 🟠 TODO | 0 | Arreglos aquí |

---

## 📚 Referencia Rápida

**Ve a master (seguro):**
```bash
git checkout master
```

**Ve a develop (pruebas):**
```bash
git checkout develop
```

**Crea rama para feature:**
```bash
git checkout -b feature/mi-feature
```

**Push cambios:**
```bash
git push origin feature/mi-feature
```

**Ve cambios en GitHub:**
- Abre: https://github.com/herramientas-annalit/meta-ads-reports/branches

---

## ✨ Ventajas

✅ **master** limpio = producción estable
✅ **develop** = testing seguro  
✅ **feature/** = nuevas cosas sin riesgo
✅ **bugfix/** = arreglos organizados
✅ **Pull Requests** = control y documentación
✅ **Historio** = NUNCA pierdes cambios

---

**Última actualización:** 2026-03-14 19:23 UTC

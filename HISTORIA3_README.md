# 🎯 Historia 3: Reporte Ejecutivo de Alertas (Marketing)

## ¿Cómo Funciona?

Historia 3 se activa cuando:
1. ✅ Subes 2 archivos CSV de **marketing**
2. ✅ Escribes algo en el chat
3. ✅ Aprietas el botón **"🚨 Analizar"** en la sección **"💡 ESTRATEGIA"**

## 📁 Archivos de Demo

Para probar, usa estos archivos CSV:
- `demo_marketing_servicios.csv` - Datos de servicios (tarifa, horas, costo/hora)
- `demo_marketing_ventas.csv` - Datos de ventas por servicio

## 🚀 Pasos para Ejecutar

### 1. Abre Streamlit
```bash
cd frontend
streamlit run streamlit_final.py
```

### 2. En la Interfaz
- **Sección izquierda (💬 Chat):**
  - Haz clic en "**➕ Subir CSV**"
  - Selecciona ambos archivos de demostración
  - Escribe cualquier cosa en el chat (ej: "Analizar")
  - ¡Verás el reporte ejecutivo!

- **Sección derecha (🎯 Análisis):**
  - Ve a la sección **"💡 ESTRATEGIA"**
  - Haz clic en **"🚨 Analizar"**
  - ¡Verás Historia 3 con alertas de marketing!

## 📊 Qué Verás en Historia 3

### Contadores KPI
```
🔴 Negativos: 2       (servicios con margen negativo)
🟡 Críticos: 3        (servicios con margen crítico)
🟠 Desactualizados: 1 (servicios con precio desactualizado)
⏱ Alto esfuerzo: 2    (servicios con alto esfuerzo/bajo retorno)
```

### Alertas Detectadas
- **🔴 Alerta 1 — MARGEN NEGATIVO (ALTA)**
  - Servicio: Gestión de redes premium (S11)
  - Tarifa $22.500 vs costo $26.800 → pérdida $4.300/mes
  - Acciones: Ajustar tarifa, reducir alcance, automatizar

- **🟡 Alerta 2 — ALTO ESFUERZO / BAJO RETORNO (MEDIA)**
  - Servicio: Campaña Ads + optimización (S05)
  - 18 horas/mes con margen 8% (objetivo 15%)
  - Acciones: Paquetizar, subir tarifa, estandarizar

- **🟠 Alerta 3 — PRECIO_DESACTUALIZADO (MEDIA)**
  - Servicio: Diseño + contenido mensual (S03)
  - Costo/hora +12% pero tarifa sin cambios
  - Acciones: Ajustar tarifa, aplicar cláusula trimestral

### Filtros Disponibles
- Filtra por **Tipo**: MARGEN_NEGATIVO, MARGEN_CRITICO, ALTO_ESFUERZO_BAJO_RETORNO, PRECIO_DESACTUALIZADO
- Filtra por **Severidad**: ALTA, MEDIA

## 💡 Ejemplo de Uso Real (Agencia Digital)

1. **Dueña sube CSVs de servicios** (spreadsheet de tarifas vs horas)
2. **Escribe en el chat** "¿Cuál es mi problema de márgenes?"
3. **Ve Historia 3** con las 3 alertas de marketing
4. **Filtra por ALTA prioridad**
5. **Lee la alerta #1** → "Gestión de redes me está quemando"
6. **Ve la acción sugerida** → "Aumentar tarifa a $30k"
7. **Estima el impacto** → "+$3.7k mensuales de más margen"

## 🎨 Visualización

Las alertas se muestran como **tarjetas de colores**:
- 🔴 **Rojo** = ALTA prioridad (acción inmediata)
- 🟡 **Amarillo** = MEDIA prioridad (revisar pronto)
- 🟠 **Naranja** = Precio desactualizado

Cada tarjeta muestra:
- Nombre del servicio
- Explicación clara del problema
- Evidencia numérica ($, %)
- Acciones sugeridas (bullets)

## 🔧 Detalles Técnicos

### Datos Simulados (en `streamlit_final.py`)
Historia 3 está bajo la clave `"marketing"` en el diccionario `SIM_REPORTS`
- 8 servicios analizados
- 2 con margen negativo
- 3 con margen crítico
- 2 con alto esfuerzo
- 1 con precio desactualizado

### Detección Automática
Si subes archivos con palabras clave como:
- "marketing"
- "agencia"
- "marketing_"

Streamlit detectará automáticamente que es data de marketing y mostrará los datos de Historia 3.

## ❓ FAQ

**P: ¿Qué pasa si subo solo 1 archivo?**  
R: Streamlit te pedirá ambos archivos (como dice el chat).

**P: ¿Qué pasa si subo archivos de panadería?**  
R: Verás Historia 1 y 2 (panadería), no Historia 3 (marketing).

**P: ¿Puedo cambiar los datos?**  
R: Sí, edita el diccionario `SIM_REPORTS["marketing"]` en `streamlit_final.py`.

**P: ¿Cómo agrego más alertas?**  
R: Agrega items al array `"alerts"` de la sección marketing en `SIM_REPORTS`.

---

¡Ahora tienes Historia 3 lista para demostrar! 🚀

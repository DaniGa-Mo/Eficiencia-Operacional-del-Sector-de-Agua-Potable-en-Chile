# 💧 Eficiencia Operacional del Sector de Agua Potable en Chile
### Análisis 2015–2022 | Estructura de Informes SISS

> **Proyecto Integrador — Diplomado Python para la Toma Estratégica de Decisiones Organizacionales**
> Universidad Andrés Bello (UNAB) · Abril 2026

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.2.3-150458?logo=pandas)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-6.0.1-3F4F75?logo=plotly)](https://plotly.com/)
[![NumPy](https://img.shields.io/badge/NumPy-1.26.4-013243?logo=numpy)](https://numpy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Tabla de Contenidos

- [Descripción del Proyecto](#-descripción-del-proyecto)
- [Contexto y Motivación](#-contexto-y-motivación)
- [Hipótesis Central](#-hipótesis-central)
- [Objetivos](#-objetivos)
- [Estructura del Repositorio](#-estructura-del-repositorio)
- [Fuentes de Datos](#-fuentes-de-datos)
- [Pipeline ETL](#-pipeline-etl)
- [Análisis y Visualizaciones](#-análisis-y-visualizaciones)
- [Dashboard Ejecutivo](#-dashboard-ejecutivo)
- [Principales Hallazgos](#-principales-hallazgos)
- [Propuestas de Acción](#-propuestas-de-acción)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Cómo Ejecutar el Proyecto](#-cómo-ejecutar-el-proyecto)
- [Autor](#-autor)

---

## 🔍 Descripción del Proyecto

Este proyecto analiza la **eficiencia operacional de 8 empresas sanitarias concesionarias de agua potable en Chile** durante el periodo 2015–2022, utilizando como referencia la estructura de indicadores publicados por la **Superintendencia de Servicios Sanitarios (SISS)**.

El análisis se construye sobre un **dataset sintético con parámetros calibrados a partir de informes públicos reales**, garantizando reproducibilidad académica y validez analítica. Se desarrolla un pipeline ETL completo, análisis exploratorio, 7 preguntas estratégicas respondidas con visualizaciones interactivas y un dashboard ejecutivo de KPIs.

---

## 🌊 Contexto y Motivación

Chile tiene una de las coberturas de agua potable más altas de América Latina (**>99%**), pero el sector enfrenta desafíos estructurales urgentes:

| Desafío | Descripción |
|--------|------------|
| 💸 **Agua No Facturada (ANF)** | Las pérdidas en red oscilan entre el 18% y el 40% según empresa. Cada punto porcentual equivale a millones de m³ no recuperados |
| 📊 **Disparidad entre empresas** | La eficiencia varía considerablemente entre sanitarias, generando brechas de calidad de servicio entre regiones |
| 🌡️ **Crisis hídrica** | El cambio climático agudiza la escasez, haciendo urgente la optimización de recursos |
| 💼 **Presión inversora** | Accionistas y regulador exigen evidencia de que la inversión en infraestructura se traduce en mejoras medibles |

> ⚠️ El ANF promedio sectorial (~28%) implica que **casi 1 de cada 3 m³ producidos no llega al cliente**, con impacto directo en ingresos, sostenibilidad hídrica y huella ambiental.

---

## 💡 Hipótesis Central

> *"Las diferencias en la tasa de Agua No Facturada (ANF) entre las empresas sanitarias chilenas responden a factores estructurales como la antigüedad de la red, el tipo de fuente hídrica y el nivel de inversión por cliente. Un mayor gasto en infraestructura debería correlacionarse con menores pérdidas y mejor calidad de servicio."*

---

## 🎯 Objetivos

### Objetivo General
Analizar la evolución de la eficiencia operacional en la producción y distribución de agua potable en Chile entre 2015 y 2022, identificando los factores que explican las brechas entre empresas sanitarias y proponiendo acciones estratégicas basadas en datos.

### Objetivos Específicos

1. 🔧 Construir un **pipeline ETL completo** sobre datos del sector sanitario chileno
2. 📈 Explorar estadísticamente los indicadores operacionales: ANF, calidad, cobertura y continuidad
3. 📊 Responder **7 preguntas analíticas estratégicas** mediante visualizaciones con Plotly
4. 🖥️ Desarrollar un **dashboard ejecutivo consolidado** con KPIs del sector
5. 🚀 Proponer acciones concretas para reducir el ANF y mejorar la eficiencia operacional

---

## 📁 Estructura del Repositorio

```
📦 eficiencia-agua-potable-chile/
├── 📓 20260420_DanielGallardo.ipynb   # Notebook principal con todo el análisis
├── 📄 20260420_DanielGallardo.pdf     # Informe final del proyecto
├── 📊 dataset_agua_potable_chile.csv  # Dataset generado (64 registros x 16 variables)
├── 📋 README.md                       # Este archivo
└── 📁 assets/                         # Imágenes y capturas del dashboard
    └── dashboard_preview.png
```

---

## 📂 Fuentes de Datos

El proyecto utiliza un **dataset sintético con estructura real** calibrado a partir de fuentes oficiales:

| Fuente | Tipo | Uso |
|--------|------|-----|
| 📰 **Informes de Gestión SISS 2015–2022** | Primaria (base) | Parámetros reales: ANF base, clientes, regiones, fuentes hídricas |
| 🐍 **Dataset sintético generado en Python** | Primaria (sintética) | Datos longitudinales 2015–2022 de 8 empresas y 14 variables |
| 🗂️ **BCN / SIIT** | Secundaria (referencia) | Validación de magnitudes de clientes y cobertura por región |
| ⚖️ **NCh409 — Norma de calidad del agua** | Regulatoria | Umbral mínimo de muestras conformes (97%) |
| 🌐 **Banco Mundial — WSS Chile** | Secundaria (contexto) | Benchmarks internacionales de ANF |

### 🏢 Empresas Analizadas

| Empresa | Región |
|---------|--------|
| 🏙️ Aguas Andinas | Metropolitana |
| 🌊 ESVAL | Valparaíso |
| 🌿 ESSBIO | Biobío |
| 🏔️ Aguas del Valle | Coquimbo |
| 🌾 Aguas Nuevo Sur | Maule |
| 🌲 Aguas Araucanía | Araucanía |
| 🌧️ ESSAL | Los Lagos |
| ☀️ Aguas Antofagasta | Antofagasta |

### 📐 Variables del Dataset

| Variable | Tipo | Descripción | Rango |
|----------|------|-------------|-------|
| `ano` | Num. discreta | Año del registro | 2015–2022 |
| `empresa` | Categórica | Empresa sanitaria concesionaria | 8 valores |
| `clientes_ap` | Num. entera | Clientes de agua potable | 95K – 2.1M |
| `produccion_mm3` | Num. continua | Producción total (millones m³) | 11 – 280 Mm³ |
| `anf_pct` | Num. continua | Agua No Facturada (%) | 15 – 45% |
| `cobertura_pct` | Num. continua | Cobertura AP (%) | 99.2 – 99.95% |
| `calidad_pct` | Num. continua | Muestras conformes NCh409 (%) | 97.5 – 99.8% |
| `inversion_mmclp` | Num. continua | Inversión (MM$ CLP) | Variable |
| `continuidad_horas` | Num. continua | Horas anuales de corte | 0.5 – 6.0 h |
| `fuente_agua` | Categórica | Tipo de fuente hídrica | Superficial / Subterránea / Mixta / Desalación |
| `inversion_por_cliente` *(KPI)* | Num. entera | Inversión per cápita (CLP/cliente) | 18K – 35K CLP |
| `perdidas_mm3` *(KPI)* | Num. continua | Pérdidas absolutas (Mm³) | producción − facturación |
| `eficiencia_pct` *(KPI)* | Num. continua | % agua efectivamente facturada | 100 − ANF |
| `indice_servicio` *(KPI)* | Num. continua | Índice compuesto de calidad | Fórmula ponderada |

---

## ⚙️ Pipeline ETL

El pipeline se divide en tres etapas:

### 1️⃣ Extracción — Generación del Dataset
- Dataset generado programáticamente con `np.random.seed(42)` para **reproducibilidad total**
- Cada empresa tiene parámetros ANF base distintos, con reducción de **0.4 p.p./año** + ruido gaussiano (σ=1.2)
- Resultado: **64 registros × 12 variables** base

### 2️⃣ Limpieza — Validación de Calidad

| Verificación | Resultado |
|-------------|-----------|
| ✅ Valores nulos | Ninguno — APROBADO |
| ✅ Duplicados (año + empresa) | 0 — APROBADO |
| ✅ ANF en [10, 50] | APROBADO |
| ✅ Cobertura en [95, 100] | APROBADO |
| ✅ Calidad en [90, 100] | APROBADO |
| ✅ Producción > 0 | APROBADO |
| ✅ Facturación < Producción | APROBADO |

### 3️⃣ Transformación — KPIs Derivados

```python
# KPIs derivados en la etapa de transformación
df['inversion_por_cliente'] = (df['inversion_mmclp'] * 1e6) / df['clientes_ap']
df['perdidas_mm3']          = df['produccion_mm3'] - df['facturacion_mm3']
df['eficiencia_pct']        = 100 - df['anf_pct']
df['indice_servicio']       = (df['cobertura_pct'] * 0.30 +
                                df['calidad_pct']   * 0.40 +
                               (100 - df['continuidad_horas'] * 5) * 0.30)
```

Dataset final: **64 filas × 16 columnas** exportado como `dataset_agua_potable_chile.csv`

---

## 📊 Análisis y Visualizaciones

Se responden **7 preguntas estratégicas** mediante visualizaciones interactivas con Plotly:

| # | Pregunta Estratégica | Visualización |
|---|---------------------|---------------|
| **P1** | ¿Cómo evolucionó la producción de agua potable por empresa entre 2015 y 2022? | Serie temporal |
| **P2** | ¿Qué empresa pierde más agua antes de llegar al cliente (ANF)? | Barras horizontales |
| **P3** | ¿Existe una tendencia de mejora sostenida en el ANF a lo largo del tiempo? | Heatmap empresa × año |
| **P4** | ¿La inversión por cliente se asocia con una menor tasa de pérdidas? | Dispersión multivariada |
| **P5** | ¿Las empresas cumplen los estándares de calidad del agua NCh409? | Serie temporal de calidad |
| **P6** | ¿Cuál es la brecha entre el agua producida y la efectivamente facturada? | Barras apiladas |
| **P7** | ¿Qué empresa ofrece la mayor continuidad de servicio al cliente? | Barras de cortes |

### 📌 Hallazgos Clave por Pregunta

**P2 — Ranking ANF promedio 2015–2022:**

```
🥇 Aguas Antofagasta  18.9%  ✅ Bajo meta sectorial (20%)
   Aguas Andinas       20.5%  ✅ Cerca de meta sectorial
   ESSBIO              27.0%  🟡 Bajo umbral crítico (30%)
   ESVAL               28.4%  🟡 Bajo umbral crítico (30%)
   Aguas Araucanía     32.8%  🔴 SOBRE umbral crítico
   Aguas del Valle     34.2%  🔴 SOBRE umbral crítico
   ESSAL               35.3%  🔴 SOBRE umbral crítico
🔴 Aguas Nuevo Sur     36.9%  🔴 SOBRE umbral crítico
```

> Brecha entre la mejor y la peor empresa: **~18 puntos porcentuales**

**P6 — Pérdidas acumuladas 2015–2022: 849.7 Mm³** de agua tratada no recuperada.

---

## 🖥️ Dashboard Ejecutivo

Panel de KPIs consolidados al cierre 2022:

| KPI | Valor | Estado |
|-----|-------|--------|
| 👥 Clientes totales | 3,867,806 | — |
| 🏭 Producción total | 472.1 Mm³ | — |
| 💧 ANF promedio sector | **27.8%** | 🔴 Sobre objetivo (20%) |
| 🌐 Cobertura AP | 99.58% | ✅ Excelente |
| 🧪 Calidad NCh409 | 98.50% | ✅ Dentro del rango regulatorio |
| 💰 Inversión promedio/cliente | $25,521 CLP | — |
| ⏱️ Horas de corte/año | 2.8 h | 🟡 Sobre meta de 2h |
| 💸 Pérdidas totales 2022 | 107.9 Mm³ | 🔴 Agua tratada no recuperada |
| 🏆 Empresa más eficiente | **Aguas Antofagasta** | ANF ~16.3% |
| ⚠️ Mayor criticidad ANF | **Aguas Nuevo Sur** | ANF ~36.4% |

---

## 🔑 Principales Hallazgos

1. **💧 El ANF es el indicador crítico del sector:** El promedio sectorial oscila entre 25–30%, muy por encima del estándar internacional del 15–20%. Aproximadamente 1 de cada 3 m³ producidos se pierde antes de llegar al cliente.

2. **📉 Existe una brecha estructural entre empresas:** La diferencia entre la más eficiente (Aguas Antofagasta, ~18.9%) y la menos eficiente (Aguas Nuevo Sur, ~36.9%) supera los **18 puntos porcentuales**. Esta brecha responde a factores como antigüedad de la red, tipo de fuente hídrica y entorno regulatorio.

3. **💼 La inversión importa, pero no es suficiente sola:** La correlación negativa entre inversión por cliente y ANF es real pero moderada (**r = −0.135**). La calidad y el foco de la inversión es determinante, no solo su volumen.

4. **✅ Calidad del agua: fortaleza del sector:** Todas las empresas cumplen y superan el mínimo regulatorio del 97% de muestras conformes NCh409. Esto es un activo estratégico frente a la opinión pública y los reguladores.

5. **⏳ La tendencia de mejora es insuficiente:** Con una reducción de ~0.4 p.p./año, tomaría **más de una década** alcanzar la meta del 20% para las empresas más rezagadas. Se requieren intervenciones estructurales aceleradas.

---

## 🚀 Propuestas de Acción

### Para las Empresas Sanitarias

| Acción | Descripción | Impacto Esperado |
|--------|-------------|-----------------|
| 🔧 **Programa ANF focalizado** | Detección activa de fugas con correladores acústicos. Priorizar empresas con ANF > 30% | −3 a −5 p.p. ANF en 2 años |
| 📡 **Sensores SCADA/IoT** | Instalar sensores de presión y caudal para detección temprana de fugas y roturas | −30–40% en horas de corte |
| 📊 **Benchmarking interempresas** | Transferencia de mejores prácticas desde Aguas Andinas y Aguas Antofagasta | Brecha ANF < 10 p.p. en 3 años |

### Para el Regulador (SISS)

| Acción | Descripción |
|--------|-------------|
| ⚖️ **Meta regulatoria diferenciada** | ANF > 30%: reducir 2 p.p./año · ANF 20–30%: reducir 1 p.p./año |
| 📢 **Dashboard open-data** | Publicar KPIs anuales del sector en plataforma interactiva (Plotly/Dash) |

### Para la Alta Dirección e Inversionistas

- 💰 **Scoring CAPEX por impacto ANF:** Priorizar proyectos de renovación de redes y medición sobre expansión de capacidad productiva.

### 🗓️ Hoja de Ruta Integrada

| Acción | Responsable | Plazo | KPI de Éxito |
|--------|-------------|-------|-------------|
| Programa ANF focalizado | Empresas ANF > 30% | 6–24 meses | ANF < 28% en 2 años |
| Sensores SCADA/IoT | Emp. con > 4h cortes | 12–36 meses | Cortes < 2h/año |
| Benchmarking interempresas | Grupo sanitario | Permanente | Brecha ANF < 10 p.p. |
| Meta regulatoria gradual | SISS | Inmediato | Todos bajo 30% en 5 años |
| Dashboard open-data SISS | SISS + empresas | 6–12 meses | Publicación anual vigente |
| Scoring CAPEX por ANF | Alta dirección | 3–6 meses | Modelo en producción |

---

## 🛠️ Tecnologías Utilizadas

```python
pandas==2.2.3      # Manipulación y análisis de datos
numpy==1.26.4      # Generación de datos sintéticos y cálculos numéricos
plotly==6.0.1      # Visualizaciones interactivas y dashboard
```

---

## ▶️ Cómo Ejecutar el Proyecto

### Prerrequisitos

```bash
Python >= 3.9
pip install pandas numpy plotly
```

### Ejecución

1. **Clona el repositorio:**
```bash
git clone https://github.com/tu-usuario/eficiencia-agua-potable-chile.git
cd eficiencia-agua-potable-chile
```

2. **Instala las dependencias:**
```bash
pip install -r requirements.txt
```

3. **Abre el notebook:**
```bash
jupyter notebook 20260420_DanielGallardo.ipynb
```

4. **Ejecuta todas las celdas** con `Kernel → Restart & Run All`

> 💡 El dataset se genera automáticamente con `np.random.seed(42)`. No se requiere ningún archivo externo para reproducir el análisis completo.

---

## 📚 Referencias

1. Superintendencia de Servicios Sanitarios (SISS). *Informe de Gestión del Sector Sanitario 2015–2022*. Santiago, Chile.
2. Biblioteca del Congreso Nacional (BCN) / SIIT. *Estadísticas regionales de cobertura sanitaria*.
3. Instituto Nacional de Normalización (INN). *Norma Chilena NCh409 — Agua potable. Parte 1: Requisitos*.
4. Banco Mundial. *Water Supply and Sanitation in Chile — Performance and Benchmarking*. Washington D.C.
5. McKinney, W. (2022). *Python for Data Analysis* (3.ª ed.). O'Reilly Media.
6. Plotly Technologies Inc. (2024). *Plotly 6.x documentation*. Montreal, QC.

---

## 👤 Autor

**Daniel Gallardo Monsalves**

📚 Diplomado en Python para la Toma Estratégica de Decisiones Organizacionales
🏛️ Universidad Andrés Bello (UNAB) | Abril 2026


---

> *Este informe fue elaborado con fines académicos. Los datos utilizados son de carácter sintético, generados programáticamente con parámetros calibrados a partir de los informes públicos de la SISS.*

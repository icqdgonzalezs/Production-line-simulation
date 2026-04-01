# 🏭 Simulación de Línea de Envasado — Snacks & Cereales

Proyecto de simulación, balance y análisis de OEE para líneas de envasado de
alimentos sólidos. Motor de simulación de eventos discretos con análisis Monte
Carlo y dashboard interactivo.

## Stack tecnológico

| Módulo | Librería | Propósito |
|--------|----------|-----------|
| Simulación | `simpy 4.1` | Eventos discretos (fallas, buffers, flujo) |
| Análisis numérico | `numpy`, `scipy` | Estadística, optimización |
| Datos | `pandas` | Tablas de resultados |
| Dashboard | `plotly` | HTML interactivo |
| Gráficos | `matplotlib` | Figuras estáticas / PDF |
| Reportes | `openpyxl` | Excel multi-hoja |
| Config | `pyyaml` | Parámetros sin tocar código |
| CLI | `rich` | Output en consola profesional |
| Tests | `pytest` | 20+ tests unitarios |

## Instalación (VS Code)

```bash
# 1. Crear entorno virtual
python -m venv .venv
source .venv/bin/activate          # Linux / Mac
.venv\Scripts\activate             # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Correr la simulación
python main.py

# 4. Opciones avanzadas
python main.py --replications 50           # más réplicas Monte Carlo
python main.py --config config/mi_linea.yaml  # otra configuración
python main.py --no-dashboard              # solo consola, sin HTML

# 5. Tests
pytest tests/ -v --cov=src --cov-report=term-missing
```

## Estructura del proyecto

```
production_line/
├── config/
│   └── line_config.yaml       # ← CONFIGURA AQUÍ tu línea
├── data/                      # CSVs de entrada (logs reales)
├── src/
│   ├── models.py              # Dataclasses: Station, LineMetrics, OEE
│   ├── simulator.py           # Motor SimPy + Monte Carlo
│   ├── oee.py                 # OEE: A × P × Q, estadísticas MC
│   ├── bottleneck.py          # 3 métodos detección CB + Cp/Cpk
│   ├── reporter.py            # Dashboard Plotly + PNG + Excel
│   └── config_loader.py       # Carga YAML → dataclasses
├── tests/
│   └── test_simulator.py      # 20+ tests unitarios
├── reports/                   # Salida automática
│   ├── dashboard.html         # Dashboard interactivo
│   ├── summary.png            # Figura resumen
│   └── analisis_linea.xlsx    # Excel multi-hoja
├── main.py                    # Orquestador CLI
└── requirements.txt
```

## Configurar tu línea real

Edita `config/line_config.yaml` con los datos reales de tu línea:

```yaml
stations:
  - id: S01
    name: "Nombre de la estación"
    rate_upm: 95.0        # velocidad nominal (unidades/minuto)
    cycle_time_std: 0.05  # variabilidad del ciclo (fracción, ej: 0.05 = ±5%)
    mtbf_min: 120         # tiempo medio entre fallas (minutos)
    mttr_min: 8           # tiempo medio de reparación (minutos)
    quality_rate: 0.998   # fracción de unidades conformes (0.998 = 99.8%)
```

## Salida del análisis

### Consola (Rich)
- Tabla OEE por estación (A, P, Q, OEE medio ± σ, percentiles P10/P50/P90)
- Tabla de frecuencia de cuello de botella (N réplicas MC)
- Panel resumen ejecutivo

### dashboard.html (Plotly)
1. OEE descompuesto por estación (barras agrupadas A/P/Q/OEE)
2. Distribución de throughput por estación (violín Monte Carlo)
3. Heatmap de pérdidas (semáforo verde/amarillo/rojo)
4. Frecuencia de detección de cuello de botella
5. Índices Cp / Cpk con línea de referencia 1.33
6. Balance de tiempos: Running / Starved / Bloqueado / Falla

### summary.png (Matplotlib)
4 paneles: OEE waterfall, boxplot Monte Carlo, balance horizontal, ranking CB.

### analisis_linea.xlsx
- Hoja 1: OEE por estación (media, std, percentiles)
- Hoja 2: Frecuencia de cuello de botella
- Hoja 3: Capacidad Cp/Cpk por estación
- Hoja 4: Producción por réplica

## Próximos módulos (Fase 2)

- `optimizer.py` — Balance de línea con `scipy.optimize` (What-If scenarios)
- `changeover.py` — Simulación de cambios de formato (SMED analysis)
- `scheduler.py` — Planificación de mantenimiento preventivo (PM scheduling)
- `sensitivity.py` — Análisis de sensibilidad por parámetro (tornado chart)

## Conceptos de ingeniería aplicados

| Concepto | Implementación |
|----------|----------------|
| OEE (ISO 22400) | `src/oee.py` — Disponibilidad × Rendimiento × Calidad |
| Cuello de botella | `src/bottleneck.py` — 3 métodos: utilización, throughput, score compuesto |
| MTBF / MTTR | `src/simulator.py` — distribución exponencial (zona de vida útil) |
| Índices Cp/Cpk | `src/bottleneck.py` — capacidad de proceso de tiempos de ciclo |
| Monte Carlo | `src/simulator.py` — N réplicas con semillas deterministas |
| Buffers finitos | `simpy.Container` — modelado de bloqueo y hambre |
| Variabilidad | Normal truncada en tiempos de ciclo (±30% del nominal) |

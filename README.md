# 🏭 Production Line Simulation in Python

## 📌 Description

This project simulates a production line using Python. It models workstations, failures, maintenance events, energy consumption, and scrap generation, while calculating key industrial KPIs.

The system also includes an interactive dashboard and automated report generation in Excel and PDF formats.

---

## 🎯 Project Objectives

* Simulate the operation of a production line
* Identify bottlenecks
* Calculate key industrial KPIs (OEE, TEEP, scrap, energy consumption)
* Analyze failures and maintenance (MTBF, MTTR)
* Generate automated reports (Excel & PDF)
* Visualize results through an interactive web dashboard

---

## 📊 KPIs Calculated

* **OEE** (Overall Equipment Effectiveness)
* **TEEP** (Total Effective Equipment Performance)
* **Throughput** (Production Rate)
* **Scrap / Waste**
* **Energy Consumption** (kWh/ton)
* **MTBF** (Mean Time Between Failures)
* **MTTR** (Mean Time To Repair)
* **FMEA Analysis**
* **Statistical Process Control (SPC, Cp, Cpk)**
* **Batch Traceability**

---

## 🛠️ Technologies Used

* Python
* SimPy (Discrete Event Simulation)
* Pandas (Data Analysis)
* Plotly / Dash (Interactive Dashboard)
* OpenPyXL (Excel Export)
* ReportLab (PDF Generation)
* YAML (Configuration Files)
* Git & GitHub (Version Control)

---

## 📁 Project Structure

```
production_line/
│
├── config/              # Line configuration files (YAML)
├── src/                 # Core modules
│   ├── models.py
│   ├── simulator.py
│   ├── kpis.py
│   ├── export.py
│   └── config_loader.py
│
├── dashboard_app.py     # Web dashboard
├── main.py              # Main execution
├── requirements.txt
├── reports/
└── tests/
```

---

## ⚙️ How to Run the Project

### 1. Create virtual environment

```bash
python -m venv .venv
```

### 2. Activate virtual environment

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the dashboard

```bash
python dashboard_app.py
```

### 5. Open in browser

```
http://127.0.0.1:8050
```

---

## 🧠 Engineering Applications

This project integrates concepts from:

* Process Engineering
* Industrial Engineering
* Production System Simulation
* Continuous Improvement
* Industrial Maintenance
* Industrial Data Analysis
* Industry 4.0
* Process Optimization

---

## 👨‍💻 Author

**David González Santibañez**
Chemical Engineer – Process Engineer

This project was developed as a practical application of Python in process engineering, production line simulation, and industrial data analysis.

"""
main.py — Orquestador principal del proyecto de simulación de línea de envasado.

Uso:
    python main.py                          # configuración por defecto
    python main.py --config config/mi.yaml  # config personalizada
    python main.py --replications 50        # más réplicas MC
    python main.py --no-dashboard           # sin HTML interactivo

Salida:
    reports/dashboard.html   — dashboard Plotly interactivo
    reports/summary.png      — figura resumen Matplotlib
    reports/analisis_linea.xlsx — export Excel
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track
from rich import box

from src.config_loader import load_config, parse_station_configs
from src.simulator import run_monte_carlo
from src.oee import analyze_monte_carlo, oee_to_dataframe
from src.bottleneck import detect_bottleneck, aggregate_bottleneck_results
from src.reporter import build_plotly_dashboard, build_matplotlib_summary, export_excel

console = Console()


def print_header(cfg: dict) -> None:
    line_cfg = cfg["line"]
    console.print(Panel(
        f"[bold cyan]{line_cfg['name']}[/bold cyan]\n"
        f"Producto: [yellow]{line_cfg['product']}[/yellow]\n"
        f"Turno: {line_cfg['shift_duration_min']} min | "
        f"Target: {line_cfg['target_rate_upm']} upm | "
        f"Réplicas: {line_cfg['sim_replications']}",
        title="[bold]Simulación de Línea de Envasado[/bold]",
        border_style="cyan",
    ))


def print_oee_table(oee_df) -> None:
    table = Table(title="OEE por Estación (Media Monte Carlo)",
                  box=box.ROUNDED, border_style="blue")
    for col in oee_df.columns:
        table.add_column(col, justify="right" if col != "Estación" else "left")
    for _, row in oee_df.iterrows():
        style = "bold red" if float(row["OEE Medio (%)"]) < 75 else ""
        table.add_row(*[str(v) for v in row], style=style)
    console.print(table)


def print_bottleneck_table(bn_df) -> None:
    table = Table(title="Frecuencia de Cuello de Botella",
                  box=box.ROUNDED, border_style="red")
    for col in bn_df.columns:
        table.add_column(col, justify="right" if col != "Estación" else "left")
    for _, row in bn_df.iterrows():
        style = "bold red" if float(row["Frecuencia CB (%)"]) > 40 else ""
        table.add_row(*[str(v) for v in row], style=style)
    console.print(table)


def main(args: argparse.Namespace) -> None:
    t0 = time.perf_counter()

    # ── Cargar configuración ──────────────────────────────────────────────────
    cfg = load_config(args.config)
    line_cfg = cfg["line"]
    stations = parse_station_configs(cfg)
    n_reps = args.replications or line_cfg["sim_replications"]
    print_header(cfg)

    # ── Simulación Monte Carlo ────────────────────────────────────────────────
    console.print(f"\n[bold]Ejecutando {n_reps} réplicas Monte Carlo...[/bold]")
    replications = []
    for r in track(range(n_reps), description="Simulando..."):
        from src.simulator import run_replication
        rep = run_replication(
            station_configs=stations,
            shift_duration_min=line_cfg["shift_duration_min"],
            buffer_capacity=cfg["conveyors"]["buffer_capacity"],
            transport_time_min=cfg["conveyors"]["transport_time_min"],
            target_rate_upm=line_cfg["target_rate_upm"],
            line_name=line_cfg["name"],
            product=line_cfg["product"],
            replication_id=r,
            seed=42 + r,
        )
        replications.append(rep)

    elapsed_sim = time.perf_counter() - t0
    console.print(f"[green]✓ Simulación completada en {elapsed_sim:.2f}s[/green]\n")

    # ── Análisis OEE ──────────────────────────────────────────────────────────
    oee_stats = analyze_monte_carlo(replications)
    oee_df    = oee_to_dataframe(oee_stats)
    print_oee_table(oee_df)

    # ── Cuello de botella ─────────────────────────────────────────────────────
    bn_df = aggregate_bottleneck_results(replications)
    print_bottleneck_table(bn_df)

    # OEE global de línea
    import numpy as np
    line_oees = [r.line_oee * 100 for r in replications]
    console.print(Panel(
        f"OEE Línea (mínimo entre estaciones):\n"
        f"  Media: [bold cyan]{np.mean(line_oees):.1f}%[/bold cyan]  "
        f"P10: {np.percentile(line_oees, 10):.1f}%  "
        f"P90: {np.percentile(line_oees, 90):.1f}%\n"
        f"  Producción media/turno: "
        f"[bold yellow]{np.mean([r.total_output for r in replications]):.0f} uds[/bold yellow]",
        title="[bold]Resumen Ejecutivo[/bold]",
        border_style="green",
    ))

    # ── Reportes ──────────────────────────────────────────────────────────────
    if not args.no_dashboard:
        console.print("\n[bold]Generando reportes...[/bold]")
        build_plotly_dashboard(replications)
        build_matplotlib_summary(replications)
        export_excel(replications)
        console.print("[green]✓ Reportes generados en reports/[/green]")

    total_time = time.perf_counter() - t0
    console.print(f"\n[bold green]✓ Análisis completo en {total_time:.2f}s[/bold green]")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Simulación y análisis de línea de envasado"
    )
    parser.add_argument(
        "--config", default="config/line_config.yaml",
        help="Ruta al archivo de configuración YAML"
    )
    parser.add_argument(
        "--replications", type=int, default=None,
        help="Número de réplicas Monte Carlo (sobreescribe config)"
    )
    parser.add_argument(
        "--no-dashboard", action="store_true",
        help="Omitir generación de reportes"
    )
    main(parser.parse_args())

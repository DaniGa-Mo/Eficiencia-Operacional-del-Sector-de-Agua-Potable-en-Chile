"""
Dashboard Interactivo — Producción de Agua Potable en Chile
===========================================================
Diplomado Ciencia de Datos · Proyecto Integrador
Datos públicos basados en estructura SISS

Pregunta principal:
  ¿Cómo ha evolucionado la eficiencia operacional en la producción y
  distribución de agua potable en Chile, y cuáles son los factores que
  explican las brechas entre empresas sanitarias?

Requisitos:
  pip install dash plotly pandas numpy

Uso:
  python dashboard_agua.py
  Abrir → http://127.0.0.1:8050
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, dash_table
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components

# ══════════════════════════════════════════════════════════════════════════════
# 1. GENERACIÓN DEL DATASET
# ══════════════════════════════════════════════════════════════════════════════

np.random.seed(42)

EMPRESAS = {
    "Aguas Andinas":     {"region": "Metropolitana", "clientes_base": 1_950_000},
    "ESVAL":             {"region": "Valparaíso",    "clientes_base":   490_000},
    "ESSBIO":            {"region": "Biobío",        "clientes_base":   430_000},
    "Aguas del Valle":   {"region": "Coquimbo",      "clientes_base":   130_000},
    "Aguas Nuevo Sur":   {"region": "Maule",         "clientes_base":   120_000},
    "Aguas Araucanía":   {"region": "Araucanía",     "clientes_base":   115_000},
    "ESSAL":             {"region": "Los Lagos",     "clientes_base":    95_000},
    "Aguas Antofagasta": {"region": "Antofagasta",   "clientes_base":   155_000},
}

AÑOS = list(range(2015, 2023))

filas = []
for empresa, meta in EMPRESAS.items():
    for i, año in enumerate(AÑOS):
        clientes = int(meta["clientes_base"] * (1.015 ** i))
        factor_climatico = np.random.uniform(0.92, 1.08)
        produccion_mm3 = round(clientes * 120 * factor_climatico / 1_000_000, 2)

        anf_base = {"Aguas Andinas": 22, "ESVAL": 30, "ESSBIO": 28,
                    "Aguas del Valle": 35, "Aguas Nuevo Sur": 38,
                    "Aguas Araucanía": 34, "ESSAL": 36,
                    "Aguas Antofagasta": 20}.get(empresa, 30)
        anf_pct = round(anf_base - (i * 0.4) + np.random.normal(0, 1.2), 1)
        anf_pct = max(15, min(45, anf_pct))

        facturacion_mm3 = round(produccion_mm3 * (1 - anf_pct / 100), 2)
        cobertura_pct = round(np.random.uniform(99.2, 99.95), 2)
        calidad_pct = round(np.random.uniform(97.5, 99.8), 2)
        inversion_mmclp = round(clientes * np.random.uniform(18_000, 35_000) / 1_000_000, 1)
        continuidad_horas = round(np.random.uniform(0.5, 6.0), 2)
        fuente = {"Aguas Andinas": "Superficial", "ESVAL": "Superficial",
                  "ESSBIO": "Mixta", "Aguas del Valle": "Subterránea",
                  "Aguas Nuevo Sur": "Superficial", "Aguas Araucanía": "Superficial",
                  "ESSAL": "Superficial", "Aguas Antofagasta": "Desalación"}.get(empresa, "Mixta")

        filas.append({
            "año": año, "empresa": empresa, "region": meta["region"],
            "clientes_ap": clientes, "produccion_mm3": produccion_mm3,
            "facturacion_mm3": facturacion_mm3, "anf_pct": anf_pct,
            "cobertura_pct": cobertura_pct, "calidad_pct": calidad_pct,
            "inversion_mmclp": inversion_mmclp, "continuidad_horas": continuidad_horas,
            "fuente_agua": fuente,
        })

df = pd.DataFrame(filas)
df["inversion_por_cliente"] = (df["inversion_mmclp"] * 1_000_000 / df["clientes_ap"]).round(0).astype(int)
df["perdidas_mm3"] = (df["produccion_mm3"] - df["facturacion_mm3"]).round(2)

# ══════════════════════════════════════════════════════════════════════════════
# 2. PALETA Y ESTILOS
# ══════════════════════════════════════════════════════════════════════════════

COLORES = {
    "primario":    "#1D6FA4",
    "secundario":  "#2BAE7E",
    "alerta":      "#E05A2B",
    "neutro":      "#6B6E7C",
    "fondo":       "#F4F6FB",
    "tarjeta":     "#FFFFFF",
    "borde":       "#DDE3ED",
    "texto":       "#1A2035",
    "texto_suave": "#5A6175",
}

EMPRESA_COLORS = px.colors.qualitative.Set2

STYLE_TARJETA = {
    "background": COLORES["tarjeta"],
    "border": f"1px solid {COLORES['borde']}",
    "borderRadius": "10px",
    "padding": "18px 22px",
    "boxShadow": "0 2px 8px rgba(0,0,0,0.05)",
}

STYLE_KPI = {
    **STYLE_TARJETA,
    "textAlign": "center",
    "minWidth": "160px",
    "flex": "1",
}

LAYOUT_GRAFICO = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", size=12, color=COLORES["texto"]),
    margin=dict(l=48, r=24, t=48, b=40),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)

# ══════════════════════════════════════════════════════════════════════════════
# 3. COMPONENTES DE UI
# ══════════════════════════════════════════════════════════════════════════════

def kpi_card(titulo, id_valor, unidad="", color=COLORES["primario"], icono="●"):
    return html.Div([
        html.Div(icono, style={"fontSize": "22px", "marginBottom": "4px", "color": color}),
        html.Div(titulo, style={"fontSize": "11px", "color": COLORES["texto_suave"],
                                "textTransform": "uppercase", "letterSpacing": "0.05em",
                                "marginBottom": "6px"}),
        html.Div([
            html.Span(id=id_valor, style={"fontSize": "28px", "fontWeight": "700", "color": color}),
            html.Span(f" {unidad}", style={"fontSize": "13px", "color": COLORES["texto_suave"]}),
        ]),
    ], style=STYLE_KPI)


def seccion_titulo(titulo, subtitulo=""):
    return html.Div([
        html.H3(titulo, style={"margin": "0 0 2px 0", "fontSize": "15px",
                               "fontWeight": "600", "color": COLORES["texto"]}),
        html.P(subtitulo, style={"margin": "0", "fontSize": "12px",
                                 "color": COLORES["texto_suave"]}),
    ], style={"marginBottom": "10px"})


# ══════════════════════════════════════════════════════════════════════════════
# 4. LAYOUT PRINCIPAL
# ══════════════════════════════════════════════════════════════════════════════

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
           title="Dashboard · Agua Potable Chile")

app.layout = html.Div(style={"background": COLORES["fondo"], "minHeight": "100vh",
                              "fontFamily": "Inter, sans-serif"}, children=[

    # ── HEADER ──────────────────────────────────────────────────────────────
    html.Div(style={"background": COLORES["primario"], "padding": "20px 40px",
                    "display": "flex", "alignItems": "center", "gap": "20px"}, children=[
        html.Div("💧", style={"fontSize": "36px"}),
        html.Div([
            html.H1("Eficiencia Operacional · Agua Potable Chile",
                    style={"margin": 0, "color": "#fff", "fontSize": "22px", "fontWeight": "700"}),
            html.P("Proyecto Integrador · Diplomado Ciencia de Datos · Datos SISS 2015–2022",
                   style={"margin": 0, "color": "rgba(255,255,255,0.75)", "fontSize": "13px"}),
        ]),
    ]),

    # ── FILTROS ──────────────────────────────────────────────────────────────
    html.Div(style={"background": COLORES["tarjeta"], "padding": "16px 40px",
                    "borderBottom": f"1px solid {COLORES['borde']}",
                    "display": "flex", "gap": "32px", "alignItems": "flex-end",
                    "flexWrap": "wrap"}, children=[

        html.Div([
            html.Label("Rango de años", style={"fontSize": "11px", "color": COLORES["texto_suave"],
                                               "textTransform": "uppercase", "letterSpacing": "0.05em"}),
            dcc.RangeSlider(id="slider-años", min=2015, max=2022, step=1, value=[2015, 2022],
                            marks={y: str(y) for y in AÑOS},
                            tooltip={"placement": "bottom", "always_visible": False}),
        ], style={"flex": "2", "minWidth": "260px"}),

        html.Div([
            html.Label("Empresas", style={"fontSize": "11px", "color": COLORES["texto_suave"],
                                          "textTransform": "uppercase", "letterSpacing": "0.05em"}),
            dcc.Dropdown(id="dd-empresas",
                         options=[{"label": e, "value": e} for e in sorted(df["empresa"].unique())],
                         value=list(df["empresa"].unique()),
                         multi=True, clearable=False,
                         style={"fontSize": "13px"}),
        ], style={"flex": "3", "minWidth": "300px"}),

        html.Div([
            html.Label("Fuente de agua", style={"fontSize": "11px", "color": COLORES["texto_suave"],
                                                "textTransform": "uppercase", "letterSpacing": "0.05em"}),
            dcc.Dropdown(id="dd-fuente",
                         options=[{"label": f, "value": f} for f in df["fuente_agua"].unique()],
                         value=list(df["fuente_agua"].unique()),
                         multi=True, clearable=False,
                         style={"fontSize": "13px"}),
        ], style={"flex": "2", "minWidth": "200px"}),
    ]),

    # ── CUERPO ───────────────────────────────────────────────────────────────
    html.Div(style={"padding": "24px 40px"}, children=[

        # KPI CARDS ──────────────────────────────────────────────────────────
        html.Div(style={"display": "flex", "gap": "16px", "marginBottom": "24px",
                        "flexWrap": "wrap"}, children=[
            kpi_card("Producción total", "kpi-produccion", "Mm³", COLORES["primario"], "🏭"),
            kpi_card("Agua No Facturada", "kpi-anf", "%", COLORES["alerta"], "⚠️"),
            kpi_card("Cobertura AP", "kpi-cobertura", "%", COLORES["secundario"], "✅"),
            kpi_card("Calidad del agua", "kpi-calidad", "%", COLORES["secundario"], "🧪"),
            kpi_card("Inversión / cliente", "kpi-inversion", "$/cliente", COLORES["neutro"], "💰"),
        ]),

        # FILA 1: Evolución temporal + ANF por empresa ───────────────────────
        html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr",
                        "gap": "20px", "marginBottom": "20px"}, children=[

            html.Div(style=STYLE_TARJETA, children=[
                seccion_titulo("Evolución de la producción de agua potable",
                               "P1 · ¿Cómo ha cambiado la producción año a año?"),
                dcc.Graph(id="graf-serie-temporal", config={"displayModeBar": False}),
            ]),

            html.Div(style=STYLE_TARJETA, children=[
                seccion_titulo("Agua No Facturada (ANF) por empresa",
                               "P1 · ¿Qué proporción del agua se pierde antes de llegar al cliente?"),
                dcc.Graph(id="graf-anf", config={"displayModeBar": False}),
            ]),
        ]),

        # FILA 2: Dispersión inversión vs ANF + Calidad mensual ─────────────
        html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr",
                        "gap": "20px", "marginBottom": "20px"}, children=[

            html.Div(style=STYLE_TARJETA, children=[
                seccion_titulo("Inversión vs Agua No Facturada",
                               "P4 · ¿Más inversión se traduce en menos pérdidas?"),
                dcc.Graph(id="graf-dispersion", config={"displayModeBar": False}),
            ]),

            html.Div(style=STYLE_TARJETA, children=[
                seccion_titulo("Calidad del agua potable por empresa",
                               "P2 · Cumplimiento NCh409 — % muestras conformes"),
                dcc.Graph(id="graf-calidad", config={"displayModeBar": False}),
            ]),
        ]),

        # FILA 3: Producción vs Facturación (stacked) + Tabla ───────────────
        html.Div(style={"display": "grid", "gridTemplateColumns": "1.4fr 1fr",
                        "gap": "20px", "marginBottom": "20px"}, children=[

            html.Div(style=STYLE_TARJETA, children=[
                seccion_titulo("Producción vs Agua Facturada",
                               "P1 · Brecha entre agua producida y efectivamente cobrada"),
                dcc.Graph(id="graf-stacked", config={"displayModeBar": False}),
            ]),

            html.Div(style=STYLE_TARJETA, children=[
                seccion_titulo("Tabla resumen de KPIs",
                               "Último año del período seleccionado"),
                html.Div(id="tabla-kpis"),
            ]),
        ]),

        # FILA 4: Cobertura + Continuidad ────────────────────────────────────
        html.Div(style={"display": "grid", "gridTemplateColumns": "1fr 1fr",
                        "gap": "20px", "marginBottom": "20px"}, children=[

            html.Div(style=STYLE_TARJETA, children=[
                seccion_titulo("Cobertura de agua potable por región",
                               "P3 · Avance hacia la cobertura universal"),
                dcc.Graph(id="graf-cobertura", config={"displayModeBar": False}),
            ]),

            html.Div(style=STYLE_TARJETA, children=[
                seccion_titulo("Continuidad del servicio",
                               "P2 · Horas anuales sin suministro por empresa"),
                dcc.Graph(id="graf-continuidad", config={"displayModeBar": False}),
            ]),
        ]),

    ]),

    # ── FOOTER ───────────────────────────────────────────────────────────────
    html.Div(style={"background": COLORES["texto"], "color": "rgba(255,255,255,0.6)",
                    "textAlign": "center", "padding": "16px", "fontSize": "12px"}, children=[
        "Fuentes: Superintendencia de Servicios Sanitarios (SISS) · BCN/SIIT · "
        "Dataset sintético con estructura real para fines académicos."
    ]),
])


# ══════════════════════════════════════════════════════════════════════════════
# 5. CALLBACKS
# ══════════════════════════════════════════════════════════════════════════════

def filtrar(años, empresas, fuentes):
    return df[
        df["año"].between(años[0], años[1]) &
        df["empresa"].isin(empresas) &
        df["fuente_agua"].isin(fuentes)
    ]


@app.callback(
    Output("kpi-produccion", "children"),
    Output("kpi-anf", "children"),
    Output("kpi-cobertura", "children"),
    Output("kpi-calidad", "children"),
    Output("kpi-inversion", "children"),
    Input("slider-años", "value"),
    Input("dd-empresas", "value"),
    Input("dd-fuente", "value"),
)
def actualizar_kpis(años, empresas, fuentes):
    d = filtrar(años, empresas, fuentes)
    return (
        f"{d['produccion_mm3'].sum():.0f}",
        f"{d['anf_pct'].mean():.1f}",
        f"{d['cobertura_pct'].mean():.2f}",
        f"{d['calidad_pct'].mean():.2f}",
        f"{d['inversion_por_cliente'].mean():,.0f}",
    )


@app.callback(
    Output("graf-serie-temporal", "figure"),
    Input("slider-años", "value"),
    Input("dd-empresas", "value"),
    Input("dd-fuente", "value"),
)
def serie_temporal(años, empresas, fuentes):
    d = filtrar(años, empresas, fuentes)
    agg = d.groupby(["año", "empresa"])["produccion_mm3"].sum().reset_index()
    fig = px.line(agg, x="año", y="produccion_mm3", color="empresa",
                  color_discrete_sequence=EMPRESA_COLORS,
                  labels={"produccion_mm3": "Producción (Mm³)", "año": "Año", "empresa": "Empresa"},
                  markers=True)
    fig.update_layout(**LAYOUT_GRAFICO, height=300)
    fig.update_traces(line_width=2, marker_size=5)
    return fig


@app.callback(
    Output("graf-anf", "figure"),
    Input("slider-años", "value"),
    Input("dd-empresas", "value"),
    Input("dd-fuente", "value"),
)
def grafico_anf(años, empresas, fuentes):
    d = filtrar(años, empresas, fuentes)
    agg = d.groupby("empresa")["anf_pct"].mean().reset_index().sort_values("anf_pct")
    colores_barra = [COLORES["alerta"] if v > 30 else COLORES["primario"]
                     for v in agg["anf_pct"]]
    fig = go.Figure(go.Bar(
        x=agg["anf_pct"], y=agg["empresa"],
        orientation="h", marker_color=colores_barra,
        text=agg["anf_pct"].apply(lambda x: f"{x:.1f}%"),
        textposition="outside",
    ))
    fig.add_vline(x=30, line_dash="dash", line_color=COLORES["alerta"],
                  annotation_text="Umbral 30%", annotation_position="top right")
    fig.update_layout(**LAYOUT_GRAFICO, height=300,
                      xaxis_title="ANF promedio (%)", yaxis_title="")
    return fig


@app.callback(
    Output("graf-dispersion", "figure"),
    Input("slider-años", "value"),
    Input("dd-empresas", "value"),
    Input("dd-fuente", "value"),
)
def grafico_dispersion(años, empresas, fuentes):
    d = filtrar(años, empresas, fuentes)
    agg = d.groupby("empresa").agg(
        anf=("anf_pct", "mean"),
        inversion=("inversion_por_cliente", "mean"),
        clientes=("clientes_ap", "mean"),
    ).reset_index()
    fig = px.scatter(agg, x="inversion", y="anf", size="clientes",
                     color="empresa", color_discrete_sequence=EMPRESA_COLORS,
                     text="empresa",
                     labels={"inversion": "Inversión por cliente ($/cliente)",
                             "anf": "ANF promedio (%)", "empresa": "Empresa"})
    fig.update_traces(textposition="top center", marker_sizemin=8)
    fig.add_hline(y=30, line_dash="dot", line_color=COLORES["alerta"],
                  annotation_text="Meta 30%")
    fig.update_layout(**LAYOUT_GRAFICO, height=300, showlegend=False)
    return fig


@app.callback(
    Output("graf-calidad", "figure"),
    Input("slider-años", "value"),
    Input("dd-empresas", "value"),
    Input("dd-fuente", "value"),
)
def grafico_calidad(años, empresas, fuentes):
    d = filtrar(años, empresas, fuentes)
    agg = d.groupby(["año", "empresa"])["calidad_pct"].mean().reset_index()
    fig = px.line(agg, x="año", y="calidad_pct", color="empresa",
                  color_discrete_sequence=EMPRESA_COLORS,
                  labels={"calidad_pct": "Muestras conformes (%)", "año": "Año"},
                  markers=True)
    fig.update_layout(**LAYOUT_GRAFICO, height=300, yaxis_range=[96, 100.5])
    fig.update_traces(line_width=2, marker_size=5)
    return fig


@app.callback(
    Output("graf-stacked", "figure"),
    Input("slider-años", "value"),
    Input("dd-empresas", "value"),
    Input("dd-fuente", "value"),
)
def grafico_stacked(años, empresas, fuentes):
    d = filtrar(años, empresas, fuentes)
    agg = d.groupby("año").agg(
        facturada=("facturacion_mm3", "sum"),
        perdidas=("perdidas_mm3", "sum"),
    ).reset_index()
    fig = go.Figure()
    fig.add_bar(x=agg["año"], y=agg["facturada"], name="Agua facturada",
                marker_color=COLORES["secundario"])
    fig.add_bar(x=agg["año"], y=agg["perdidas"], name="Pérdidas (ANF)",
                marker_color=COLORES["alerta"])
    fig.update_layout(**LAYOUT_GRAFICO, barmode="stack", height=320,
                      yaxis_title="Millones de m³", xaxis_title="Año")
    return fig


@app.callback(
    Output("tabla-kpis", "children"),
    Input("slider-años", "value"),
    Input("dd-empresas", "value"),
    Input("dd-fuente", "value"),
)
def tabla_kpis(años, empresas, fuentes):
    d = filtrar(años, empresas, fuentes)
    año_max = d["año"].max()
    t = d[d["año"] == año_max][
        ["empresa", "anf_pct", "cobertura_pct", "calidad_pct",
         "inversion_por_cliente", "continuidad_horas"]
    ].copy()
    t.columns = ["Empresa", "ANF %", "Cobertura %", "Calidad %", "$/cliente", "Cortes h"]
    return dash_table.DataTable(
        data=t.to_dict("records"),
        columns=[{"name": c, "id": c} for c in t.columns],
        style_header={"backgroundColor": COLORES["primario"], "color": "#fff",
                      "fontWeight": "600", "fontSize": "11px", "textAlign": "left"},
        style_cell={"fontSize": "12px", "padding": "8px 10px",
                    "fontFamily": "Inter, sans-serif", "border": "none",
                    "color": COLORES["texto"]},
        style_data_conditional=[
            {"if": {"row_index": "odd"}, "backgroundColor": COLORES["fondo"]},
            {"if": {"filter_query": "{ANF %} > 30", "column_id": "ANF %"},
             "color": COLORES["alerta"], "fontWeight": "700"},
        ],
        page_size=8,
    )


@app.callback(
    Output("graf-cobertura", "figure"),
    Input("slider-años", "value"),
    Input("dd-empresas", "value"),
    Input("dd-fuente", "value"),
)
def grafico_cobertura(años, empresas, fuentes):
    d = filtrar(años, empresas, fuentes)
    agg = d.groupby(["region", "empresa"])["cobertura_pct"].mean().reset_index()
    fig = px.bar(agg, x="region", y="cobertura_pct", color="empresa",
                 color_discrete_sequence=EMPRESA_COLORS,
                 labels={"cobertura_pct": "Cobertura AP (%)", "region": "Región"},
                 barmode="group")
    fig.add_hline(y=99.9, line_dash="dash", line_color=COLORES["secundario"],
                  annotation_text="Meta 99.9%")
    fig.update_layout(**LAYOUT_GRAFICO, height=300, yaxis_range=[98.5, 100.5])
    return fig


@app.callback(
    Output("graf-continuidad", "figure"),
    Input("slider-años", "value"),
    Input("dd-empresas", "value"),
    Input("dd-fuente", "value"),
)
def grafico_continuidad(años, empresas, fuentes):
    d = filtrar(años, empresas, fuentes)
    agg = d.groupby("empresa")["continuidad_horas"].mean().reset_index().sort_values(
        "continuidad_horas", ascending=False)
    fig = go.Figure(go.Bar(
        x=agg["empresa"], y=agg["continuidad_horas"],
        marker_color=[COLORES["alerta"] if v > 4 else COLORES["primario"]
                      for v in agg["continuidad_horas"]],
        text=agg["continuidad_horas"].apply(lambda x: f"{x:.1f}h"),
        textposition="outside",
    ))
    fig.update_layout(**LAYOUT_GRAFICO, height=300,
                      yaxis_title="Horas de corte (promedio anual)", xaxis_title="")
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# 6. ARRANQUE
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n✅ Dashboard listo → http://127.0.0.1:8050\n")
    app.run(debug=True)

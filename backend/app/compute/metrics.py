from typing import Dict
import pandas as pd

def compute_metrics(
    dfs: Dict[str, pd.DataFrame],
    unit_costs: pd.DataFrame
) -> pd.DataFrame:
    """
    Returns product-level metrics for the selected period (ventas already filtered upstream if needed).
    """
    productos = dfs["productos"]
    ventas = dfs["ventas"]

    unidades = ventas.groupby("producto_id", as_index=False)["cantidad_vendida"].sum()
    unidades = unidades.rename(columns={"cantidad_vendida": "unidades_periodo"})

    m = productos.merge(unit_costs, on="producto_id", how="left").merge(unidades, on="producto_id", how="left")
    m["unidades_periodo"] = m["unidades_periodo"].fillna(0.0)

    m["precio"] = m["precio_venta_actual"]
    m["ingreso_total"] = m["precio"] * m["unidades_periodo"]

    m["margen_abs_unit"] = m["precio"] - m["costo_total_unit"]
    # Evitar división por cero
    m["margen_pct"] = m.apply(lambda r: (r["margen_abs_unit"] / r["precio"]) if r["precio"] else 0.0, axis=1)

    m["contribucion_total"] = m["margen_abs_unit"] * m["unidades_periodo"]
    m["perdida_total"] = m.apply(lambda r: (-r["margen_abs_unit"] * r["unidades_periodo"]) if r["margen_abs_unit"] < 0 else 0.0, axis=1)

    # Eficiencia (min por $ de margen positivo). Si margen<=0, eficiencia = infinito conceptual -> usamos None
    def eff(r):
        if r["margen_abs_unit"] <= 0:
            return None
        return float(r["tiempo_total_min"]) / float(r["margen_abs_unit"]) if r["margen_abs_unit"] else None

    m["eficiencia_min_por_margen"] = m.apply(eff, axis=1)

    # Columnas finales útiles
    cols = [
        "producto_id", "nombre_producto", "categoria",
        "precio", "unidades_periodo", "ingreso_total",
        "costo_insumos_unit", "costo_esfuerzo_unit", "costo_indirectos_unit", "costo_total_unit",
        "margen_abs_unit", "margen_pct",
        "contribucion_total", "perdida_total",
        "tiempo_total_min", "eficiencia_min_por_margen",
    ]
    return m[cols]

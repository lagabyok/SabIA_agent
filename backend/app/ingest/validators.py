from typing import Dict
import pandas as pd

REQUIRED_COLUMNS = {
    "productos": {"producto_id", "nombre_producto", "categoria", "precio_venta_actual"},
    "ventas": {"fecha", "producto_id", "cantidad_vendida"},
    "insumos": {"insumo_id", "nombre_insumo", "unidad", "costo_unitario"},
    "recetas": {"producto_id", "insumo_id", "cantidad"},
    "tiempos_produccion": {"producto_id", "tiempo_total_min"},
    "gastos_generales": {"tipo_gasto", "monto_mensual"},
}

def validate_schema(dfs: Dict[str, pd.DataFrame]) -> None:
    missing = []
    for name, cols in REQUIRED_COLUMNS.items():
        if name not in dfs:
            missing.append(f"Falta dataset: {name}")
            continue
        df = dfs[name]
        df_cols = set(df.columns)
        if not cols.issubset(df_cols):
            missing_cols = cols - df_cols
            missing.append(f"{name}: faltan columnas {sorted(list(missing_cols))}")
    if missing:
        raise ValueError("Validación fallida:\n- " + "\n- ".join(missing))

def basic_cleaning(dfs: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    # Tipos mínimos para demo
    p = dfs["productos"].copy()
    p["producto_id"] = p["producto_id"].astype(str).str.strip()
    p["precio_venta_actual"] = p["precio_venta_actual"].astype(float)

    v = dfs["ventas"].copy()
    v["producto_id"] = v["producto_id"].astype(str).str.strip()
    v["cantidad_vendida"] = v["cantidad_vendida"].astype(float)

    i = dfs["insumos"].copy()
    i["insumo_id"] = i["insumo_id"].astype(str).str.strip()
    i["costo_unitario"] = i["costo_unitario"].astype(float)

    r = dfs["recetas"].copy()
    r["producto_id"] = r["producto_id"].astype(str).str.strip()
    r["insumo_id"] = r["insumo_id"].astype(str).str.strip()
    r["cantidad"] = r["cantidad"].astype(float)

    t = dfs["tiempos_produccion"].copy()
    t["producto_id"] = t["producto_id"].astype(str).str.strip()
    t["tiempo_total_min"] = t["tiempo_total_min"].astype(float)

    g = dfs["gastos_generales"].copy()
    g["monto_mensual"] = g["monto_mensual"].astype(float)

    return {
        "productos": p,
        "ventas": v,
        "insumos": i,
        "recetas": r,
        "tiempos_produccion": t,
        "gastos_generales": g,
    }


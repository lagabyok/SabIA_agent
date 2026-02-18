from typing import Dict, Tuple
import pandas as pd

def compute_costs(
    dfs: Dict[str, pd.DataFrame],
    valor_minuto: float
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Returns:
      - unit_costs: producto_id, costo_insumos_unit, costo_esfuerzo_unit, costo_indirectos_unit, costo_total_unit
      - recipe_drivers: producto_id, nombre_insumo, costo_insumo_unit (para top drivers)
    """
    productos = dfs["productos"]
    ventas = dfs["ventas"]
    insumos = dfs["insumos"]
    recetas = dfs["recetas"]
    tiempos = dfs["tiempos_produccion"]
    gastos = dfs["gastos_generales"]

    # Unidades vendidas por producto (para prorrateo / KPIs)
    unidades = ventas.groupby("producto_id", as_index=False)["cantidad_vendida"].sum()
    unidades = unidades.rename(columns={"cantidad_vendida": "unidades_periodo"})

    # ===== Costo insumos unitario por producto =====
    # recetas * costo_unitario
    receta_cost = recetas.merge(insumos[["insumo_id", "nombre_insumo", "costo_unitario"]],
                               on="insumo_id", how="left")
    receta_cost["costo_insumo_unit"] = receta_cost["cantidad"] * receta_cost["costo_unitario"]

    # total por producto
    costo_insumos = receta_cost.groupby("producto_id", as_index=False)["costo_insumo_unit"].sum()
    costo_insumos = costo_insumos.rename(columns={"costo_insumo_unit": "costo_insumos_unit"})

    # drivers (por insumo) para explicación
    recipe_drivers = receta_cost.groupby(
        ["producto_id", "nombre_insumo"], as_index=False
    )["costo_insumo_unit"].sum()

    # ===== Costo esfuerzo unitario por producto =====
    esfuerzo = tiempos.copy()
    esfuerzo["costo_esfuerzo_unit"] = esfuerzo["tiempo_total_min"] * float(valor_minuto)
    esfuerzo = esfuerzo[["producto_id", "tiempo_total_min", "costo_esfuerzo_unit"]]

    # ===== Prorrateo gastos indirectos =====
    total_gastos = float(gastos["monto_mensual"].sum())
    total_unidades = float(unidades["unidades_periodo"].sum()) if len(unidades) else 0.0
    if total_unidades <= 0:
        costo_indirectos_unit = 0.0
    else:
        costo_indirectos_unit = total_gastos / total_unidades

    # ===== Combine =====
    unit_costs = productos[["producto_id"]].merge(costo_insumos, on="producto_id", how="left")
    unit_costs = unit_costs.merge(esfuerzo[["producto_id", "tiempo_total_min", "costo_esfuerzo_unit"]],
                                  on="producto_id", how="left")
    unit_costs["costo_insumos_unit"] = unit_costs["costo_insumos_unit"].fillna(0.0)
    unit_costs["tiempo_total_min"] = unit_costs["tiempo_total_min"].fillna(0.0)
    unit_costs["costo_esfuerzo_unit"] = unit_costs["costo_esfuerzo_unit"].fillna(0.0)

    unit_costs["costo_indirectos_unit"] = costo_indirectos_unit
    unit_costs["costo_total_unit"] = (
        unit_costs["costo_insumos_unit"]
        + unit_costs["costo_esfuerzo_unit"]
        + unit_costs["costo_indirectos_unit"]
    )

    return unit_costs, recipe_drivers

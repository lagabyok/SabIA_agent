from typing import Dict
import os
import pandas as pd
from .validators import validate_schema, basic_cleaning

FILES = {
    "productos": "productos.csv",
    "ventas": "ventas.csv",
    "insumos": "insumos.csv",
    "recetas": "recetas.csv",
    "tiempos_produccion": "tiempos_produccion.csv",
    "gastos_generales": "gastos_generales.csv",
}

def load_csvs(data_dir: str) -> Dict[str, pd.DataFrame]:
    dfs: Dict[str, pd.DataFrame] = {}
    for key, fname in FILES.items():
        path = os.path.join(data_dir, fname)
        if not os.path.exists(path):
            raise FileNotFoundError(f"No existe: {path}")
        dfs[key] = pd.read_csv(path)

    validate_schema(dfs)
    dfs = basic_cleaning(dfs)
    return dfs

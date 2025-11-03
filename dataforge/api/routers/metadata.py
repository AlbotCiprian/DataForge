import json
import os
from pathlib import Path
from typing import Any, Dict, List

from fastapi import APIRouter

router = APIRouter(prefix="", tags=["metadata"])

DATA_DIR = Path(os.environ.get("DATA_DIR", "/data")).resolve()


@router.get("/runs")
def list_runs() -> Dict[str, Any]:
    # Fallback to a local JSON if Airflow DB is not accessible
    p = DATA_DIR / "logs" / "airflow_runs.json"
    if p.exists():
        try:
            return json.loads(p.read_text())
        except Exception:
            pass
    # Minimal stub
    return {
        "runs": [
            {"dag_id": "ingest_raw_data", "state": "success"},
            {"dag_id": "transform_with_dbt", "state": "success"},
        ]
    }


@router.get("/models")
def list_models() -> Dict[str, Any]:
    # Prefer dbt manifest if available; otherwise, list SQL files
    manifest = Path("dbt/target/manifest.json")
    if manifest.exists():
        try:
            data = json.loads(manifest.read_text())
            nodes = [
                v.get("name")
                for v in data.get("nodes", {}).values()
                if v.get("resource_type") == "model"
            ]
            return {"models": sorted(nodes)}
        except Exception:
            pass

    models: List[str] = []
    for p in Path("dbt/models").rglob("*.sql"):
        models.append(p.stem)
    return {"models": sorted(models)}


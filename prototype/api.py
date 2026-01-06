from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from prototype.sparql_query_building import build_main_query
from prototype.sparql_utils import run_query


app = FastAPI(title="EPD SPARQL API", version="1.0.0")


class SparqlRequest(BaseModel):
    query: str = Field(..., min_length=1)


class MainQueryRequest(BaseModel):
    category: Optional[str] = None
    modules: Optional[List[str]] = None
    countries: Optional[List[str]] = None
    subtypes: Optional[List[str]] = None
    str_groups: Optional[List[str]] = None
    density_groups: Optional[List[str]] = None
    din_groups: Optional[List[str]] = None
    environ_thr: int = 1000
    lifecycle_thr: int = 5000
    scenario_recycled: bool = False
    strict_din: bool = False
    query_mode: bool = False
    environmental_indicator: Optional[str] = None
    lifecycle_indicator: Optional[str] = None


@app.get("/api/v1/health")
def health():
    return {"ok": True}


@app.post("/api/v1/sparql")
def sparql(req: SparqlRequest):
    try:
        return run_query(req.query)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))


@app.post("/api/v1/main-query")
def main_query(req: MainQueryRequest):
    query = build_main_query(
        category=req.category,
        modules=req.modules,
        countries=req.countries,
        subtypes=req.subtypes,
        str_groups=req.str_groups,
        density_groups=req.density_groups,
        din_groups=req.din_groups,
        environ_thr=req.environ_thr,
        lifecycle_thr=req.lifecycle_thr,
        scenario_recycled=req.scenario_recycled,
        strict_din=req.strict_din,
        query_mode=req.query_mode,
        environmental_indicator=req.environmental_indicator,
        lifecycle_indicator=req.lifecycle_indicator,
    )
    try:
        results = run_query(query)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    return {"query": query, "results": results}

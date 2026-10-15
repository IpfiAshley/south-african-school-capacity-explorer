"""Build district and provincial aggregates from the DBE 2025 school masterlist."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).parent
SOURCE = ROOT / "data" / "sa-school-masterlist-q3-2025.xlsx"
APP = ROOT / "app"


def main() -> None:
    df = pd.read_excel(SOURCE, sheet_name="National")
    df = df[(df["Status"] == "OPEN") & (df["Sector"] == "PUBLIC") &
            (df["Type_DoE"] == "ORDINARY SCHOOL")].copy()
    for col in ("Learners2025", "Educators2025", "GIS_Lat", "GIS_Long"):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    # Keep school counts separate from ratios when staffing/enrollment data is missing.
    ratio_df = df[(df["Learners2025"] > 0) & (df["Educators2025"] > 0)].copy()
    ratio_df["learner_educator_ratio"] = ratio_df["Learners2025"] / ratio_df["Educators2025"]
    ratio_df["Quintile"] = ratio_df["Quintile"].astype("string").str.upper()
    ratio_df["Urban_Rural"] = ratio_df["Urban_Rural"].astype("string").str.title()
    ratio_df["Province"] = ratio_df["Province"].replace({
        "EC": "Eastern Cape", "FS": "Free State", "GT": "Gauteng", "GP": "Gauteng", "KZN": "KwaZulu-Natal",
        "LP": "Limpopo", "MP": "Mpumalanga", "NC": "Northern Cape", "NW": "North West", "WC": "Western Cape",
    })
    ratio_df["EIDistrict"] = ratio_df["EIDistrict"].fillna("District not recorded").astype(str).str.title()

    def summarize(keys: list[str]) -> list[dict]:
        result = []
        grouper = keys[0] if len(keys) == 1 else keys
        for key, group in ratio_df.groupby(grouper, dropna=False, sort=True):
            if not isinstance(key, tuple):
                key = (key,)
            learners = float(group["Learners2025"].sum())
            educators = float(group["Educators2025"].sum())
            record = dict(zip(keys, [str(x) for x in key]))
            record.update({
                "schools": int(len(group)),
                "learners": int(learners),
                "educators": int(educators),
                "weighted_ratio": round(learners / educators, 2) if educators else None,
                "median_school_ratio": round(float(group["learner_educator_ratio"].median()), 2),
                "q1_schools": int((group["Quintile"] == "Q1").sum()),
                "q2_schools": int((group["Quintile"] == "Q2").sum()),
                "q3_schools": int((group["Quintile"] == "Q3").sum()),
                "q4_schools": int((group["Quintile"] == "Q4").sum()),
                "q5_schools": int((group["Quintile"] == "Q5").sum()),
                "rural_schools": int((group["Urban_Rural"] == "Rural").sum()),
                "unknown_quintile": int((~group["Quintile"].isin(["Q1", "Q2", "Q3", "Q4", "Q5"])).sum()),
            })
            # District centroid supports an approximate geographic overview without publishing school pins.
            if len(keys) > 1:
                record["longitude"] = round(float(group["GIS_Long"].mean()), 4) if group["GIS_Long"].notna().any() else None
                record["latitude"] = round(float(group["GIS_Lat"].mean()), 4) if group["GIS_Lat"].notna().any() else None
            result.append(record)
        return result

    usable = ratio_df
    by_province = summarize(["Province"])
    by_district = summarize(["Province", "EIDistrict"])
    total_learners = int(usable["Learners2025"].sum())
    total_educators = int(usable["Educators2025"].sum())
    quintiles = []
    for q in ["Q1", "Q2", "Q3", "Q4", "Q5", "Unknown"]:
        g = usable if q == "Unknown" else usable[usable["Quintile"] == q]
        if q == "Unknown":
            g = usable[~usable["Quintile"].isin(["Q1", "Q2", "Q3", "Q4", "Q5"])]
        quintiles.append({"quintile": q, "schools": int(len(g)),
                          "learners": int(g["Learners2025"].sum()),
                          "educators": int(g["Educators2025"].sum()),
                          "weighted_ratio": round(float(g["Learners2025"].sum() / g["Educators2025"].sum()), 2)
                          if g["Educators2025"].sum() else None})
    stats = {
        "title": "South African School Capacity Explorer",
        "source_release": "Department of Basic Education, Quarter 3 2025 Schools Masterlist",
        "scope": "Open public ordinary schools with learner and educator counts greater than zero",
        "coverage": {
            "source_rows": int(len(df)), "usable_ratio_rows": int(len(usable)),
            "missing_or_zero_counts": int(len(df) - len(usable)),
            "coordinate_coverage_pct": round(float(usable[["GIS_Lat", "GIS_Long"]].dropna().shape[0] / len(usable) * 100), 1)
            if len(usable) else 0,
        },
        "totals": {"schools": int(len(usable)), "learners": total_learners, "educators": total_educators,
                   "weighted_ratio": round(total_learners / total_educators, 2) if total_educators else None,
                   "districts": int(ratio_df["EIDistrict"].nunique()), "provinces": int(ratio_df["Province"].nunique())},
        "provinces": by_province,
        "districts": by_district,
        "quintiles": quintiles,
        "sources": [{"name": "DBE EMIS Downloads — Schools Masterlist", "url": "https://www.education.gov.za/Programmes/EMIS/EMISDownloads.aspx"}],
    }
    APP.mkdir(exist_ok=True)
    (APP / "data.json").write_text(json.dumps(stats, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    template = APP / "index.template.html"
    page = APP / "index.html"
    page.write_text(template.read_text(encoding="utf-8").replace(
        "__DASHBOARD_DATA__", json.dumps(stats, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")),
        encoding="utf-8")
    print(f"Prepared South African school summaries: {len(df):,} source schools; {len(usable):,} with usable counts; {len(by_district)} districts.")


if __name__ == "__main__":
    main()

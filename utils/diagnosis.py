from collections import defaultdict

from utils.storage import load_problem_rules


SEVERITY_SCORE = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}


def _normalize_text(value):
    return str(value or "").strip().lower()


def diagnose_plant(symptoms, plant_type=None):
    selected = {_normalize_text(symptom) for symptom in symptoms if _normalize_text(symptom)}
    if not selected:
        return []

    rules = load_problem_rules().copy()
    if rules.empty:
        return []

    rules["symptom"] = rules["symptom"].astype(str).str.strip().str.lower()
    rules["problem"] = rules["problem"].astype(str).str.strip()
    rules["recommendation"] = rules["recommendation"].astype(str).str.strip()
    rules["plant_type"] = rules["plant_type"].fillna("").astype(str).str.strip().str.lower()
    rules["severity"] = rules["severity"].fillna("low").astype(str).str.strip().str.lower()

    plant_type = _normalize_text(plant_type)
    if plant_type:
        filtered = rules[(rules["plant_type"] == "") | (rules["plant_type"] == plant_type)]
    else:
        filtered = rules

    matched = filtered[filtered["symptom"].isin(selected)].copy()
    if matched.empty:
        return []

    grouped = defaultdict(lambda: {
        "problem": "",
        "recommendation": "",
        "severity": "low",
        "match_count": 0,
        "matched_symptoms": [],
    })

    for _, row in matched.iterrows():
        key = (row["problem"], row["recommendation"])
        bucket = grouped[key]
        bucket["problem"] = row["problem"]
        bucket["recommendation"] = row["recommendation"]
        bucket["severity"] = max(bucket["severity"], row["severity"], key=lambda s: SEVERITY_SCORE.get(s, 0))
        bucket["match_count"] += 1
        bucket["matched_symptoms"].append(row["symptom"])

    results = list(grouped.values())
    results.sort(
        key=lambda item: (
            item["match_count"],
            SEVERITY_SCORE.get(item["severity"], 0),
            item["problem"],
        ),
        reverse=True,
    )
    return results

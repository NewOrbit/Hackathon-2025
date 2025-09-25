from __future__ import annotations

import os
from typing import Any, Dict, List, Optional, Tuple

import requests

from utils import clamp_non_negative, round2


class NutritionSource:
    NUTRITIONIX = "nutritionix"
    EDAMAM = "edamam"
    OPENFOODFACTS = "openfoodfacts"


def _nutritionix_available() -> bool:
    return bool(os.getenv("NUTRITIONIX_APP_ID") and os.getenv("NUTRITIONIX_API_KEY"))


def _edamam_available() -> bool:
    return bool(os.getenv("EDAMAM_APP_ID") and os.getenv("EDAMAM_APP_KEY"))


def _call_nutritionix_nlp(query: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        "x-app-id": os.getenv("NUTRITIONIX_APP_ID", ""),
        "x-app-key": os.getenv("NUTRITIONIX_API_KEY", ""),
        "Content-Type": "application/json",
    }
    try:
        resp = requests.post(url, json={"query": query}, headers=headers, timeout=15)
        if resp.status_code == 200:
            return resp.json(), None
        return None, f"nutritionix_error:{resp.status_code}"
    except Exception as ex:  # noqa: BLE001
        return None, f"nutritionix_exception:{ex}"


def _call_edamam_nlp(query: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    # Edamam Nutrition Analysis v2 - natural language endpoint
    # https://developer.edamam.com/edamam-nutrition-api
    app_id = os.getenv("EDAMAM_APP_ID", "")
    app_key = os.getenv("EDAMAM_APP_KEY", "")
    url = f"https://api.edamam.com/api/nutrition-data?app_id={app_id}&app_key={app_key}&nutrition-type=logging&ingr={requests.utils.quote(query)}"
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            return resp.json(), None
        return None, f"edamam_error:{resp.status_code}"
    except Exception as ex:  # noqa: BLE001
        return None, f"edamam_exception:{ex}"


def _call_openfoodfacts_search(query: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    # Simple search - best effort, good for branded items
    url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {"search_terms": query, "search_simple": 1, "json": 1, "page_size": 1}
    try:
        resp = requests.get(url, params=params, timeout=15)
        if resp.status_code == 200:
            return resp.json(), None
        return None, f"openfoodfacts_error:{resp.status_code}"
    except Exception as ex:  # noqa: BLE001
        return None, f"openfoodfacts_exception:{ex}"


def _normalize_nutritionix(payload: Dict[str, Any]) -> Dict[str, Any]:
    foods = payload.get("foods", [])
    items: List[Dict[str, Any]] = []
    total = {"calories": 0.0, "protein_g": 0.0, "carbs_g": 0.0, "fat_g": 0.0}
    for f in foods:
        item = {
            "name": f.get("food_name"),
            "serving_qty": f.get("serving_qty"),
            "serving_unit": f.get("serving_unit"),
            "calories": round2(f.get("nf_calories", 0.0)),
            "protein_g": round2(f.get("nf_protein", 0.0)),
            "carbs_g": round2(f.get("nf_total_carbohydrate", 0.0)),
            "fat_g": round2(f.get("nf_total_fat", 0.0)),
        }
        items.append(item)
        total["calories"] += item["calories"]
        total["protein_g"] += item["protein_g"]
        total["carbs_g"] += item["carbs_g"]
        total["fat_g"] += item["fat_g"]

    for k in total:
        total[k] = round2(total[k])

    return {
        "source": NutritionSource.NUTRITIONIX,
        "confidence": 0.9 if items else 0.3,
        "items": items,
        "total": total,
    }


def _normalize_edamam(payload: Dict[str, Any], query: str) -> Dict[str, Any]:
    # Edamam nutrition-data returns totals for the full text
    total = {
        "calories": round2(payload.get("calories", 0.0)),
        "protein_g": round2(payload.get("totalNutrients", {}).get("PROCNT", {}).get("quantity", 0.0)),
        "carbs_g": round2(payload.get("totalNutrients", {}).get("CHOCDF", {}).get("quantity", 0.0)),
        "fat_g": round2(payload.get("totalNutrients", {}).get("FAT", {}).get("quantity", 0.0)),
    }
    return {
        "source": NutritionSource.EDAMAM,
        "confidence": 0.7,
        "items": [{"name": query, **total}],
        "total": total,
    }


def _normalize_openfoodfacts(payload: Dict[str, Any]) -> Dict[str, Any]:
    products = payload.get("products", [])
    if not products:
        return {"source": NutritionSource.OPENFOODFACTS, "confidence": 0.2, "items": [], "total": {}}
    p = products[0]
    nutr = p.get("nutriments", {})
    per100kcal = {
        "calories": round2(nutr.get("energy-kcal_100g", 0.0)),
        "protein_g": round2(nutr.get("proteins_100g", 0.0)),
        "carbs_g": round2(nutr.get("carbohydrates_100g", 0.0)),
        "fat_g": round2(nutr.get("fat_100g", 0.0)),
    }
    return {
        "source": NutritionSource.OPENFOODFACTS,
        "confidence": 0.5,
        "items": [{"name": p.get("product_name", "product"), **per100kcal, "basis": "per_100g"}],
        "total": per100kcal,
    }


def estimate_macros_from_description(description: str) -> Dict[str, Any]:
    description = description.strip()
    tried: List[str] = []

    if _nutritionix_available():
        data, err = _call_nutritionix_nlp(description)
        tried.append(NutritionSource.NUTRITIONIX)
        if data:
            return _normalize_nutritionix(data)

    if _edamam_available():
        data, err = _call_edamam_nlp(description)
        tried.append(NutritionSource.EDAMAM)
        if data:
            return _normalize_edamam(data, description)

    data, err = _call_openfoodfacts_search(description)
    tried.append(NutritionSource.OPENFOODFACTS)
    if data:
        return _normalize_openfoodfacts(data)

    return {
        "source": "none",
        "confidence": 0.0,
        "items": [],
        "total": {},
        "error": "No data sources available or reachable",
        "tried": tried,
    }


def estimate_macros_from_ingredients(ingredients: List[str]) -> Dict[str, Any]:
    if not ingredients:
        return {"source": "none", "confidence": 0.0, "items": [], "total": {}}
    combined = ", ".join(ingredients)
    return estimate_macros_from_description(combined)


def build_formatted_resource(query: str, data: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append(f"Food: {query}")
    lines.append(f"Source: {data.get('source')}  |  Confidence: {data.get('confidence')}")

    total = data.get("total", {})
    if total:
        lines.append("Total (approx):")
        lines.append(
            f"  Calories: {total.get('calories', 0)} kcal | Protein: {total.get('protein_g', 0)} g | Carbs: {total.get('carbs_g', 0)} g | Fat: {total.get('fat_g', 0)} g"
        )
    items = data.get("items", [])
    if items:
        lines.append("Items:")
        for it in items:
            name = it.get("name", "item")
            extra = []
            if it.get("serving_qty"):
                extra.append(f"{it.get('serving_qty')} {it.get('serving_unit')}")
            if it.get("basis"):
                extra.append(f"basis: {it.get('basis')}")
            suffix = f" ({', '.join(extra)})" if extra else ""
            lines.append(
                f"  - {name}{suffix}: {it.get('calories', 0)} kcal, P {it.get('protein_g', 0)} g, C {it.get('carbs_g', 0)} g, F {it.get('fat_g', 0)} g"
            )
    if data.get("error"):
        lines.append(f"Error: {data.get('error')}")
    if data.get("tried"):
        lines.append(f"Tried sources: {', '.join(data['tried'])}")
    return "\n".join(lines)



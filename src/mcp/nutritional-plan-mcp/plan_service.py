from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class UserProfile:
    sex: str  # "male" | "female"
    age_years: int
    height_cm: float
    weight_kg: float
    activity_level: str  # sedentary, lightly_active, moderately_active, very_active, extra_active
    goal: str  # lose_weight, maintain, gain_muscle
    weekly_rate: Optional[float] = None  # kg per week (positive for gain, positive for loss target)


def calculate_bmr_mifflin(profile: UserProfile) -> float:
    # Mifflin-St Jeor
    s = 5 if profile.sex.lower() == "male" else -161
    return 10 * profile.weight_kg + 6.25 * profile.height_cm - 5 * profile.age_years + s


def activity_multiplier(level: str) -> float:
    mapping = {
        "sedentary": 1.2,
        "lightly_active": 1.375,
        "moderately_active": 1.55,
        "very_active": 1.725,
        "extra_active": 1.9,
    }
    return mapping.get(level.lower(), 1.2)


def protein_target_grams(profile: UserProfile) -> float:
    # Simple heuristic: vary by goal/activity
    if profile.goal == "gain_muscle":
        grams_per_kg = 1.8
    elif profile.goal == "lose_weight":
        grams_per_kg = 1.6
    else:
        grams_per_kg = 1.4
    return round(profile.weight_kg * grams_per_kg, 1)


def fat_target_grams(total_calories: int, profile: UserProfile) -> float:
    # 25-35% calories from fat depending on goal
    if profile.goal == "gain_muscle":
        pct = 0.25
    elif profile.goal == "lose_weight":
        pct = 0.30
    else:
        pct = 0.30
    return round((total_calories * pct) / 9.0, 1)


def carbs_from_remaining(total_calories: int, protein_g: float, fat_g: float) -> float:
    calories_from_protein = protein_g * 4
    calories_from_fat = fat_g * 9
    remaining = max(0.0, total_calories - calories_from_protein - calories_from_fat)
    return round(remaining / 4.0, 1)


def plan_calories(profile: UserProfile) -> Dict:
    bmr = calculate_bmr_mifflin(profile)
    tdee = bmr * activity_multiplier(profile.activity_level)

    # energy balance: 7700 kcal ~ 1 kg
    target_delta = 0.0
    if profile.goal == "lose_weight":
        weekly = profile.weekly_rate or 0.4  # kg/week default
        target_delta = - (weekly * 7700) / 7.0
    elif profile.goal == "gain_muscle":
        weekly = profile.weekly_rate or 0.25
        target_delta = (weekly * 7700) / 7.0

    target_cals = int(round(tdee + target_delta))
    min_safe = int(round(bmr * 1.1))  # avoid too low
    target_cals = max(target_cals, min_safe)

    protein_g = protein_target_grams(profile)
    fat_g = fat_target_grams(target_cals, profile)
    carbs_g = carbs_from_remaining(target_cals, protein_g, fat_g)

    return {
        "bmr": int(round(bmr)),
        "tdee": int(round(tdee)),
        "target_calories": target_cals,
        "macros": {
            "protein_g": protein_g,
            "carbs_g": carbs_g,
            "fat_g": fat_g,
        },
        "assumptions": {
            "formula": "Mifflin-St Jeor",
            "weekly_rate_kg": profile.weekly_rate or (0.4 if profile.goal == "lose_weight" else 0.25 if profile.goal == "gain_muscle" else 0.0),
            "activity_multiplier": activity_multiplier(profile.activity_level),
            "kcal_per_kg": 7700,
        }
    }


def build_text_plan(profile: UserProfile, data: Dict) -> str:
    lines = []
    lines.append("Nutrition Plan")
    lines.append(f"Sex: {profile.sex}, Age: {profile.age_years}, Height: {profile.height_cm} cm, Weight: {profile.weight_kg} kg")
    lines.append(f"Activity: {profile.activity_level}, Goal: {profile.goal}")
    lines.append("")
    lines.append(f"BMR: {data['bmr']} kcal | TDEE: {data['tdee']} kcal")
    lines.append(f"Daily target: {data['target_calories']} kcal")
    m = data["macros"]
    lines.append(f"Macros (approx): Protein {m['protein_g']} g, Carbs {m['carbs_g']} g, Fat {m['fat_g']} g")
    lines.append("")
    lines.append("Assumptions:")
    a = data["assumptions"]
    lines.append(f"  - Formula: {a['formula']}")
    lines.append(f"  - Weekly rate: {a['weekly_rate_kg']} kg/week")
    lines.append(f"  - Activity multiplier: {a['activity_multiplier']}")
    lines.append(f"  - Energy per kg: {a['kcal_per_kg']} kcal")
    lines.append("")
    lines.append("Guidance:")
    lines.append("  - Spread protein across 3–4 meals.")
    lines.append("  - Emphasize whole foods, fiber, and hydration.")
    lines.append("  - Reassess every 2–4 weeks and adjust based on progress.")
    return "\n".join(lines)



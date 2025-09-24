import { type Totals } from "./types";

export function extractTargetsFromPlan(plan: string): Totals | null {
  if (!plan) return null;
  let calories = 0;
  let protein = 0;
  let carbs = 0;
  let fat = 0;

  const calorieMatch = plan.match(
    /\b(?:calories|calorie target)\b[^\d]*(\d+(?:\.\d+)?)/i
  );
  if (calorieMatch) {
    calories = Number.parseFloat(calorieMatch[1]);
  }

  for (const match of plan.matchAll(
    /(protein|carbs?|fat)\s*:?\s*(\d+(?:\.\d+)?)\s*g/gi
  )) {
    const key = match[1].toLowerCase();
    const value = Number.parseFloat(match[2]);
    if (key.startsWith("protein")) protein = value;
    if (key.startsWith("carb")) carbs = value;
    if (key.startsWith("fat")) fat = value;
  }

  if (!calories && !protein && !carbs && !fat) {
    return null;
  }

  return {
    calories,
    protein_g: protein,
    carbs_g: carbs,
    fat_g: fat,
  };
}

export function calculateRemaining(
  target: Totals | null,
  consumed: Totals
): Totals | null {
  if (!target) return null;
  return {
    calories: target.calories - consumed.calories,
    protein_g: target.protein_g - consumed.protein_g,
    carbs_g: target.carbs_g - consumed.carbs_g,
    fat_g: target.fat_g - consumed.fat_g,
  };
}

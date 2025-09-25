import { type Totals, type PlanData } from "./types";

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

export function parsePlanResponse(output: string): {
  summary: string;
  data: PlanData;
} {
  const delimiter = "```json";
  const start = output.indexOf(delimiter);
  if (start === -1) {
    throw new Error("Plan response missing JSON section");
  }
  const summary = output.slice(0, start).trim();
  const jsonPart = output.slice(start + delimiter.length);
  const closingIndex = jsonPart.indexOf("```", 0);
  const jsonString = (
    closingIndex === -1 ? jsonPart : jsonPart.slice(0, closingIndex)
  ).trim();
  const parsed = JSON.parse(jsonString);
  if (!parsed?.targets) {
    throw new Error("Plan response JSON missing targets");
  }
  return {
    summary,
    data: parsed,
  };
}

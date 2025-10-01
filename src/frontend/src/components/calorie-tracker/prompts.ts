import { type FormState, type Totals } from "./types";

export function buildPlanPrompt(form: FormState) {
  return `You are an AI nutrition coach. Use the nutritional_plan compose_plan tool to calculate daily calories and macronutrients for this user.
  
  User profile:
  - Name: ${form.name || "N/A"}
  - Sex: ${form.sex}
  - Age: ${form.ageYears}
  - Height: ${form.heightCm} cm
  - Weight: ${form.weightKg} kg
  - Activity level: ${form.activityLevel}
  - Goal: ${form.goal}
  - Weekly rate target (kg/week): ${form.weeklyRate || "0"}
  - Dietary notes: ${form.dietaryNotes || "none"}
  
  Return your answer in the following exact format:
  
  ### Daily Nutrition Plan
  (Provide 2–3 short paragraphs summarising the plan and highlighting key advice. Use the nutrition_plan compose_plan tool to generate the plan.)
  
  #### Daily Targets
  - Calories: <number> kcal
  - Protein: <number> g
  - Carbs: <number> g
  - Fat: <number> g
  
  #### Macro Split
  - Protein: <number>%
  - Carbs: <number>%
  - Fat: <number>%
  
  #### Guidance
  - Bullet point 1
  - Bullet point 2
  - Bullet point 3
  
  \`\`\`json
  {
    "targets": {
      "calories": <number>,
      "protein_g": <number>,
      "carbs_g": <number>,
      "fat_g": <number>
    },
    "macro_percentages": {
      "protein": <number>,
      "carbs": <number>,
      "fat": <number>
    },
    "guidance": ["string", "string", "string"]
  }
  \`\`\`
  
  Rules:
  - Use plain digits without thousands separators in the JSON values (e.g. 2050, not 2,050).
  - Ensure the JSON block is valid parseable JSON and matches the schema exactly.
  - Do not add any other text after the closing \`\`\` fence.`;
}

export function buildMealPrompt(
  mealDescription: string,
  totals: Totals,
  planSummary: string
) {
  return `We already created the following nutrition plan:
${planSummary}

Current running totals (kcal, protein_g, carbs_g, fat_g): ${JSON.stringify(
    totals
  )}

The user just consumed:
"""${mealDescription}"""

Use the macros analyze_macros/analyze_recipe tools to estimate this meal.
Return JSON ONLY using this schema (no code fences):
{
  "meal": string,
  "estimates": {"calories": number, "protein_g": number, "carbs_g": number, "fat_g": number},
  "running_totals": {"calories": number, "protein_g": number, "carbs_g": number, "fat_g": number},
  "notes": string
}
Round numbers to 1 decimal place.`;
}

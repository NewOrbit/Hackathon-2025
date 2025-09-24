export type SexOption = "male" | "female" | "nonbinary" | "";
export type GoalValue = "lose_weight" | "maintain" | "gain_muscle" | "";

export type FormState = {
  name: string;
  sex: SexOption;
  ageYears: string;
  heightCm: string;
  weightKg: string;
  activityLevel: string;
  goal: GoalValue;
  weeklyRate: string;
  dietaryNotes: string;
};

export type Totals = {
  calories: number;
  protein_g: number;
  carbs_g: number;
  fat_g: number;
};

export type PlanData = {
  targets: Totals;
  guidance?: string[];
  macroPercentages?: {
    protein?: number;
    carbs?: number;
    fat?: number;
  };
};

export type MealEntry = {
  meal: string;
  response: string;
  estimates?: Totals;
  runningTotals?: Totals;
  notes?: string;
  parseError?: boolean;
  timestamp: string;
};

export type ActivityLevelOption = {
  value: string;
  label: string;
};

export type GoalOption = {
  value: Exclude<GoalValue, "">;
  label: string;
  defaultRate: string;
  helper: string;
};

export const steps = [
  "Basic info",
  "Measurements",
  "Lifestyle & goal",
] as const;

export const activityLevels: ActivityLevelOption[] = [
  { value: "sedentary", label: "Sedentary – little or no exercise" },
  { value: "lightly_active", label: "Lightly active – 1-3 days exercise" },
  { value: "moderately_active", label: "Moderately active – 3-5 days" },
  { value: "very_active", label: "Very active – 6-7 days" },
  { value: "extra_active", label: "Extra active – physical job or training" },
];

export const goalOptions: GoalOption[] = [
  {
    value: "lose_weight",
    label: "Lose weight",
    defaultRate: "0.4",
    helper: "Typical 0.25–0.7 kg per week",
  },
  {
    value: "maintain",
    label: "Maintain weight",
    defaultRate: "0",
    helper: "Stay around current weight",
  },
  {
    value: "gain_muscle",
    label: "Gain muscle",
    defaultRate: "0.25",
    helper: "Typical 0.1–0.4 kg per week",
  },
];

export const initialFormState: FormState = {
  name: "",
  sex: "",
  ageYears: "",
  heightCm: "",
  weightKg: "",
  activityLevel: "",
  goal: "",
  weeklyRate: "",
  dietaryNotes: "",
};

export const initialTotals: Totals = {
  calories: 0,
  protein_g: 0,
  carbs_g: 0,
  fat_g: 0,
};

export function isStepValid(form: FormState, stepIndex: number): boolean {
  if (stepIndex === 0) {
    return Boolean(form.sex && Number(form.ageYears) > 0);
  }
  if (stepIndex === 1) {
    return Number(form.heightCm) > 0 && Number(form.weightKg) > 0;
  }
  if (stepIndex === 2) {
    if (!form.activityLevel || !form.goal) {
      return false;
    }
    if (form.goal !== "maintain") {
      return form.weeklyRate === "" || !Number.isNaN(Number(form.weeklyRate));
    }
    return true;
  }
  return true;
}

export function subtractTotals(target: Totals, consumed: Totals): Totals {
  return {
    calories: target.calories - consumed.calories,
    protein_g: target.protein_g - consumed.protein_g,
    carbs_g: target.carbs_g - consumed.carbs_g,
    fat_g: target.fat_g - consumed.fat_g,
  };
}

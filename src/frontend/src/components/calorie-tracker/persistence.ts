import {
  type FormState,
  type MealEntry,
  type Totals,
  type PlanData,
  initialFormState,
  initialTotals,
} from "./types";

const STORAGE_KEY = "ai-calorie-tracker-state";

export type PersistedTrackerState = {
  form: FormState;
  planSummary: string;
  planData: PlanData | null;
  totals: Totals;
  entries: MealEntry[];
  activeStep: number;
};

export function loadPersistedState(): PersistedTrackerState | null {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw);
    if (!parsed || typeof parsed !== "object") return null;
    return {
      form: parsed.form ?? initialFormState,
      planSummary: parsed.planSummary ?? "",
      planData: parsed.planData ?? null,
      totals: parsed.totals ?? initialTotals,
      entries: Array.isArray(parsed.entries) ? parsed.entries : [],
      activeStep: typeof parsed.activeStep === "number" ? parsed.activeStep : 0,
    } satisfies PersistedTrackerState;
  } catch (error) {
    console.warn("Failed to load persisted tracker state", error);
    return null;
  }
}

export function savePersistedState(state: PersistedTrackerState) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  } catch (error) {
    console.warn("Failed to persist tracker state", error);
  }
}

export function clearPersistedState() {
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch (error) {
    console.warn("Failed to clear tracker state", error);
  }
}

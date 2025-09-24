import { useEffect, useMemo, useState } from "react";
import {
  Box,
  Button,
  Paper,
  Stack,
  Step,
  StepLabel,
  Stepper,
  Typography,
} from "@mui/material";

import { initSession, sendMessage } from "../api/api";
import {
  FormState,
  MealEntry,
  Totals,
  initialFormState,
  initialTotals,
  isStepValid,
  steps,
  goalOptions,
} from "./calorie-tracker";
import { FormStep } from "./calorie-tracker/formStep";
import { PlanCard } from "./calorie-tracker/PlanCard";
import { MealLogger } from "./calorie-tracker/MealLogger";

function buildPlanPrompt(form: FormState) {
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

Return the response as clear Markdown with these sections:
1. Daily Targets (calories and macros)
2. Macro Split (percentages and gram targets)
3. Guidance (3 short bullet points)
Finish with a one-line invitation for the user to log their first meal.`;
}

function buildMealPrompt(
  mealDescription: string,
  totals: Totals,
  planMarkdown: string
) {
  return `We already created the following nutrition plan:
${planMarkdown}

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

export default function CalorieTracker() {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [activeStep, setActiveStep] = useState(0);
  const [form, setForm] = useState<FormState>(initialFormState);
  const [plan, setPlan] = useState<string>("");
  const [planError, setPlanError] = useState<string | null>(null);
  const [planLoading, setPlanLoading] = useState(false);
  const [mealInput, setMealInput] = useState("");
  const [mealLoading, setMealLoading] = useState(false);
  const [mealError, setMealError] = useState<string | null>(null);
  const [entries, setEntries] = useState<MealEntry[]>([]);
  const [totals, setTotals] = useState<Totals>(initialTotals);

  useEffect(() => {
    (async () => {
      try {
        const init = await initSession();
        setSessionId(init.sessionId);
      } catch (error) {
        console.error("Failed to init session", error);
      }
    })();
  }, []);

  useEffect(() => {
    if (!form.goal) return;
    const goalConfig = goalOptions.find((g) => g.value === form.goal);
    if (!goalConfig) return;
    if (form.weeklyRate.trim() === "" || form.weeklyRate === "0") {
      setForm((prev) => ({ ...prev, weeklyRate: goalConfig.defaultRate }));
    }
  }, [form.goal]);

  const stepValid = useMemo(
    () => isStepValid(form, activeStep),
    [form, activeStep]
  );

  const handleNext = async () => {
    if (activeStep < steps.length - 1) {
      setActiveStep((prev) => prev + 1);
      return;
    }
    await generatePlan();
  };

  const generatePlan = async () => {
    if (!sessionId) return;
    setPlanLoading(true);
    setPlanError(null);
    try {
      const prompt = buildPlanPrompt(form);
      const res = await sendMessage(sessionId, prompt);
      setPlan(res.output.trim());
      setActiveStep(steps.length);
    } catch (error: any) {
      console.error(error);
      setPlanError(error?.message || "Failed to generate plan");
    } finally {
      setPlanLoading(false);
    }
  };

  const handleLogMeal = async () => {
    if (!sessionId || !mealInput.trim() || !plan) return;
    setMealLoading(true);
    setMealError(null);
    const mealText = mealInput.trim();
    setMealInput("");
    try {
      const prompt = buildMealPrompt(mealText, totals, plan);
      const res = await sendMessage(sessionId, prompt);
      const raw = res.output.trim();
      let estimates: Totals | undefined;
      let runningTotals: Totals | undefined;
      let notes: string | undefined;
      let parseError = false;
      try {
        const parsed = JSON.parse(raw);
        estimates = parsed.estimates;
        runningTotals = parsed.running_totals;
        notes = parsed.notes;
        if (runningTotals && typeof runningTotals.calories === "number") {
          setTotals(runningTotals);
        }
      } catch (jsonError) {
        parseError = true;
        console.warn("Failed to parse meal response as JSON", jsonError, raw);
      }

      setEntries((prev) => [
        {
          meal: mealText,
          response: raw,
          estimates,
          runningTotals,
          notes,
          parseError,
          timestamp: new Date().toISOString(),
        },
        ...prev,
      ]);
    } catch (error: any) {
      console.error(error);
      setMealError(error?.message || "Failed to log meal");
    } finally {
      setMealLoading(false);
    }
  };

  return (
    <Stack spacing={3} sx={{ width: "min(960px, 100%)", mx: "auto", py: 4 }}>
      <Typography variant="h4" fontWeight={700} textAlign="center">
        AI Calorie Tracker
      </Typography>
      <Typography textAlign="center" color="text.secondary">
        Share a few details, review your personalised plan, then log meals in
        natural language to keep tabs on calories and macros.
      </Typography>

      <Paper variant="outlined" sx={{ p: 3 }}>
        <Stepper
          activeStep={Math.min(activeStep, steps.length)}
          alternativeLabel
        >
          {steps.map((label) => (
            <Step key={label}>
              <StepLabel>{label}</StepLabel>
            </Step>
          ))}
        </Stepper>

        {activeStep < steps.length && (
          <Box sx={{ mt: 3 }}>
            <FormStep
              stepIndex={activeStep}
              form={form}
              onChange={(fields) => setForm((prev) => ({ ...prev, ...fields }))}
            />
            <Stack
              direction="row"
              spacing={1}
              sx={{ mt: 3 }}
              justifyContent="flex-end"
            >
              {activeStep > 0 && (
                <Button
                  onClick={() => setActiveStep((prev) => prev - 1)}
                  disabled={planLoading}
                >
                  Back
                </Button>
              )}
              <Button
                variant="contained"
                onClick={handleNext}
                disabled={!stepValid || planLoading || !sessionId}
              >
                {activeStep === steps.length - 1 ? "Generate plan" : "Next"}
              </Button>
            </Stack>
            {planError && (
              <Paper variant="outlined" sx={{ mt: 2, p: 2 }}>
                <Typography color="error">{planError}</Typography>
              </Paper>
            )}
          </Box>
        )}

        {activeStep >= steps.length && (
          <PlanCard
            plan={plan}
            loading={planLoading}
            error={planError}
            onBackToEdit={() => setActiveStep(steps.length - 1)}
            onReset={() => {
              setPlan("");
              setTotals(initialTotals);
              setEntries([]);
              setMealInput("");
              setForm(initialFormState);
              setActiveStep(0);
            }}
          />
        )}
      </Paper>

      {plan && (
        <MealLogger
          plan={plan}
          totals={totals}
          entries={entries}
          mealInput={mealInput}
          onInputChange={setMealInput}
          onLogMeal={handleLogMeal}
          loading={mealLoading}
          error={mealError}
        />
      )}
    </Stack>
  );
}

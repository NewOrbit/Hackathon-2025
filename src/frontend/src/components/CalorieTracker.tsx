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
  type FormState,
  type MealEntry,
  type Totals,
  type PlanData,
  initialFormState,
  initialTotals,
  isStepValid,
  steps,
  goalOptions,
  calculateRemaining,
  parsePlanResponse,
  loadPersistedState,
  savePersistedState,
  clearPersistedState,
  buildPlanPrompt,
  buildMealPrompt,
} from "./calorie-tracker";
import { FormStep } from "./calorie-tracker/formStep";
import { PlanCard } from "./calorie-tracker/PlanCard";
import { MealLogger } from "./calorie-tracker/MealLogger";
import MealLogContext from "./calorie-tracker/MealLogContext";
import ChatWidget from "./ChatWidget";

export default function CalorieTracker() {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [activeStep, setActiveStep] = useState(0);
  const [form, setForm] = useState<FormState>(initialFormState);
  const [planSummary, setPlanSummary] = useState<string>("");
  const [planData, setPlanData] = useState<PlanData | null>(null);
  const [planError, setPlanError] = useState<string | null>(null);
  const [planLoading, setPlanLoading] = useState(false);
  const [mealInput, setMealInput] = useState("");
  const [mealLoading, setMealLoading] = useState(false);
  const [mealError, setMealError] = useState<string | null>(null);
  const [entries, setEntries] = useState<MealEntry[]>([]);
  const [totals, setTotals] = useState<Totals>(initialTotals);
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    const persisted = loadPersistedState();
    if (persisted) {
      setForm(persisted.form);
      setPlanSummary(persisted.planSummary);
      setPlanData(persisted.planData);
      setTotals(persisted.totals);
      setEntries(persisted.entries);
      setActiveStep(persisted.activeStep);
    }
    setHydrated(true);
  }, []);

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
    if (!hydrated) return;
    if (!form.goal) return;
    const goalConfig = goalOptions.find((g) => g.value === form.goal);
    if (!goalConfig) return;
    if (form.weeklyRate.trim() === "" || form.weeklyRate === "0") {
      setForm((prev) => ({ ...prev, weeklyRate: goalConfig.defaultRate }));
    }
  }, [form.goal, form.weeklyRate, hydrated]);

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
    setPlanData(null);
    setPlanSummary("");
    try {
      const prompt = buildPlanPrompt(form);
      const res = await sendMessage(sessionId, prompt);
      const { summary, data } = parsePlanResponse(res.output);
      setPlanSummary(summary);
      setPlanData(data);
      setTotals(initialTotals);
      setEntries([]);
      setActiveStep(steps.length);
    } catch (error: any) {
      console.error(error);
      setPlanError(error?.message || "Failed to generate plan");
    } finally {
      setPlanLoading(false);
    }
  };

  const handleLogMealFromText = async (
    description: string,
    fromChat = false
  ) => {
    if (!sessionId || !planSummary) {
      return {
        success: false,
        message: "Meal logging is not ready yet.",
      };
    }
    const mealText = description.trim();
    if (!mealText) {
      return { success: false, message: "Please provide a meal description." };
    }

    if (!fromChat) {
      setMealLoading(true);
      setMealError(null);
    }

    try {
      const prompt = buildMealPrompt(mealText, totals, planSummary);
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
      } catch (error) {
        parseError = true;
        console.warn("Failed to parse meal response as JSON", error, raw);
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

      return {
        success: true,
        message: parseError
          ? "Logged meal, but could not parse structured data."
          : "Meal logged successfully.",
        parseError,
      };
    } catch (error: any) {
      console.error(error);
      return {
        success: false,
        message: error?.message ?? "Failed to log meal.",
      };
    } finally {
      if (!fromChat) {
        setMealLoading(false);
      }
    }
  };

  const handleLogMeal = async () => {
    if (!mealInput.trim()) return;
    const result = await handleLogMealFromText(mealInput, false);
    if (result.success) {
      setMealInput("");
    } else {
      setMealError(result.message ?? "Failed to log meal");
    }
  };

  const remaining = useMemo(
    () => calculateRemaining(planData?.targets ?? null, totals),
    [planData, totals]
  );

  useEffect(() => {
    if (!hydrated) return;
    savePersistedState({
      form,
      planSummary,
      planData,
      totals,
      entries,
      activeStep,
    });
  }, [form, planSummary, planData, totals, entries, activeStep, hydrated]);

  return (
    <MealLogContext.Provider
      value={{
        logMealFromText: (text) => handleLogMealFromText(text, true),
        canLogMeal: Boolean(sessionId && planSummary),
      }}
    >
      <Stack spacing={3} sx={{ width: "min(960px, 100%)", mx: "auto", py: 4 }}>
        <Typography variant="h4" fontWeight={700} textAlign="center">
          m<span style={{ color: "#1976d2", fontWeight: 800 }}>ai</span>tre d'
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
                onChange={(fields) =>
                  setForm((prev) => ({ ...prev, ...fields }))
                }
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
              plan={planSummary}
              loading={planLoading}
              error={planError}
              onBackToEdit={() => setActiveStep(steps.length - 1)}
              onReset={() => {
                setPlanSummary("");
                setPlanData(null);
                setTotals(initialTotals);
                setEntries([]);
                setMealInput("");
                setForm(initialFormState);
                setActiveStep(0);
                clearPersistedState();
              }}
            />
          )}
        </Paper>

        {planSummary && (
          <MealLogger
            planSummary={planSummary}
            totals={totals}
            entries={entries}
            mealInput={mealInput}
            onInputChange={setMealInput}
            onLogMeal={handleLogMeal}
            loading={mealLoading}
            error={mealError}
            remaining={remaining}
          />
        )}
      </Stack>
      <ChatWidget />
    </MealLogContext.Provider>
  );
}

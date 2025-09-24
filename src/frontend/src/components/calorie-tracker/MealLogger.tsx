import {
  Alert,
  Button,
  Paper,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import { Totals, MealEntry } from "./types";

type MealLoggerProps = {
  plan: string;
  totals: Totals;
  entries: MealEntry[];
  mealInput: string;
  onInputChange: (value: string) => void;
  onLogMeal: () => void;
  loading: boolean;
  error: string | null;
};

export function MealLogger({
  plan,
  totals,
  entries,
  mealInput,
  onInputChange,
  onLogMeal,
  loading,
  error,
}: MealLoggerProps) {
  return (
    <Paper variant="outlined" sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        Log a meal
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        Describe what you ate in plain language. The AI will estimate calories
        and macros using the food MCP and keep track of totals.
      </Typography>
      <Stack
        direction={{ xs: "column", sm: "row" }}
        spacing={1}
        alignItems={{ xs: "stretch", sm: "flex-start" }}
      >
        <TextField
          fullWidth
          multiline
          minRows={2}
          placeholder="e.g. grilled chicken salad with quinoa and avocado"
          value={mealInput}
          onChange={(e) => onInputChange(e.target.value)}
          disabled={!plan}
        />
        <Button
          variant="contained"
          onClick={onLogMeal}
          disabled={loading || !mealInput.trim() || !plan}
          sx={{ minWidth: 160 }}
        >
          {loading ? "Tracking…" : "Add meal"}
        </Button>
      </Stack>
      {error && (
        <Alert sx={{ mt: 2 }} severity="error">
          {error}
        </Alert>
      )}

      <Stack spacing={2} sx={{ mt: 3 }}>
        <Typography variant="subtitle1">Running totals</Typography>
        <Typography color="text.secondary">
          Calories: {totals.calories.toFixed(1)} kcal · Protein:{" "}
          {totals.protein_g.toFixed(1)} g · Carbs: {totals.carbs_g.toFixed(1)} g
          · Fat: {totals.fat_g.toFixed(1)} g
        </Typography>
      </Stack>

      <Stack spacing={2} sx={{ mt: 3 }}>
        {entries.length === 0 && (
          <Typography color="text.secondary">No meals logged yet.</Typography>
        )}
        {entries.map((entry) => (
          <Paper key={entry.timestamp} variant="outlined" sx={{ p: 2 }}>
            <Typography fontWeight={600}>{entry.meal}</Typography>
            {entry.estimates && entry.runningTotals && !entry.parseError ? (
              <Stack spacing={1} sx={{ mt: 1 }}>
                <Typography variant="body2">
                  Estimated: {entry.estimates.calories.toFixed(1)} kcal ·
                  Protein {entry.estimates.protein_g.toFixed(1)} g · Carbs{" "}
                  {entry.estimates.carbs_g.toFixed(1)} g · Fat{" "}
                  {entry.estimates.fat_g.toFixed(1)} g
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  New totals: {entry.runningTotals.calories.toFixed(1)} kcal ·
                  Protein {entry.runningTotals.protein_g.toFixed(1)} g · Carbs{" "}
                  {entry.runningTotals.carbs_g.toFixed(1)} g · Fat{" "}
                  {entry.runningTotals.fat_g.toFixed(1)} g
                </Typography>
                {entry.notes && (
                  <Typography variant="body2">Notes: {entry.notes}</Typography>
                )}
              </Stack>
            ) : (
              <Typography sx={{ whiteSpace: "pre-wrap", mt: 1 }}>
                {entry.response}
              </Typography>
            )}
            {entry.parseError && (
              <Alert severity="warning" sx={{ mt: 1 }}>
                Could not parse structured response; showing raw output.
              </Alert>
            )}
          </Paper>
        ))}
      </Stack>
    </Paper>
  );
}

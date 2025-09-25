import { MenuItem, Stack, TextField, Typography } from "@mui/material";

import {
  type FormState,
  activityLevels,
  goalOptions,
  type GoalValue,
} from "./types";

type FormStepProps = {
  stepIndex: number;
  form: FormState;
  onChange: (fields: Partial<FormState>) => void;
};

export function FormStep({ stepIndex, form, onChange }: FormStepProps) {
  if (stepIndex === 0) {
    return (
      <Stack spacing={2}>
        <Typography variant="h6">Tell us about yourself</Typography>
        <TextField
          label="Preferred name (optional)"
          value={form.name}
          onChange={(e) => onChange({ name: e.target.value })}
        />
        <TextField
          select
          required
          label="Sex"
          value={form.sex}
          onChange={(e) =>
            onChange({ sex: e.target.value as FormState["sex"] })
          }
        >
          <MenuItem value="male">Male</MenuItem>
          <MenuItem value="female">Female</MenuItem>
          <MenuItem value="nonbinary">Non-binary</MenuItem>
        </TextField>
        <TextField
          required
          label="Age (years)"
          type="number"
          inputProps={{ min: 10 }}
          value={form.ageYears}
          onChange={(e) => onChange({ ageYears: e.target.value })}
        />
      </Stack>
    );
  }

  if (stepIndex === 1) {
    return (
      <Stack spacing={2}>
        <Typography variant="h6">Measurements</Typography>
        <TextField
          required
          label="Height (cm)"
          type="number"
          inputProps={{ min: 100 }}
          value={form.heightCm}
          onChange={(e) => onChange({ heightCm: e.target.value })}
        />
        <TextField
          required
          label="Weight (kg)"
          type="number"
          inputProps={{ min: 30 }}
          value={form.weightKg}
          onChange={(e) => onChange({ weightKg: e.target.value })}
        />
      </Stack>
    );
  }

  return (
    <Stack spacing={2}>
      <Typography variant="h6">Lifestyle & goal</Typography>
      <TextField
        select
        required
        label="Activity level"
        value={form.activityLevel}
        onChange={(e) => onChange({ activityLevel: e.target.value })}
      >
        {activityLevels.map((option) => (
          <MenuItem key={option.value} value={option.value}>
            {option.label}
          </MenuItem>
        ))}
      </TextField>
      <TextField
        select
        required
        label="Goal"
        value={form.goal}
        onChange={(e) => onChange({ goal: e.target.value as GoalValue })}
      >
        {goalOptions.map((goal) => (
          <MenuItem key={goal.value} value={goal.value}>
            {goal.label}
          </MenuItem>
        ))}
      </TextField>
      {form.goal && (
        <Typography variant="body2" color="text.secondary">
          {goalOptions.find((g) => g.value === form.goal)?.helper ||
            "Choose a comfortable pace"}
        </Typography>
      )}
      <TextField
        label="Weekly rate (kg/week)"
        type="number"
        value={form.weeklyRate}
        onChange={(e) => onChange({ weeklyRate: e.target.value })}
        helperText="Positive for gain, negative for loss."
      />
      <TextField
        label="Notes or dietary preferences (optional)"
        multiline
        minRows={2}
        value={form.dietaryNotes}
        onChange={(e) => onChange({ dietaryNotes: e.target.value })}
      />
    </Stack>
  );
}

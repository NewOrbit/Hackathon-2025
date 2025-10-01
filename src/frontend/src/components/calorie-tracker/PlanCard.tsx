import {
  Alert,
  Button,
  CircularProgress,
  Paper,
  Stack,
  Typography,
} from "@mui/material";

type PlanCardProps = {
  plan: string;
  loading: boolean;
  error: string | null;
  onBackToEdit: () => void;
  onReset: () => void;
};

export function PlanCard({
  plan,
  loading,
  error,
  onBackToEdit,
  onReset,
}: PlanCardProps) {
  return (
    <Stack spacing={2}>
      <Typography variant="h6">Your personalised plan</Typography>
      {loading ? (
        <Stack direction="row" spacing={1} alignItems="center">
          <CircularProgress size={20} />
          <Typography variant="body2">Creating your plan…</Typography>
        </Stack>
      ) : (
        <Paper variant="outlined" sx={{ p: 2 }}>
          <Typography sx={{ whiteSpace: "pre-wrap" }}>{plan}</Typography>
        </Paper>
      )}
      {error && <Alert severity="error">{error}</Alert>}
      <Stack direction="row" spacing={1}>
        <Button variant="outlined" onClick={onBackToEdit} disabled={loading}>
          Update details
        </Button>
        <Button
          variant="outlined"
          color="inherit"
          onClick={onReset}
          disabled={loading}
        >
          Start over
        </Button>
      </Stack>
    </Stack>
  );
}

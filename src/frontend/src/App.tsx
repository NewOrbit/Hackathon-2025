import { CssBaseline, Stack } from "@mui/material";
import CalorieTracker from "./components/CalorieTracker";

function App() {
  return (
    <>
      <CssBaseline />
      <Stack direction="column" minHeight="100dvh" px={{ xs: 2, md: 4 }}>
        <CalorieTracker />
      </Stack>
    </>
  );
}

export default App;

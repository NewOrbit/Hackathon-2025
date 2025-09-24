import { CssBaseline, Stack } from "@mui/material";
import CalorieTracker from "./components/CalorieTracker";
import ChatWidget from "./components/ChatWidget";

function App() {
  return (
    <>
      <CssBaseline />
      <Stack direction="column" minHeight="100dvh" px={{ xs: 2, md: 4 }}>
        <CalorieTracker />
      </Stack>
      <ChatWidget />
    </>
  );
}

export default App;

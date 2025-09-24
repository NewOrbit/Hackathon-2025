import { Stack } from "@mui/material";
import Chat from "./components/Chat";

function App() {
  return (
    <Stack
      direction="column"
      alignItems="center"
      justifyContent="center"
      height="100dvh"
    >
      <Chat />
    </Stack>
  );
}

export default App;

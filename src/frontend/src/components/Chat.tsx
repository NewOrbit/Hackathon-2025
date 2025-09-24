import { useEffect, useRef, useState } from "react";
import {
  Box,
  Button,
  Paper,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import { initSession, sendMessage } from "../api/api";

type Message = { role: "user" | "assistant"; content: string };

export default function Chat() {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const endRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    (async () => {
      try {
        const init = await initSession();
        setSessionId(init.sessionId);
      } catch (e) {
        console.error(e);
      }
    })();
  }, []);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function onSend() {
    const text = input.trim();
    if (!text || !sessionId) return;
    setInput("");
    setMessages((m) => [...m, { role: "user", content: text }]);
    setBusy(true);
    try {
      const res = await sendMessage(sessionId, text);
      setSessionId(res.sessionId);
      setMessages((m) => [...m, { role: "assistant", content: res.output }]);
    } catch (e) {
      console.error(e);
      setMessages((m) => [
        ...m,
        {
          role: "assistant",
          content: "Sorry, something went wrong. Please try again.",
        },
      ]);
    } finally {
      setBusy(false);
    }
  }

  return (
    <Stack spacing={2} sx={{ width: "min(900px, 100%)", height: "100%" }}>
      <Typography variant="h4" fontWeight={700}>
        Agent Chat
      </Typography>
      <Paper
        variant="outlined"
        sx={{ p: 2, flex: 1, overflow: "auto", minHeight: 300 }}
      >
        <Stack spacing={1}>
          {messages.map((m, i) => (
            <Box key={i} sx={{ whiteSpace: "pre-wrap" }}>
              <Typography variant="subtitle2" color="text.secondary">
                {m.role === "user" ? "You" : "Assistant"}
              </Typography>
              <Typography>{m.content}</Typography>
            </Box>
          ))}
          <div ref={endRef} />
        </Stack>
      </Paper>
      <Stack direction="row" spacing={1}>
        <TextField
          fullWidth
          placeholder="Ask something..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              onSend();
            }
          }}
        />
        <Button
          variant="contained"
          disabled={busy || !input.trim()}
          onClick={onSend}
        >
          Send
        </Button>
      </Stack>
    </Stack>
  );
}

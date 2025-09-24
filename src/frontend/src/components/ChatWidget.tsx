import { useEffect, useRef, useState } from "react";
import {
  Box,
  Fab,
  IconButton,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import { FiMessageSquare, FiX } from "react-icons/fi";

import { initSession, sendMessage } from "../api/api";

type Message = { role: "user" | "assistant"; content: string };

export default function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const scrollRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (!open || sessionId) return;
    (async () => {
      try {
        const init = await initSession();
        setSessionId(init.sessionId);
        setMessages([
          {
            role: "assistant",
            content:
              "Hi! I'm your AI assistant. Ask me anything about your nutrition plan or meals.",
          },
        ]);
      } catch (error) {
        console.error("Failed to initialise chat session", error);
      }
    })();
  }, [open, sessionId]);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, open]);

  const handleToggle = () => {
    setOpen((prev) => !prev);
  };

  const handleSend = async () => {
    const text = input.trim();
    if (!text || !sessionId) return;

    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: text }]);
    setBusy(true);
    try {
      const res = await sendMessage(sessionId, text);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: res.output },
      ]);
    } catch (error) {
      console.error(error);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Sorry, something went wrong. Please try again.",
        },
      ]);
    } finally {
      setBusy(false);
    }
  };

  return (
    <>
      <Fab
        color="primary"
        onClick={handleToggle}
        sx={{
          position: "fixed",
          bottom: 24,
          right: 24,
          zIndex: 1400,
        }}
      >
        {open ? <FiX size={20} /> : <FiMessageSquare size={20} />}
      </Fab>

      {open && (
        <Box
          sx={{
            position: "fixed",
            bottom: 96,
            right: 24,
            width: 360,
            height: 460,
            bgcolor: "background.paper",
            boxShadow: 6,
            borderRadius: 2,
            display: "flex",
            flexDirection: "column",
            zIndex: 1399,
          }}
        >
          <Stack
            direction="row"
            alignItems="center"
            justifyContent="space-between"
            sx={{ px: 2, py: 1.5, borderBottom: 1, borderColor: "divider" }}
          >
            <Typography variant="subtitle1" fontWeight={600}>
              Chat with AI
            </Typography>
            <IconButton size="small" onClick={handleToggle}>
              <FiX size={18} />
            </IconButton>
          </Stack>

          <Box
            sx={{
              flexGrow: 1,
              overflowY: "auto",
              px: 2,
              py: 1.5,
              gap: 1,
              display: "flex",
              flexDirection: "column",
            }}
          >
            {messages.map((msg, idx) => (
              <Box
                key={`${msg.role}-${idx}-${msg.content.slice(0, 10)}`}
                sx={{
                  alignSelf: msg.role === "user" ? "flex-end" : "flex-start",
                  bgcolor: msg.role === "user" ? "primary.main" : "grey.200",
                  color:
                    msg.role === "user"
                      ? "primary.contrastText"
                      : "text.primary",
                  px: 1.5,
                  py: 1,
                  borderRadius: 2,
                  maxWidth: "85%",
                  whiteSpace: "pre-wrap",
                }}
              >
                <Typography variant="body2">{msg.content}</Typography>
              </Box>
            ))}
            <div ref={scrollRef} />
          </Box>

          <Box sx={{ px: 2, py: 1.5, borderTop: 1, borderColor: "divider" }}>
            <TextField
              fullWidth
              size="small"
              placeholder="Type your message..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
              disabled={busy || !sessionId}
            />
          </Box>
        </Box>
      )}
    </>
  );
}

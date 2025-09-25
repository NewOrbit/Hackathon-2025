export type InitResponse = { sessionId: string };
export type ChatResponse = { sessionId: string; output: string };

const BASE_URL = import.meta.env.VITE_AGENT_URL ?? "http://localhost:8080";

export async function initSession(): Promise<InitResponse> {
  const res = await fetch(`${BASE_URL}/init`, { method: "POST" });
  if (!res.ok) throw new Error(`init failed: ${res.status}`);
  return res.json();
}

export async function sendMessage(
  sessionId: string,
  message: string
): Promise<ChatResponse> {
  const res = await fetch(`${BASE_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ sessionId, message }),
  });
  if (!res.ok) throw new Error(`chat failed: ${res.status}`);
  return res.json();
}

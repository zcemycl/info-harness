import { useCallback, useEffect, useState, type FormEvent } from "react";
import { apiFetch } from "@/api/client";
import { MarkdownMessage } from "@/components/MarkdownMessage";
import { RunActivity } from "@/components/step-graph/RunActivity";
import { useAuth } from "@/hooks";
import type { ChatMessage, ChatMeta, RunEvent } from "@/types";
import { followRun } from "./followRun";

export function ChatPage() {
  const { accessToken, logout, user } = useAuth();
  const [chats, setChats] = useState<ChatMeta[]>([]);
  const [chatId, setChatId] = useState<string>("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [stages, setStages] = useState<RunEvent[]>([]);
  const [settled, setSettled] = useState(false);
  const [prompt, setPrompt] = useState("");
  const [error, setError] = useState<string | null>(null);
  const token = accessToken ?? "";

  const accountId = user?.userId ?? "";

  const loadChats = useCallback(async () => {
    const response = await apiFetch(token, "/chats");
    if (!response.ok) throw new Error(await response.text());
    setChats((await response.json()) as ChatMeta[]);
  }, [token]);

  const openChat = useCallback(
    async (id: string) => {
      setChatId(id);
      setStages([]);
      setSettled(false);
      const response = await apiFetch(token, `/chats/${id}`);
      if (!response.ok) throw new Error(await response.text());
      setMessages((await response.json()) as ChatMessage[]);
    },
    [token],
  );

  useEffect(() => {
    setChatId("");
    setMessages([]);
    setStages([]);
    setSettled(false);
    setChats([]);
    setError(null);
    if (!accountId) return;
    void loadChats().catch((err: unknown) =>
      setError(err instanceof Error ? err.message : "Failed to load chats"),
    );
  }, [accountId, loadChats]);

  async function removeChat(id: string) {
    setError(null);
    const response = await apiFetch(token, `/chats/${id}`, { method: "DELETE" });
    if (!response.ok && response.status !== 204) {
      setError(await response.text());
      return;
    }
    if (chatId === id) {
      setChatId("");
      setMessages([]);
      setStages([]);
      setSettled(false);
    }
    await loadChats();
  }

  async function createChat() {
    const response = await apiFetch(token, "/chats", { method: "POST" });
    if (!response.ok) throw new Error(await response.text());
    const meta = (await response.json()) as ChatMeta;
    await loadChats();
    await openChat(meta.chat_id);
    return meta.chat_id;
  }

  function onStage(event: RunEvent) {
    if (event.type === "stage" || event.type === "error") {
      setStages((current) => (current.some((item) => item.seq === event.seq) ? current : [...current, event]));
    }
    if (event.type === "final" || event.type === "error") setSettled(true);
    if (event.type === "stage") return;
    setMessages((current) => [
      ...current,
      {
        role: "assistant",
        content: event.answer || event.summary || "No answer",
        ts: "",
        run_id: null,
      },
    ]);
  }

  async function follow(runId: string) {
    setStages([]);
    setSettled(false);
    await followRun(token, runId, onStage);
  }

  async function send(event: FormEvent) {
    event.preventDefault();
    const text = prompt.trim();
    if (!text || !token) return;
    setError(null);
    setPrompt("");
    try {
      const id = chatId || (await createChat());
      setMessages((current) => [...current, { role: "user", content: text, ts: "", run_id: null }]);
      const response = await apiFetch(token, `/chats/${id}/messages`, {
        method: "POST",
        body: JSON.stringify({ prompt: text }),
      });
      if (!response.ok) throw new Error(await response.text());
      const body = (await response.json()) as { run_id: string };
      await follow(body.run_id);
      await loadChats();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Send failed");
    }
  }

  return (
    <div className="grid min-h-svh grid-cols-1 bg-[#f4f7f5] md:grid-cols-[260px_1fr]">
      <aside className="flex flex-col gap-3 border-b border-[#0c1f1a]/10 bg-[#efe8db] p-4 md:border-r md:border-b-0">
        <div className="flex items-center justify-between">
          <h1 className="font-mono text-sm font-bold tracking-wide">info-harness</h1>
          <button type="button" className="text-sm underline" onClick={() => void logout()}>
            Sign out
          </button>
        </div>
        <p className="truncate text-xs text-[#5a7a6c]">{user?.username}</p>
        <button type="button" className="rounded-lg bg-[#0c1f1a] px-3 py-2 text-sm text-white" onClick={() => void createChat()}>
          New chat
        </button>
        <ul className="space-y-1 overflow-auto">
          {chats.map((chat) => (
            <li key={chat.chat_id} className="flex items-center gap-1">
              <button type="button" className="min-w-0 flex-1 truncate rounded px-2 py-1 text-left text-sm hover:bg-[#d9cbb3]" onClick={() => void openChat(chat.chat_id)}>
                {chat.title}
              </button>
              <button
                type="button"
                className="rounded px-1.5 text-lg leading-none text-[#5a7a6c] hover:bg-[#d9cbb3] hover:text-[#0c1f1a]"
                aria-label={`Delete ${chat.title}`}
                onClick={() => void removeChat(chat.chat_id)}
              >
                ×
              </button>
            </li>
          ))}
        </ul>
      </aside>
      <main className="flex min-h-svh flex-col p-4">
        {error ? <p className="mb-3 rounded bg-red-50 px-3 py-2 text-sm text-red-700">{error}</p> : null}
        <form className="grid grid-cols-[1fr_auto] gap-2" onSubmit={(event) => void send(event)}>
          <textarea className="rounded-lg border px-3 py-2" rows={3} value={prompt} onChange={(event) => setPrompt(event.target.value)} placeholder="Ask a research question" required />
          <button className="rounded-lg bg-[#0c1f1a] px-4 text-white" type="submit">
            Send
          </button>
        </form>
        {stages.length > 0 ? <RunActivity events={stages} settled={settled} /> : null}
        <ol className="mt-3 flex-1 space-y-2 overflow-auto">
          {messages.map((message, index) => (
            <li
              key={`${message.ts}-${index}`}
              className={`rounded-lg px-3 py-2 text-sm ${message.role === "user" ? "whitespace-pre-wrap bg-[#e7f0ea]" : "border bg-white"}`}
            >
              {message.role === "assistant" ? <MarkdownMessage text={message.content} /> : message.content}
            </li>
          ))}
        </ol>
      </main>
    </div>
  );
}

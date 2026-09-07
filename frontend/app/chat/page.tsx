"use client";

import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { askQuestion, getMe } from "@/lib/api";
import { Input } from "@/components/ui/input";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { ScrollArea } from "@/components/ui/scroll-area";

// iZone brand
// Navy:    #1E3169
// Gold:    #F5A623
// Gradient: linear-gradient(to right, #1E3169, #F5A623)

type Message = {
  role: "user" | "assistant";
  content: string;
};

const SUGGESTIONS = [
  "What services does I-Zone offer?",
  "How can I hire a developer?",
  "What is I-Zone's AI expertise?",
  "Tell me about I-Zone's process",
];

const BRAND_GRADIENT = "linear-gradient(to right, #1E3169 0%, #F5A623 100%)";
const NAVY = "#1E3169";
const GOLD = "#F5A623";

export default function ChatPage() {
  const router = useRouter();
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [userName, setUserName] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) { router.push("/"); return; }
    getMe(token)
      .then((u) => setUserName(u.full_name || u.email))
      .catch(() => { localStorage.removeItem("token"); router.push("/"); });
  }, [router]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function handleSend(e: React.FormEvent) {
    e.preventDefault();
    if (!input.trim() || loading) return;
    const question = input.trim();
    setInput("");
    setMessages((p) => [...p, { role: "user", content: question }]);
    setLoading(true);
    try {
      const token = localStorage.getItem("token")!;
      const data = await askQuestion(question, token);
      setMessages((p) => [...p, { role: "assistant", content: data.answer }]);
    } catch {
      setMessages((p) => [...p, { role: "assistant", content: "Sorry, something went wrong. Please try again." }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex flex-col h-screen bg-white" style={{ fontFamily: "var(--font-montserrat), sans-serif" }}>

      {/* Subtle background tint */}
      <div
        className="fixed inset-0 pointer-events-none"
        style={{
          background:
            "radial-gradient(ellipse at 90% 0%, rgba(245,166,35,0.09) 0%, transparent 50%)",
        }}
      />

      {/* Header */}
      <header className="relative bg-white border-b border-gray-100 px-6 py-3 flex items-center justify-between shrink-0">
        <div className="flex items-center gap-3">
          <img
            src="/izone-logo.svg"
            alt="iZone Technologies"
            width={100}
          />
          <span className="text-gray-300 select-none">|</span>
          <span className="text-sm font-medium" style={{ color: "#6b7280" }}>
            AI Assistant
          </span>
        </div>

        <div className="flex items-center gap-3">
          <Avatar className="h-8 w-8">
            <AvatarFallback
              className="text-white text-xs font-bold"
              style={{ background: BRAND_GRADIENT }}
            >
              {userName.charAt(0).toUpperCase()}
            </AvatarFallback>
          </Avatar>
          <span className="text-sm font-medium hidden sm:block" style={{ color: "#374151" }}>
            {userName}
          </span>
          <button
            onClick={() => { localStorage.removeItem("token"); router.push("/"); }}
            className="text-xs border border-gray-200 rounded-full px-3 py-1.5 transition-colors hover:bg-gray-50"
            style={{ color: "#6b7280" }}
          >
            Sign out
          </button>
        </div>
      </header>

      {/* Messages */}
      <ScrollArea className="flex-1 px-4 py-6 relative">
        <div className="max-w-2xl mx-auto space-y-5">

          {/* Welcome state */}
          {messages.length === 0 && (
            <div className="text-center py-14">
              <div
                className="inline-flex items-center gap-2 rounded-full px-4 py-1.5 mb-6 text-sm font-semibold text-white"
                style={{ background: BRAND_GRADIENT }}
              >
                Software Outsourcing · SaaS · AI Engineering
              </div>
              <h2
                className="text-4xl font-black leading-tight mb-4"
                style={{ color: NAVY }}
              >
                How can I help<br />you today?
              </h2>
              <p className="text-base max-w-sm mx-auto mb-10" style={{ color: "#9ca3af" }}>
                Ask me anything about I-Zone Technologies.
              </p>
              <div className="flex flex-wrap gap-3 justify-center">
                {SUGGESTIONS.map((s) => (
                  <button
                    key={s}
                    onClick={() => setInput(s)}
                    className="text-sm bg-white border border-gray-200 rounded-full px-5 py-2.5 font-medium transition-all shadow-sm"
                    style={{ color: "#374151" }}
                    onMouseEnter={(e) => {
                      const btn = e.currentTarget as HTMLButtonElement;
                      btn.style.background = BRAND_GRADIENT;
                      btn.style.borderColor = "transparent";
                      btn.style.color = "white";
                    }}
                    onMouseLeave={(e) => {
                      const btn = e.currentTarget as HTMLButtonElement;
                      btn.style.background = "white";
                      btn.style.borderColor = "#e5e7eb";
                      btn.style.color = "#374151";
                    }}
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Message bubbles */}
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`flex gap-3 ${msg.role === "user" ? "justify-end" : "justify-start"}`}
            >
              {msg.role === "assistant" && (
                <div
                  className="shrink-0 w-8 h-8 rounded-full flex items-center justify-center mt-0.5"
                  style={{ background: BRAND_GRADIENT }}
                >
                  <span className="text-white text-xs font-black">IZ</span>
                </div>
              )}
              <div
                className={`max-w-[75%] rounded-2xl px-4 py-3 text-sm leading-relaxed font-medium ${
                  msg.role === "user"
                    ? "text-white rounded-br-sm"
                    : "bg-gray-50 border border-gray-100 rounded-bl-sm"
                }`}
                style={
                  msg.role === "user"
                    ? { background: BRAND_GRADIENT }
                    : { color: "#1f2937" }
                }
              >
                {msg.content}
              </div>
              {msg.role === "user" && (
                <Avatar className="h-8 w-8 shrink-0 mt-0.5">
                  <AvatarFallback
                    className="text-white text-xs font-bold"
                    style={{ background: BRAND_GRADIENT }}
                  >
                    {userName.charAt(0).toUpperCase()}
                  </AvatarFallback>
                </Avatar>
              )}
            </div>
          ))}

          {/* Loading dots */}
          {loading && (
            <div className="flex gap-3 justify-start">
              <div
                className="shrink-0 w-8 h-8 rounded-full flex items-center justify-center"
                style={{ background: BRAND_GRADIENT }}
              >
                <span className="text-white text-xs font-black">IZ</span>
              </div>
              <div className="bg-gray-50 border border-gray-100 rounded-2xl rounded-bl-sm px-4 py-3">
                <div className="flex gap-1 items-center h-4">
                  <span
                    className="w-2 h-2 rounded-full animate-bounce"
                    style={{ background: NAVY, animationDelay: "0ms" }}
                  />
                  <span
                    className="w-2 h-2 rounded-full animate-bounce"
                    style={{ background: "#3a5ab5", animationDelay: "150ms" }}
                  />
                  <span
                    className="w-2 h-2 rounded-full animate-bounce"
                    style={{ background: GOLD, animationDelay: "300ms" }}
                  />
                </div>
              </div>
            </div>
          )}

          <div ref={bottomRef} />
        </div>
      </ScrollArea>

      {/* Input bar */}
      <div className="relative bg-white border-t border-gray-100 px-4 py-4 shrink-0">
        <form onSubmit={handleSend} className="max-w-2xl mx-auto flex gap-3">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a question about I-Zone Technologies..."
            disabled={loading}
            className="flex-1 h-11 border-gray-200 bg-gray-50 placeholder:text-gray-400 rounded-full px-5 font-medium"
            style={{
              color: NAVY,
              fontFamily: "var(--font-montserrat), sans-serif",
            }}
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="h-11 px-6 rounded-full text-white font-bold text-sm disabled:opacity-50 shrink-0 transition-opacity"
            style={{
              background: BRAND_GRADIENT,
              fontFamily: "var(--font-montserrat), sans-serif",
            }}
          >
            Send →
          </button>
        </form>
      </div>

    </div>
  );
}

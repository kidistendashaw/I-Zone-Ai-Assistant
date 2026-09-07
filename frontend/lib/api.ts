const API_URL = "http://localhost:8000";

// ─── Auth ────────────────────────────────────────────────────────────────────

export async function login(email: string, password: string) {
  const res = await fetch(`${API_URL}/api/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) throw new Error("Invalid email or password");
  return res.json(); // { access_token, token_type }
}

export async function signup(email: string, password: string, full_name: string) {
  const res = await fetch(`${API_URL}/api/auth/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password, full_name }),
  });
  if (!res.ok) throw new Error("Signup failed");
  return res.json();
}

export async function getMe(token: string) {
  const res = await fetch(`${API_URL}/api/auth/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error("Not authenticated");
  return res.json(); // { id, email, full_name, role }
}

// ─── Chat ────────────────────────────────────────────────────────────────────

export async function askQuestion(question: string, token: string) {
  const res = await fetch(`${API_URL}/api/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ question }),
  });
  if (!res.ok) throw new Error("Failed to get answer");
  return res.json(); // { answer, conversation_id, question }
}

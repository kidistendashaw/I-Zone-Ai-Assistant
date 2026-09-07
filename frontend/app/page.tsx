"use client";

import { Suspense, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Eye, EyeOff } from "lucide-react";
import { login } from "@/lib/api";
import { Input } from "@/components/ui/input";

function LoginForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const justRegistered = searchParams.get("registered") === "1";

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const data = await login(email, password);
      localStorage.setItem("token", data.access_token);
      router.push("/chat");
    } catch {
      setError("Invalid email or password. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="relative w-full max-w-sm px-6">

      {/* Logo */}
      <div className="flex flex-col items-center mb-10">
        <img
          src="/izone-logo.svg"
          alt="iZone Technologies"
          width={140}
          className="mb-4"
        />
        <h1
          className="text-2xl font-black mb-1"
          style={{ color: "#1E3169", fontFamily: "var(--font-montserrat), sans-serif" }}
        >
          AI Assistant
        </h1>
        <p className="text-sm" style={{ color: "#9ca3af" }}>
          Sign in to your account
        </p>
      </div>

      {/* Form */}
      <form onSubmit={handleLogin} className="space-y-4">

        <div>
          <label className="text-sm font-semibold block mb-1.5" style={{ color: "#1E3169" }}>
            Email address
          </label>
          <Input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@izone.com"
            required
            className="h-11 border-gray-200 rounded-xl bg-gray-50 text-gray-900 placeholder:text-gray-400"
            style={{ fontFamily: "var(--font-montserrat), sans-serif" }}
          />
        </div>

        <div>
          <label className="text-sm font-semibold block mb-1.5" style={{ color: "#1E3169" }}>
            Password
          </label>
          <div className="relative">
            <input
              type={showPassword ? "text" : "password"}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              required
              className="w-full h-11 border border-gray-200 rounded-xl bg-gray-50 text-gray-900 placeholder:text-gray-400 px-3 pr-11 text-sm outline-none focus:border-[#1E3169] focus:ring-1 focus:ring-[#1E3169]"
              style={{ fontFamily: "var(--font-montserrat), sans-serif" }}
            />
            <button
              type="button"
              onClick={() => setShowPassword((v) => !v)}
              tabIndex={-1}
              aria-label={showPassword ? "Hide password" : "Show password"}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors z-10 cursor-pointer"
            >
              {showPassword ? <Eye size={18} /> : <EyeOff size={18} />}
            </button>
          </div>
        </div>

        {/* Success message after registration */}
        {justRegistered && (
          <div className="bg-green-50 border border-green-100 rounded-xl px-4 py-3">
            <p className="text-green-600 text-sm font-medium">
              Account created successfully. Sign in below.
            </p>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="bg-red-50 border border-red-100 rounded-xl px-4 py-3">
            <p className="text-red-500 text-sm">{error}</p>
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          className="w-full h-11 rounded-full text-white font-bold text-sm transition-opacity disabled:opacity-60 mt-2"
          style={{
            background: "linear-gradient(to right, #1E3169 0%, #F5A623 100%)",
            fontFamily: "var(--font-montserrat), sans-serif",
            letterSpacing: "0.01em",
          }}
        >
          {loading ? "Signing in..." : "Sign in →"}
        </button>
      </form>

      {/* Link to signup */}
      <p
        className="text-center text-sm mt-6"
        style={{ color: "#6b7280", fontFamily: "var(--font-montserrat), sans-serif" }}
      >
        Don&apos;t have an account?{" "}
        <a href="/signup" className="font-semibold hover:underline" style={{ color: "#1E3169" }}>
          Sign up
        </a>
      </p>

      <p
        className="text-center text-xs mt-4"
        style={{ color: "#9ca3af", fontFamily: "var(--font-montserrat), sans-serif" }}
      >
        I-Zone Technologies · AI Assistant
      </p>
    </div>
  );
}

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-white">
      {/* Subtle brand background tint */}
      <div
        className="fixed inset-0 pointer-events-none"
        style={{
          background:
            "radial-gradient(ellipse at 80% 0%, rgba(245,166,35,0.10) 0%, transparent 55%), radial-gradient(ellipse at 20% 100%, rgba(30,49,105,0.07) 0%, transparent 55%)",
        }}
      />
      <Suspense fallback={null}>
        <LoginForm />
      </Suspense>
    </div>
  );
}

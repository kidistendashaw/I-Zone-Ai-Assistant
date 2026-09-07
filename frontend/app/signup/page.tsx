"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Eye, EyeOff } from "lucide-react";
import { signup } from "@/lib/api";

export default function SignupPage() {
  const router = useRouter();
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSignup(e: React.FormEvent) {
    e.preventDefault();
    setError("");

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }
    if (password.length < 8) {
      setError("Password must be at least 8 characters.");
      return;
    }

    setLoading(true);
    try {
      await signup(email, password, fullName);
      // Account created — go to login
      router.push("/?registered=1");
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : "";
      if (message.toLowerCase().includes("already")) {
        setError("An account with this email already exists.");
      } else {
        setError("Something went wrong. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  }

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

      <div className="relative w-full max-w-sm px-6 py-10">

        {/* Logo */}
        <div className="flex flex-col items-center mb-8">
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
            Create Account
          </h1>
          <p className="text-sm" style={{ color: "#9ca3af" }}>
            Join I-Zone AI Assistant
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleSignup} className="space-y-4">

          {/* Full name */}
          <div>
            <label
              className="text-sm font-semibold block mb-1.5"
              style={{ color: "#1E3169" }}
            >
              Full name
            </label>
            <Input
              type="text"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              placeholder="Kidist Endashaw"
              required
              className="h-11 border-gray-200 rounded-xl bg-gray-50 text-gray-900 placeholder:text-gray-400"
              style={{ fontFamily: "var(--font-montserrat), sans-serif" }}
            />
          </div>

          {/* Email */}
          <div>
            <label
              className="text-sm font-semibold block mb-1.5"
              style={{ color: "#1E3169" }}
            >
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

          {/* Password */}
          <div>
            <label className="text-sm font-semibold block mb-1.5" style={{ color: "#1E3169" }}>
              Password
            </label>
            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Min. 8 characters"
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

          {/* Confirm password */}
          <div>
            <label className="text-sm font-semibold block mb-1.5" style={{ color: "#1E3169" }}>
              Confirm password
            </label>
            <div className="relative">
              <input
                type={showConfirm ? "text" : "password"}
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="••••••••"
                required
                className="w-full h-11 border border-gray-200 rounded-xl bg-gray-50 text-gray-900 placeholder:text-gray-400 px-3 pr-11 text-sm outline-none focus:border-[#1E3169] focus:ring-1 focus:ring-[#1E3169]"
                style={{ fontFamily: "var(--font-montserrat), sans-serif" }}
              />
              <button
                type="button"
                onClick={() => setShowConfirm((v) => !v)}
                tabIndex={-1}
                aria-label={showConfirm ? "Hide password" : "Show password"}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors z-10 cursor-pointer"
              >
                {showConfirm ? <Eye size={18} /> : <EyeOff size={18} />}
              </button>
            </div>
          </div>

          {/* Error */}
          {error && (
            <div className="bg-red-50 border border-red-100 rounded-xl px-4 py-3">
              <p className="text-red-500 text-sm">{error}</p>
            </div>
          )}

          {/* Submit */}
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
            {loading ? "Creating account..." : "Create account →"}
          </button>
        </form>

        {/* Link to login */}
        <p
          className="text-center text-sm mt-6"
          style={{ color: "#6b7280", fontFamily: "var(--font-montserrat), sans-serif" }}
        >
          Already have an account?{" "}
          <a
            href="/"
            className="font-semibold hover:underline"
            style={{ color: "#1E3169" }}
          >
            Sign in
          </a>
        </p>

        <p
          className="text-center text-xs mt-6"
          style={{ color: "#9ca3af", fontFamily: "var(--font-montserrat), sans-serif" }}
        >
          I-Zone Technologies · AI Assistant
        </p>
      </div>
    </div>
  );
}

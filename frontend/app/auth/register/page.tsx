"use client";

import { useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Eye, EyeOff, Loader2, Check } from "lucide-react";

const industries = [
  "E-Commerce (B2C)", "B2B Enterprise SaaS", "EdTech & Professional Courses",
  "FinTech", "D2C / FMCG", "Travel & Hospitality", "Healthcare", "Other",
];
const steps = ["Company", "Account", "Confirm"];

function slugify(t: string) {
  return t.toLowerCase().replace(/\s+/g, "-").replace(/[^a-z0-9-]/g, "");
}

export default function RegisterPage() {
  const [step, setStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [showPw, setShowPw] = useState(false);
  const [form, setForm] = useState({ companyName: "", slug: "", industry: "", adminName: "", email: "", password: "" });

  const setCompanyName = (v: string) => setForm({ ...form, companyName: v, slug: slugify(v) });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (step < 2) { setStep(step + 1); return; }
    setLoading(true);
    await new Promise((r) => setTimeout(r, 1500));
    setLoading(false);
    window.location.href = `/dashboard/${form.slug}`;
  };

  return (
    <div className="w-full max-w-[440px]">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-slate-900 mb-2">Create your workspace</h1>
        <p className="text-slate-500 text-sm">
          Already have an account?{" "}
          <Link href="/auth/login" className="text-primary-600 font-medium hover:underline">Sign in</Link>
        </p>
      </div>

      {/* Step indicator */}
      <div className="flex items-center gap-2 mb-8">
        {steps.map((s, i) => (
          <div key={s} className="flex items-center gap-2">
            <div className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-semibold transition-all ${
              i < step ? "bg-primary-600 text-white" : i === step ? "bg-slate-900 text-white" : "bg-slate-100 text-slate-400"
            }`}>
              {i < step ? <Check className="w-3.5 h-3.5" /> : i + 1}
            </div>
            <span className={`text-sm font-medium ${i === step ? "text-slate-900" : "text-slate-400"}`}>{s}</span>
            {i < steps.length - 1 && <div className={`h-px w-8 ${i < step ? "bg-primary-600" : "bg-slate-200"}`} />}
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="space-y-4">
        {step === 0 && (
          <>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1.5">Company name</label>
              <Input placeholder="Acme Corp" value={form.companyName} onChange={(e) => setCompanyName(e.target.value)} required autoFocus />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1.5">Workspace URL</label>
              <div className="flex rounded-lg border border-slate-200 overflow-hidden focus-within:ring-2 focus-within:ring-primary-600 bg-white">
                <span className="bg-slate-50 border-r border-slate-200 px-3 flex items-center text-xs text-slate-400 shrink-0">
                  app.attributeiq.com/
                </span>
                <input className="flex-1 px-3 py-2 text-sm text-slate-900 bg-white outline-none placeholder:text-slate-300"
                  placeholder="acme-corp" value={form.slug}
                  onChange={(e) => setForm({ ...form, slug: e.target.value })} required />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1.5">Industry</label>
              <select className="flex h-10 w-full rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm text-slate-900 focus:outline-none focus:ring-2 focus:ring-primary-600"
                value={form.industry} onChange={(e) => setForm({ ...form, industry: e.target.value })} required>
                <option value="" disabled>Select your industry</option>
                {industries.map((i) => <option key={i} value={i}>{i}</option>)}
              </select>
            </div>
          </>
        )}

        {step === 1 && (
          <>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1.5">Your full name</label>
              <Input placeholder="Priya Sharma" value={form.adminName} onChange={(e) => setForm({ ...form, adminName: e.target.value })} required autoFocus />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1.5">Work email</label>
              <Input type="email" placeholder="priya@acme.com" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1.5">Password</label>
              <div className="relative">
                <Input type={showPw ? "text" : "password"} placeholder="Min. 8 characters"
                  value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })}
                  required minLength={8} className="pr-10" />
                <button type="button" onClick={() => setShowPw(!showPw)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600">
                  {showPw ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>
          </>
        )}

        {step === 2 && (
          <div className="bg-slate-50 rounded-xl border border-slate-200 p-5 space-y-3">
            <h3 className="text-sm font-semibold text-slate-900 mb-4">Review your workspace</h3>
            {[
              { label: "Company", value: form.companyName },
              { label: "URL", value: `app.attributeiq.com/${form.slug}` },
              { label: "Industry", value: form.industry },
              { label: "Admin", value: form.adminName },
              { label: "Email", value: form.email },
            ].map(({ label, value }) => (
              <div key={label} className="flex justify-between text-sm">
                <span className="text-slate-500">{label}</span>
                <span className="text-slate-900 font-medium">{value}</span>
              </div>
            ))}
          </div>
        )}

        <div className="flex gap-3 pt-2">
          {step > 0 && (
            <Button type="button" variant="outline" onClick={() => setStep(step - 1)} className="flex-1" size="lg">
              ← Back
            </Button>
          )}
          <Button type="submit" className="flex-1" size="lg" disabled={loading}>
            {loading ? <><Loader2 className="w-4 h-4 animate-spin" /> Creating...</> : step < 2 ? "Continue →" : "Create workspace →"}
          </Button>
        </div>
      </form>

      <p className="text-center text-xs text-slate-400 mt-6">
        By creating an account you agree to our <Link href="#" className="underline">Terms</Link> and <Link href="#" className="underline">Privacy Policy</Link>.
      </p>
    </div>
  );
}


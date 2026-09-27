"use client";

import { FormEvent, useState } from "react";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export default function Home() {
  const [url, setUrl] = useState("");
  const [status, setStatus] = useState("");

  async function submit(event: FormEvent) {
    event.preventDefault();
    setStatus("Submitting...");
    try {
      const response = await fetch(API + "/api/v1/videos", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ source_url: url }),
      });
      const data = await response.json();
      setStatus(data.status === "queued" ? "Job queued." : JSON.stringify(data));
    } catch {
      setStatus("Could not reach the API.");
    }
  }

  return (
    <main style={{ maxWidth: 760, margin: "80px auto", padding: 24, fontFamily: "system-ui" }}>
      <p>AI Shorts Studio</p>
      <h1>Turn authorized videos into ready-to-publish shorts.</h1>
      <p>Paste a source URL to start the processing pipeline.</p>
      <form onSubmit={submit} style={{ display: "flex", gap: 12, marginTop: 32 }}>
        <input
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://..."
          required
          style={{ flex: 1, padding: 14 }}
        />
        <button type="submit" style={{ padding: "14px 20px" }}>Generate</button>
      </form>
      {status && <p style={{ marginTop: 20 }}>{status}</p>}
    </main>
  );
}

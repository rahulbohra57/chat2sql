"use client";

import { useState, useRef } from "react";
import { askDatabase, type QueryResponse } from "@/lib/api";
import ResultsTable from "./ResultsTable";
import ChartView from "./ChartView";

interface ChatBoxProps {
  selectedSchema: string | null;
}

export default function ChatBox({ selectedSchema }: ChatBoxProps) {
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState<QueryResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const abortControllerRef = useRef<AbortController | null>(null);

  async function handleAsk() {
    if (!question.trim()) return;

    abortControllerRef.current = new AbortController();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await askDatabase(question, selectedSchema, abortControllerRef.current.signal);
      setResult(data);
    } catch (err: unknown) {
      if (err instanceof Error && err.name === "AbortError") {
        setError("Query cancelled.");
      } else {
        setError(err instanceof Error ? err.message : "An unexpected error occurred.");
      }
    } finally {
      setLoading(false);
      abortControllerRef.current = null;
    }
  }

  function handleStop() {
    abortControllerRef.current?.abort();
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLInputElement>) {
    if (e.key === "Enter" && !loading) handleAsk();
  }

  return (
    <div>
      <div className="chat-box">
        <h2>
          Ask your database
          {selectedSchema && (
            <span className="schema-badge">{selectedSchema}</span>
          )}
        </h2>
        <div className="input-row">
          <input
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="e.g. Show top 5 employees by salary"
            disabled={loading}
          />
          {loading ? (
            <button className="stop-btn" onClick={handleStop}>
              Stop
            </button>
          ) : (
            <button onClick={handleAsk} disabled={!question.trim()}>
              Ask
            </button>
          )}
        </div>
        {loading && <p className="thinking-text">Thinking...</p>}
        {error && <div className="error-box">{error}</div>}
      </div>

      {result && (
        <>
          <ResultsTable data={result.data} />

          {result.chart && <ChartView chart={result.chart} />}

          <div className="sql-block">
            <h2>Generated SQL</h2>
            <pre>{result.sql}</pre>
          </div>
        </>
      )}
    </div>
  );
}

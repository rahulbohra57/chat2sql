"use client";

import { useState, useEffect } from "react";
import { getSchemas, type SchemaInfo } from "@/lib/api";
import ChatBox from "./components/ChatBox";
import SchemaPanel from "./components/SchemaPanel";
import LoginScreen from "./components/LoginScreen";

export default function Home() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [schemas, setSchemas] = useState<SchemaInfo[]>([]);
  const [selectedSchema, setSelectedSchema] = useState<string | null>(null);
  const [schemaError, setSchemaError] = useState<string | null>(null);

  useEffect(() => {
    if (!loggedIn) return;
    getSchemas()
      .then(setSchemas)
      .catch(() => setSchemaError("Could not load schema — is the backend running?"));
  }, [loggedIn]);

  if (!loggedIn) {
    return <LoginScreen onLogin={() => setLoggedIn(true)} />;
  }

  return (
    <div className="app-layout">
      <header className="app-header">
        <h1>AI SQL Analyst</h1>
        <p>Ask questions about your database in plain English.</p>
      </header>

      <div className="app-body">
        <SchemaPanel
          schemas={schemas}
          selectedSchema={selectedSchema}
          onSelectSchema={setSelectedSchema}
        />

        <main className="main-content">
          {schemaError && <div className="error-box">{schemaError}</div>}
          <ChatBox selectedSchema={selectedSchema} />
        </main>
      </div>
    </div>
  );
}

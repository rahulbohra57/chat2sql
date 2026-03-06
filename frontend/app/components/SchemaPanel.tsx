"use client";

import { useState } from "react";
import type { SchemaInfo } from "@/lib/api";

interface SchemaPanelProps {
  schemas: SchemaInfo[];
  selectedSchema: string | null;
  onSelectSchema: (schema: string | null) => void;
}

export default function SchemaPanel({
  schemas,
  selectedSchema,
  onSelectSchema,
}: SchemaPanelProps) {
  const [expandedTables, setExpandedTables] = useState<Set<string>>(new Set());

  function toggleTable(key: string) {
    setExpandedTables((prev) => {
      const next = new Set(prev);
      next.has(key) ? next.delete(key) : next.add(key);
      return next;
    });
  }

  return (
    <aside className="schema-panel">
      <div className="schema-panel-header">
        <h2>Database</h2>
      </div>

      <div className="schema-selector">
        <label>Query scope</label>
        <select
          value={selectedSchema ?? ""}
          onChange={(e) => onSelectSchema(e.target.value || null)}
        >
          <option value="">All schemas</option>
          {schemas.map((s) => (
            <option key={s.name} value={s.name}>
              {s.name}
            </option>
          ))}
        </select>
      </div>

      <div className="schema-tree">
        {schemas
          .filter((s) => !selectedSchema || s.name === selectedSchema)
          .map((schema) => (
            <div key={schema.name} className="schema-group">
              <div className="schema-name">{schema.name}</div>
              {schema.tables.map((table) => {
                const key = `${schema.name}.${table.name}`;
                const open = expandedTables.has(key);
                return (
                  <div key={key} className="table-item">
                    <button
                      className="table-name"
                      onClick={() => toggleTable(key)}
                    >
                      <span className="table-icon">{open ? "▾" : "▸"}</span>
                      {table.name}
                      <span className="col-count">{table.columns.length}</span>
                    </button>
                    {open && (
                      <ul className="column-list">
                        {table.columns.map((col) => (
                          <li key={col.name}>
                            <span className="col-name">{col.name}</span>
                            <span className="col-type">{col.type}</span>
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                );
              })}
            </div>
          ))}
      </div>
    </aside>
  );
}

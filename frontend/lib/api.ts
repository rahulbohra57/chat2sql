const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface ChartData {
  type: string;
  label_column: string;
  value_column: string;
  labels: string[];
  values: number[];
}

export interface QueryResponse {
  sql: string;
  data: Record<string, unknown>[];
  chart: ChartData | null;
  error: string | null;
}

export interface ColumnInfo {
  name: string;
  type: string;
}

export interface TableInfo {
  name: string;
  columns: ColumnInfo[];
}

export interface SchemaInfo {
  name: string;
  tables: TableInfo[];
}

export async function getSchemas(): Promise<SchemaInfo[]> {
  const res = await fetch(`${API_URL}/schemas`);
  if (!res.ok) throw new Error("Failed to load schema");
  const data = await res.json();
  return data.schemas;
}

export async function askDatabase(
  question: string,
  schema: string | null
): Promise<QueryResponse> {
  const res = await fetch(`${API_URL}/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, schema }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || `Request failed with status ${res.status}`);
  }

  return res.json();
}

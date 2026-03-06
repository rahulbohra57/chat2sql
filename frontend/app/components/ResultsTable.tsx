interface ResultsTableProps {
  data: Record<string, unknown>[];
}

export default function ResultsTable({ data }: ResultsTableProps) {
  if (!data || data.length === 0) {
    return <p className="no-results">No results returned.</p>;
  }

  const columns = Object.keys(data[0]);

  return (
    <div className="results-table-wrap">
      <h2>Results ({data.length} rows)</h2>
      <table>
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={col}>{col}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, i) => (
            <tr key={i}>
              {columns.map((col) => (
                <td key={col}>{String(row[col] ?? "")}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

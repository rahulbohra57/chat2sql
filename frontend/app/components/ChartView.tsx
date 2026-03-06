"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import type { ChartData } from "@/lib/api";

interface ChartViewProps {
  chart: ChartData;
}

export default function ChartView({ chart }: ChartViewProps) {
  const chartData = chart.labels.map((label, i) => ({
    name: label,
    value: chart.values[i],
  }));

  return (
    <div className="chart-wrap">
      <h2>
        {chart.value_column} by {chart.label_column}
      </h2>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData} margin={{ top: 10, right: 20, left: 0, bottom: 60 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" angle={-30} textAnchor="end" interval={0} />
          <YAxis />
          <Tooltip />
          <Bar dataKey="value" fill="#6366f1" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

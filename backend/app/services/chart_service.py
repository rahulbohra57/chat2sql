from typing import Any


def suggest_chart(data: list[dict[str, Any]]) -> dict[str, Any] | None:
    """
    Inspect query results and return a chart config if the data is chart-able.
    Returns a bar chart config when there are exactly 2 columns where the
    second column is numeric.  Returns None otherwise.
    """
    if not data or len(data[0]) < 2:
        return None

    columns = list(data[0].keys())
    label_col = columns[0]
    value_col = columns[1]

    # Check that the value column contains numeric data
    sample_value = data[0][value_col]
    if not isinstance(sample_value, (int, float)):
        try:
            float(sample_value)
        except (TypeError, ValueError):
            return None

    labels = [str(row[label_col]) for row in data]
    values = [float(row[value_col]) for row in data]

    return {
        "type": "bar",
        "label_column": label_col,
        "value_column": value_col,
        "labels": labels,
        "values": values,
    }

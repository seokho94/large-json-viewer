# viewer/parser.py

import pandas as pd
import json

# resourceMetrics → resource.attributes 및 metric.dataPoints까지 평탄화
def flatten_metrics_data(file):
    content = file.read().decode("utf-8")
    file.seek(0)  # 이후 재사용을 위해 포인터 초기화

    try:
        raw = json.loads(content)
    except json.JSONDecodeError:
        raise ValueError("유효하지 않은 JSON 형식입니다.")

    resource_metrics = raw.get("resourceMetrics", [])
    rows = []

    for resource_entry in resource_metrics:
        base = {}

        # 1. resource.attributes → base dict 구성
        attributes = resource_entry.get("resource", {}).get("attributes", [])
        for attr in attributes:
            key = attr.get("key")
            value_obj = attr.get("value", {})
            if "stringValue" in value_obj:
                base[key] = value_obj["stringValue"]
            elif "intValue" in value_obj:
                base[key] = value_obj["intValue"]
            elif "arrayValue" in value_obj:
                base[key] = ", ".join(
                    v.get("stringValue", "") for v in value_obj["arrayValue"].get("values", [])
                )
            else:
                base[key] = str(value_obj)

        # 2. scopeMetrics.metrics[].dataPoints[] 순회
        for scope in resource_entry.get("scopeMetrics", []):
            for metric in scope.get("metrics", []):
                metric_name = metric.get("name", "")
                metric_type = "sum" if "sum" in metric else "gauge"
                points = metric.get(metric_type, {}).get("dataPoints", [])

                for point in points:
                    row = base.copy()
                    row["metric_name"] = metric_name
                    row["metric_type"] = metric_type
                    row["start_time"] = point.get("startTimeUnixNano")
                    row["end_time"] = point.get("timeUnixNano")
                    row["value"] = point.get("asInt") or point.get("asDouble") or 0

                    for attr in point.get("attributes", []):
                        row[attr["key"]] = attr["value"].get("stringValue", "")

                    rows.append(row)

    return pd.DataFrame(rows)

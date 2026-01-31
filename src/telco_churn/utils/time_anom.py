# utils/time_anomaly.py

# temporal_checks (2.3.7)

def detect_global_temporal_anomalies(df, time_col, numeric_cols, freq="M", z_thresh=3.0):
    """
    Detect global temporal anomalies across multiple numeric metrics.
    Aggregates all numeric columns per time bucket and computes overall z-scores.
    """
    ts = df.copy()
    ts[time_col] = pd.to_datetime(ts[time_col], errors="coerce")
    ts = ts.dropna(subset=[time_col]).sort_values(time_col).set_index(time_col)

    agg = ts[numeric_cols].resample(freq).mean()
    agg["row_count"] = ts.resample(freq)[numeric_cols[0]].count()

    # Option 1 — compute a global “health index” per bucket
    agg["mean_zscore"] = (
        (agg[numeric_cols] - agg[numeric_cols].mean()) / agg[numeric_cols].std(ddof=0)
    ).abs().mean(axis=1)

    anomalies = agg[agg["mean_zscore"] > z_thresh]
    return anomalies

# Then in notebook:
from utils.time_anomaly import detect_global_temporal_anomalies

anom_global = detect_global_temporal_anomalies(df, time_col="BeginDate", numeric_cols=continuous_cols)
display(anom_global)

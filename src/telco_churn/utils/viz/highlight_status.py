def highlight_status(row):
    status = str(row.get("status", "")).upper()
    if status == "FAIL":
        return ["background-color: #ffcccc"] * len(row)
    if status == "WARN":
        return ["background-color: #fff3cd"] * len(row)
    return [""] * len(row)

styled = (
    sec2_diagnostics_df
    .style
    .apply(highlight_status, axis=1)
    .format(na_rep="—")
)

display(styled)

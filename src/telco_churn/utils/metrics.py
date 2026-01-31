# metric_utils.py

# Place in notebook:
# from telco_churn.utils.metrics_utils import summarize_append_refactor

from __future__ import annotations

def summarize_append_refactor(
    n_sections: int,
    old_block_lines: int = 37,
    call_lines: int = 1,
    helper_lines: int = 45,
) -> dict:
    """
    Estimate how much code you save by replacing repeated inline
    CSV append blocks with a shared append_sec2 helper.
    """
    before_loc = n_sections * old_block_lines
    after_loc = n_sections * call_lines + helper_lines

    loc_saved = before_loc - after_loc
    pct_reduction = (loc_saved / before_loc * 100.0) if before_loc else 0.0

    summary = {
        "n_sections":     n_sections,
        "before_loc":     before_loc,
        "after_loc":      after_loc,
        "loc_saved":      loc_saved,
        "pct_reduction":  round(pct_reduction, 2),
        "helper_lines":   helper_lines,
        "old_block_lines": old_block_lines,
        "call_lines":     call_lines,
    }

    print("📉 Refactor savings estimate (append_sec2):")
    for k, v in summary.items():
        print(f"  {k}: {v}")

    return summary


#    # DEPRECATED v1
    # def summarize_append_refactor(
    #     n_sections: int,
    #     old_block_lines: int = 37,  # rough count of your inline block
    #     call_lines: int = 1,        # lines per section for append_sec2(...)
    #     helper_lines: int = 45,     # size of append_sec2 definition in reporting.py
    # ) -> dict:
    #     """
    #     Estimate how much code you save by replacing repeated inline
    #     CSV append blocks with a shared append_sec2 helper.

    #     Returns a dict with:
    #     - before_loc: total LOC for the old pattern
    #     - after_loc:  total LOC for the new pattern (calls + helper)
    #     - loc_saved:  net lines removed
    #     - pct_reduction: percent reduction in LOC
    #     """
    #     # "Before": every section has the full inline block, no helper
    #     before_loc = n_sections * old_block_lines

    #     # "After": each section has a one-line call + we pay the helper once
    #     after_loc = n_sections * call_lines + helper_lines

    #     loc_saved = before_loc - after_loc
    #     pct_reduction = (loc_saved / before_loc * 100.0) if before_loc else 0.0

    #     summary = {
    #         "n_sections":     n_sections,
    #         "before_loc":     before_loc,
    #         "after_loc":      after_loc,
    #         "loc_saved":      loc_saved,
    #         "pct_reduction":  round(pct_reduction, 2),
    #         "helper_lines":   helper_lines,
    #         "old_block_lines": old_block_lines,
    #         "call_lines":     call_lines,
    #     }

    #     print("📉 Refactor savings estimate (append_sec2):")
    #     for k, v in summary.items():
    #         print(f"  {k}: {v}")

    #     return summary

# src/telco_churn/lineage.py
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
import pandas as pd
import numpy as np
import hashlib
import time

@dataclass
class DFNode:
    node_id: str           # unique id for the node (e.g. "step_2.3.1_df_profiled")
    name: str              # friendly name (e.g. "df_profiled")
    step: str              # section/step id (e.g. "2.3.1")
    description: str       # what this step did
    parents: List[str]     # list of parent node_ids
    n_rows: int
    n_cols: int
    cols_added: List[str]
    cols_removed: List[str]
    timestamp: float       # time when registered (for ordering)
    sample_hash: str       # hash of a small sample for “shape-of-data” fingerprint

class DFLineageRegistry:
    def __init__(self):
        self.nodes: Dict[str, DFNode] = {}
        self.last_node_for_dfname: Dict[str, str] = {}  # df_name -> node_id

    def _hash_sample(self, df: pd.DataFrame, n: int = 10) -> str:
        if df.empty:
            return "empty"
        sample = df.head(n).to_json(orient="split", default_handler=str)
        return hashlib.md5(sample.encode("utf-8")).hexdigest()

    def register(
        self,
        df: pd.DataFrame,
        df_name: str,
        step: str,
        description: str = "",
        parents: Optional[List[str]] = None,
    ) -> str:
        """Register a new DF state and return its node_id."""
        if parents is None:
            parents = []

        # infer parents from last node of this df_name if none provided
        if not parents and df_name in self.last_node_for_dfname:
            parents = [self.last_node_for_dfname[df_name]]

        node_id = f"{step}_{df_name}"

        # column diffs vs first parent (if any)
        cols = list(df.columns)
        cols_added, cols_removed = [], []
        if parents:
            parent_node = self.nodes[parents[0]]
            parent_cols = set(parent_node.cols_added) | set(parent_node.cols_removed) \
                          if False else set()  # we’ll recompute from df sample
            # simpler: use parent snapshot stored in registry? (future enhancement)
        # for now: we’ll compute added/removed by storing the parent’s column set separately:
        # to keep it simple, we won’t use that trick here – just leave cols_added/removed',
        # or fill them in manually later if you want.

        n_rows = int(df.shape[0])
        n_cols = int(df.shape[1])

        node = DFNode(
            node_id=node_id,
            name=df_name,
            step=step,
            description=description,
            parents=parents,
            n_rows=n_rows,
            n_cols=n_cols,
            cols_added=cols_added,
            cols_removed=cols_removed,
            timestamp=time.time(),
            sample_hash=self._hash_sample(df),
        )

        self.nodes[node_id] = node
        self.last_node_for_dfname[df_name] = node_id
        return node_id

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame([asdict(n) for n in self.nodes.values()])


# telco_churn/lineage_auto.py

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Iterable, Callable
import pandas as pd
import numpy as np  # noqa: F401  # might be handy later
import hashlib
import time

try:
    from graphviz import Digraph
except ImportError:
    Digraph = None  # graceful fallback


# -------------------------------------------------------------------
# Core data structure: one node = one snapshot of a df-like variable
# -------------------------------------------------------------------
@dataclass
class DFNode:
    node_id: str           # unique id: f"{step}:{df_name}"
    df_name: str           # variable name: "df", "df_clean", "df_before_clean", etc.
    step: str              # pipeline step: "2.0.0", "2.3.14", "2.6.10", ...
    description: str       # human text of what we did
    parents: List[str]     # node_ids of parents
    n_rows: int
    n_cols: int
    columns: List[str]
    cols_added: List[str]
    cols_removed: List[str]
    timestamp: float       # time.time()
    sample_hash: str       # md5 of small JSON sample for "shape" fingerprint


class DFLineageRegistry:
    """
    Registry that tracks df-like variables across steps.
    You don't touch this directly much; you'll mostly call register_step().
    """

    def __init__(self):
        self.nodes: Dict[str, DFNode] = {}
        self.last_node_for_dfname: Dict[str, str] = {}
        self._columns_for_node: Dict[str, List[str]] = {}

    # ------------- internals ------------- #

    def _hash_sample(self, df: pd.DataFrame, n: int = 10) -> str:
        if df is None or getattr(df, "empty", False):
            return "empty"
        try:
            sample = df.head(n).to_json(orient="split", default_handler=str)
        except Exception:
            sample = "unhashable"
        return hashlib.md5(sample.encode("utf-8")).hexdigest()

    def _compute_col_diff(
        self,
        current_cols: Iterable[str],
        parent_node_id: Optional[str],
    ) -> (List[str], List[str]):
        current_cols = list(current_cols)
        if not parent_node_id or parent_node_id not in self._columns_for_node:
            # No parent info: can't diff; treat everything as "existing" not "added"
            return [], []
        parent_cols = set(self._columns_for_node[parent_node_id])
        curr_cols_set = set(current_cols)
        cols_added = sorted(list(curr_cols_set - parent_cols))
        cols_removed = sorted(list(parent_cols - curr_cols_set))
        return cols_added, cols_removed

    # ------------- public methods ------------- #

    def register_df(
        self,
        df: pd.DataFrame,
        df_name: str,
        step: str,
        description: str = "",
        parents: Optional[List[str]] = None,
    ) -> str:
        """
        Register a single df snapshot.

        Returns
        -------
        node_id : str
            The ID of the created node (e.g. "2.3.14:df_clean").
        """
        if parents is None:
            parents = []

        # If parents not explicitly set, infer from last node of same df_name
        if not parents and df_name in self.last_node_for_dfname:
            parents = [self.last_node_for_dfname[df_name]]

        node_id = f"{step}:{df_name}"

        # Basic shape
        n_rows = int(df.shape[0])
        n_cols = int(df.shape[1])
        cols = list(map(str, df.columns))

        # Column diff vs first parent (if any)
        parent_id = parents[0] if parents else None
        cols_added, cols_removed = self._compute_col_diff(cols, parent_id)

        node = DFNode(
            node_id=node_id,
            df_name=df_name,
            step=step,
            description=description,
            parents=parents,
            n_rows=n_rows,
            n_cols=n_cols,
            columns=cols,
            cols_added=cols_added,
            cols_removed=cols_removed,
            timestamp=time.time(),
            sample_hash=self._hash_sample(df),
        )

        self.nodes[node_id] = node
        self.last_node_for_dfname[df_name] = node_id
        self._columns_for_node[node_id] = cols
        return node_id

    def register_step(
        self,
        namespace: Dict[str, object],
        step: str,
        description: str = "",
        name_filter: Optional[Callable[[str], bool]] = None,
    ) -> List[str]:
        """
        Auto-register all df-like variables in a given namespace
        (e.g. globals()) for a given pipeline step.

        Parameters
        ----------
        namespace : dict
            Usually globals() from your notebook cell.
        step : str
            Step identifier like "2.3.14" or "2.6.10".
        description : str
            Human text for this step (what it represents).
        name_filter : callable or None
            Function name -> bool. If None, defaults to variables whose names
            start with "df" (df, df_clean, df_before_clean, df_num_profile, etc.).

        Returns
        -------
        node_ids : list of str
            Node IDs registered for this step.
        """
        if name_filter is None:
            def name_filter(n: str) -> bool:
                return n.startswith("df")

        node_ids: List[str] = []
        for name, value in namespace.items():
            if not name_filter(name):
                continue
            # Only track pandas DataFrame objects
            if isinstance(value, pd.DataFrame):
                node_id = self.register_df(
                    df=value,
                    df_name=name,
                    step=step,
                    description=description,
                )
                node_ids.append(node_id)
        return node_ids

    # ----------- export helpers ----------- #
    def to_dataframe(self) -> pd.DataFrame:
        if not self.nodes:
            return pd.DataFrame(columns=[
                "node_id", "df_name", "step", "description",
                "parents", "n_rows", "n_cols",
                "columns", "cols_added", "cols_removed",
                "timestamp", "sample_hash",
            ])
        return pd.DataFrame([asdict(n) for n in self.nodes.values()])

    # def build_graph(self, rankdir: str = "TB") -> "Digraph":
    #     """
    #     Build a Graphviz Digraph representing the lineage graph,
    #     styled to look more like pipes than arrows.
    #     """
    #     if Digraph is None:
    #         raise ImportError(
    #             "graphviz is not installed. `pip install graphviz` "
    #             "and make sure Graphviz binaries are available."
    #         )

    #     dot = Digraph(comment="DQ Pipeline Lineage")

    #     # Left-to-right = pipe layout
    #     dot.attr(rankdir=rankdir)

    #     # Global graph style: orthogonal splines looks more like plumbing
    #     dot.attr(splines="ortho")

        # # Nodes = junction boxes in the pipe
        # dot.attr(
        #     "node",
        #     shape="box",
        #     style="rounded,filled",
        #     penwidth="0.5",             # pipe width
        # )

        # # Edges = pipes
        # dot.attr(
        #     "edge",
        #     arrowhead="none",   # 🚫 no arrow tip
        #     arrowsize="0.0",
        #     penwidth="4",       # thicker line = pipe
        # )

        # # Node colors by phase for quick reading                        # COLOR PALETTE #
        # def color_for_step(step: str) -> str:                           # cfe2ff
        #     if step.startswith(("2.0", "2.1", "2.2")):
        #         return "#cfe2ff"  # ingestion/schema
        #     if step.startswith(("2.3", "2.4", "2.5")):
        #         return "#ffe5b4"  # diagnostics
        #     if step.startswith("2.6"):
        #         return "#d3f9d8"  # cleaning/apply
        #     return "#e2e3e5"      # default/other

        # Add nodes V1
            # for node in self.nodes.values():
            #     label = (
            #         f"{node.step}\\n"
            #         f"{node.df_name}\\n"
            #         f"rows={node.n_rows}, cols={node.n_cols}"
            #     )
            #     dot.node(
            #         node.node_id,
            #         label=label,
            #         fillcolor=color_for_step(node.step),
            #     )

        # add nodes V2
        # for node in self.nodes.values():
        #     label = f"{node.step}\\n{node.df_name}"
        #     dot.node(
        #         node.node_id,
        #         label=label,
        #         fillcolor=color_for_step(node.step),
            )

        # V2
        # for node in self.nodes.values():
            #     for parent_id in node.parents:
            #         if parent_id in self.nodes:
            #             # Add a tiny circular valve in the middle
            #             valve_id = f"valve_{parent_id}_to_{node.node_id}"
            #             dot.node(
            #                 valve_id,
            #                 label="",
            #                 shape="circle",
            #                 width="0.15",
            #                 height="0.15",
            #                 style="filled",
            #                 fillcolor="#999999",
            #             )
            #             dot.edge(parent_id, valve_id)
            #             dot.edge(valve_id, node.node_id)

        # V1 Add "pipe" edges between nodes
        # for node in self.nodes.values():
        #     for parent_id in node.parents:
        #         if parent_id in self.nodes:
        #             dot.edge(parent_id, node.node_id)

        # # ----------------------------------------------------------
        # # Focused "pipe view" for a single dataframe name (df_clean)
        # # ----------------------------------------------------------
        # def _collect_subgraph_for_df(self, df_name: str) -> Dict[str, DFNode]:
        #     """
        #     Collect all nodes and their ancestors for a specific df_name.
        #     Returns a dict node_id -> DFNode for the subgraph.
        #     """
        #     # Nodes that match this df_name
        #     target_nodes = [n for n in self.nodes.values() if n.df_name == df_name]
        #     if not target_nodes:
        #         return {}

        #     subgraph_nodes: Dict[str, DFNode] = {}

        #     # DFS up the parent chain for all matching nodes
        #     stack = [n.node_id for n in target_nodes]
        #     while stack:
        #         node_id = stack.pop()
        #         if node_id in subgraph_nodes:
        #             continue
        #         node = self.nodes[node_id]
        #         subgraph_nodes[node_id] = node
        #         for parent_id in node.parents:
        #             if parent_id in self.nodes and parent_id not in subgraph_nodes:
        #                 stack.append(parent_id)

        #     return subgraph_nodes

        # def build_graph_for_df(self, df_name: str, rankdir: str = "LR") -> "Digraph":
        #     """
        #     Build a Graphviz graph that shows only the lineage pipes
        #     for nodes where df_name == <df_name> and their ancestors.
        #     """
        #     if Digraph is None:
        #         raise ImportError(
        #             "graphviz is not installed. `pip install graphviz` "
        #             "and make sure Graphviz binaries are available."
        #         )

        #     sub_nodes = self._collect_subgraph_for_df(df_name)
        #     if not sub_nodes:
        #         raise ValueError(f"No lineage nodes found for df_name='{df_name}'")

        #     dot = Digraph(comment=f"DQ Pipeline Lineage – {df_name}")
        #     dot.attr(rankdir=rankdir)
        #     dot.attr(splines="ortho")

        #     dot.attr(
        #         "node",
        #         shape="box",
        #         style="rounded,filled",
        #         penwidth="1.5",
        #     )
        #     dot.attr(
        #         "edge",
        #         arrowhead="none",
        #         arrowsize="0.0",
        #         penwidth="4",
        #     )

        #     def color_for_step(step: str) -> str:
        #         if step.startswith(("2.0", "2.1", "2.2")):
        #             return "#cfe2ff"  # ingestion/schema
        #         if step.startswith(("2.3", "2.4", "2.5")):
        #             return "#ffe5b4"  # diagnostics
        #         if step.startswith("2.6"):
        #             return "#d3f9d8"  # cleaning/apply
        #         return "#e2e3e5"      # default/other

        #     # Add nodes
        #     for node in sub_nodes.values():
        #         label = (
        #             f"{node.step}\\n"
        #             f"{node.df_name}\\n"
        #             f"rows={node.n_rows}, cols={node.n_cols}"
        #         )
        #         dot.node(
        #             node.node_id,
        #             label=label,
        #             fillcolor=color_for_step(node.step),
        #         )

        #     # Add edges ("pipes")
        #     for node in sub_nodes.values():
        #         for parent_id in node.parents:
        #             if parent_id in sub_nodes:
        #                 dot.edge(parent_id, node.node_id)

        #     return dot

        # def view_pipes(self, df_name: str = "df_clean", rankdir: str = "LR") -> "Digraph":
        #     """
        #     Convenience wrapper for notebooks: show the pipe network for one df.
        #     Usage:
        #         LINEAGE.view_pipes("df_clean")
        #     """
        #     return self.build_graph_for_df(df_name=df_name, rankdir=rankdir)
        # return dot

    # V1 def build_graph
        # def build_graph(self, rankdir: str = "LR") -> "Digraph":
        #     """
        #     Build a Graphviz Digraph representing the lineage graph.

        #     rankdir:
        #         "LR" = left-to-right (pipe-like),
        #         "TB" = top-to-bottom, etc.
        #     """
        #     if Digraph is None:
        #         raise ImportError(
        #             "graphviz is not installed. `pip install graphviz` "
        #             "and make sure Graphviz binaries are available."
        #         )

        #     dot = Digraph(comment="DQ Pipeline Lineage")
        #     dot.attr(rankdir=rankdir)
        #     dot.attr("node", shape="box", style="rounded,filled", penwidth="1.5")
        #     dot.attr("edge", penwidth="1.5")

        #     # Node colors by phase for plumber-y vibe
        #     def color_for_step(step: str) -> str:
        #         if step.startswith("2.0") or step.startswith("2.1") or step.startswith("2.2"):
        #             return "#cfe2ff"  # ingestion/schema
        #         if step.startswith("2.3") or step.startswith("2.4") or step.startswith("2.5"):
        #             return "#ffe5b4"  # diagnostics
        #         if step.startswith("2.6"):
        #             return "#d3f9d8"  # cleaning/apply
        #         return "#e2e3e5"      # default/other

        #     for node in self.nodes.values():
        #         label = (
        #             f"{node.step}\\n"
        #             f"{node.df_name}\\n"
        #             f"rows={node.n_rows}, cols={node.n_cols}"
        #         )
        #         dot.node(
        #             node.node_id,
        #             label=label,
        #             fillcolor=color_for_step(node.step),
        #         )

        #     for node in self.nodes.values():
        #         for parent_id in node.parents:
        #             if parent_id in self.nodes:
        #                 dot.edge(parent_id, node.node_id)

        #     return dot


# Global singleton you can import & use everywhere
LINEAGE = DFLineageRegistry()

"""One Plotly chart and period controls consuming saved, loaded results only."""

from datetime import date

import ipywidgets as widgets
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from IPython.display import clear_output
from plotly.subplots import make_subplots


def common_available_range(results):
    """Default dates use the exact shared available observation dates."""
    shared = None
    for _, rows in results.groupby("duration_exposure", sort=False):
        dates = set(rows.loc[rows["core_availability"].eq("available"), "date"])
        shared = dates if shared is None else shared & dates
    if not shared:
        return None, None
    return min(shared).date(), max(shared).date()


def create_chart(results, exposure="Intermediate", start=None, end=None):
    """Filter loaded rows and present their saved values; perform no analytics."""
    rows = results.loc[results["duration_exposure"].eq(exposure)].copy()
    if rows.empty:
        raise ValueError(f"Unknown Duration Exposure: {exposure}")
    tenor = rows["representative_tenor"].iloc[0]
    if start is not None:
        rows = rows.loc[rows["date"] >= pd.Timestamp(start)]
    if end is not None:
        rows = rows.loc[rows["date"] <= pd.Timestamp(end)]
    # Explicit separators also protect extracts that omit structural gap rows.
    rows = rows.reset_index(drop=True)
    segments = rows["segment"].dropna()
    boundaries = segments.index[segments.ne(segments.shift()).fillna(False)]
    pieces, cursor = [], 0
    for position in boundaries:
        pieces.append(rows.iloc[cursor:position])
        separator = rows.iloc[[position]].copy()
        separator["yield_pct"] = np.nan
        separator["core_score"] = pd.Series(pd.NA, index=separator.index, dtype="Int64")
        pieces.append(separator)
        cursor = position
    pieces.append(rows.iloc[cursor:])
    plotted = pd.concat(pieces, ignore_index=True)
    custom_columns = ["yield_pct", "trend_value_bp", "trend_state", "recent_move_value_bp",
                      "recent_move_state", "rule_case", "core_score"]
    customdata = plotted[custom_columns].astype(object).where(plotted[custom_columns].notna(), None).to_numpy()

    # Show the Component details once, on the yield trace. The score trace shows
    # only its own ordinal value in the unified hover. Format missing values as
    # N/A instead of passing nulls through numeric Plotly format specifiers.
    def component_text(value, state):
        if pd.isna(value) or pd.isna(state):
            return "N/A"
        return f"{float(value):+.2f} bp ({state})"

    hover_details = [
        (f"Trend: {component_text(trend, trend_state)}<br>"
         f"Recent Move: {component_text(move, move_state)}<br>"
         f"Rule Case: {case if pd.notna(case) else 'N/A'}")
        for trend, trend_state, move, move_state, case in zip(
            plotted["trend_value_bp"], plotted["trend_state"],
            plotted["recent_move_value_bp"], plotted["recent_move_state"],
            plotted["rule_case"])
    ]

    figure = make_subplots(specs=[[{"secondary_y": True}]])
    figure.add_trace(go.Scatter(x=plotted["date"], y=plotted["yield_pct"].astype(float),
                               name="Treasury yield", mode="lines", connectgaps=False,
                               customdata=customdata, text=hover_details,
                               hovertemplate="Treasury yield: %{y:.2f}%<br>%{text}<extra></extra>",
                               line={"color": "#2563eb"}), secondary_y=False)
    figure.add_trace(go.Scatter(x=plotted["date"], y=plotted["core_score"].astype(float),
                               name="Core Duration score", mode="lines", connectgaps=False,
                               hovertemplate="Core score: %{y:.0f}<extra></extra>",
                               line={"shape": "hv", "color": "#b45309"}), secondary_y=True)
    figure.update_yaxes(title_text="Treasury yield (%)", secondary_y=False)
    figure.update_yaxes(title_text="Core Duration score (ordinal)", tickmode="array",
                        tickvals=list(range(-3, 4)), range=[-3.3, 3.3], secondary_y=True)
    figure.add_hline(y=0, line_dash="dot", line_color="#888888", secondary_y=True)
    figure.update_layout(title=f"Duration Core — {exposure} / {tenor}",
                         hovermode="x unified", template="plotly_white", height=560,
                         legend={"orientation": "h", "y": 1.12})
    figure.update_xaxes(title_text="Date")
    if start is not None and end is not None and pd.Timestamp(start) <= pd.Timestamp(end):
        figure.update_xaxes(range=[pd.Timestamp(start), pd.Timestamp(end)])
    if rows.empty or rows["core_score"].notna().sum() == 0:
        figure.add_annotation(text="No completed Core results in this period", showarrow=False,
                              xref="paper", yref="paper", x=0.5, y=0.5)
    elif rows["core_score"].isna().any():
        figure.add_annotation(text="Gaps indicate unavailable observations or warmup", showarrow=False,
                              xref="paper", yref="paper", x=0, y=1.05)
    return figure


class DurationControls:
    """Notebook presentation state for exposure and historical period controls.

    Returning to Custom leaves the selected historical-event dates intact so
    users can extend the event window manually. No acquisition or calculation
    modules are imported.
    """

    def __init__(self, results, historical_events):
        self.results = results.copy(deep=True)
        # Chronological ordering is independent of YAML declaration order.
        self.events = dict(sorted(
            ((name, dict(window)) for name, window in historical_events.items()),
            key=lambda item: (item[1]["start"], item[1]["end"], item[0]),
        ))
        start, end = common_available_range(self.results)
        self._updating = False
        self.exposure = widgets.Dropdown(
            options=[(f"{name} / {rows['representative_tenor'].iloc[0]}", name)
                     for name, rows in self.results.groupby("duration_exposure", sort=False)],
            value="Intermediate", description="Exposure")
        self.period = widgets.Dropdown(options=["Custom period", *self.events],
                                       value="Custom period", description="Period")
        self.start = widgets.DatePicker(value=start, description="Start Date")
        self.end = widgets.DatePicker(value=end, description="End Date")
        self.output = widgets.Output()
        self.ui = widgets.VBox([widgets.HBox([self.exposure, self.period]),
                                widgets.HBox([self.start, self.end]), self.output])
        for control in (self.exposure, self.period, self.start, self.end):
            control.observe(self._on_change, names="value")

    def _on_change(self, change):
        if self._updating:
            return
        if change["owner"] is self.period:
            self._updating = True
            try:
                custom = self.period.value == "Custom period"
                self.start.disabled = self.end.disabled = not custom
                if not custom:
                    window = self.events[self.period.value]
                    self.start.value = date.fromisoformat(window["start"])
                    self.end.value = date.fromisoformat(window["end"])
                # Returning to Custom enables the current event dates, without
                # restoring any earlier manually selected range.
            finally:
                self._updating = False
        self.render()

    def figure(self):
        return create_chart(self.results, self.exposure.value, self.start.value, self.end.value)

    def render(self):
        with self.output:
            clear_output(wait=True)
            if self.start.value is None or self.end.value is None:
                print("Choose both dates. No common completed range may be available.")
            elif self.start.value > self.end.value:
                print("Start Date must be on or before End Date.")
            else:
                self.figure().show(renderer="plotly_mimetype")

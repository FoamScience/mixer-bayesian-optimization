#!/usr/bin/env python3

# DISCLAIMER: Largely generated with AI agents
# Tun with: python3 plot_pareto_frontier.py ./ThermalMixer_frontier_report.csv

import sys
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
from pathlib import Path

data = pd.read_csv(sys.argv[1])
fig = make_subplots(
    rows=2, cols=2,
    vertical_spacing=0.1,
    subplot_titles=("Mixing Quality vs Power Consumption",
                    "Mixing Quality vs Blade Durability",
                    "Power Consumption vs Blade Durability")
)

def plot_two_objs(data, obj_x, obj_y):
    hover_template = "<br>".join([f"{col}: %{{customdata[{i}]}}" for i, col in enumerate(data.columns)])
    sctr = go.Scatter(
        x=data[obj_x],
        y=data[obj_y],
        error_x=dict(type='data', array=data[f"{obj_x}_sems"]),
        error_y=dict(type='data', array=data[f"{obj_y}_sems"]),
        mode='markers',
        marker=dict(size=6),
        hovertemplate=hover_template,
        customdata=data.values
    )
    return sctr

fig.add_trace(
    plot_two_objs(data, "MixingQuality", "PowerConsumption"),
    row=1, col=1
)
fig.add_trace(
    plot_two_objs(data, "MixingQuality", "BladeDurability"),
    row=1, col=2
)
fig.add_trace(
    plot_two_objs(data, "PowerConsumption", "BladeDurability"),
    row=2, col=1
)

fig.update_xaxes(title_text="Mixing Quality", row=1, col=1)
fig.update_yaxes(title_text="Power Consumption", row=1, col=1)
fig.update_xaxes(title_text="Mixing Quality", row=1, col=2)
fig.update_yaxes(title_text="Blade Durability", row=1, col=2)
fig.update_xaxes(title_text="Power Consumption", row=2, col=1)
fig.update_yaxes(title_text="Blade Durability", row=2, col=1)

aspect_ratio = 4 / 3
subplot_width = 1200 
subplot_height = subplot_width * aspect_ratio
total_height = subplot_height * 2 + 200

fig.update_layout(
    height=1200,
    showlegend=False,
    title_text="Pareto Frontier"
)

pio.write_html(fig, file=f'./plots/{Path(sys.argv[1]).stem}.html', auto_open=True)
fig.show()

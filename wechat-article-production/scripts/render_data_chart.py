#!/usr/bin/env python3
"""Render WeChat-friendly data charts from CSV.

Example:
  python render_data_chart.py data.csv out.png --kind bar --x industry --y score \
    --title "AI 落地证据强度" --source "Source: editor scoring, 2026-06-21"
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import font_manager


def choose_cjk_font() -> str:
    preferred = [
        "Microsoft YaHei",
        "SimHei",
        "Noto Sans CJK SC",
        "Source Han Sans SC",
        "Arial Unicode MS",
        "DejaVu Sans",
    ]
    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in preferred:
        if name in available:
            return name
    return "DejaVu Sans"


def apply_style() -> None:
    plt.rcParams["font.family"] = choose_cjk_font()
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.facecolor"] = "#f7f4ea"
    plt.rcParams["axes.facecolor"] = "#ffffff"
    plt.rcParams["axes.edgecolor"] = "#d7dde2"
    plt.rcParams["axes.labelcolor"] = "#243746"
    plt.rcParams["xtick.color"] = "#52606d"
    plt.rcParams["ytick.color"] = "#52606d"
    plt.rcParams["grid.color"] = "#e7ecef"


def plot_chart(df: pd.DataFrame, args: argparse.Namespace) -> None:
    apply_style()
    fig, ax = plt.subplots(figsize=(12, 6.75), dpi=160)
    fig.subplots_adjust(left=0.1, right=0.96, top=0.82, bottom=0.18)

    palette = ["#2f7d80", "#d08b2e", "#4f6f9f", "#9a4c7d", "#6b8e23", "#34495e"]

    if args.kind == "bar":
        if args.series:
            pivot = df.pivot(index=args.x, columns=args.series, values=args.y)
            pivot.plot(kind="bar", ax=ax, color=palette[: len(pivot.columns)], width=0.72)
        else:
            ax.bar(df[args.x].astype(str), df[args.y], color=palette[0], width=0.62)
    elif args.kind == "line":
        if args.series:
            for i, (name, group) in enumerate(df.groupby(args.series)):
                ax.plot(group[args.x], group[args.y], marker="o", linewidth=2.8, label=str(name), color=palette[i % len(palette)])
        else:
            ax.plot(df[args.x], df[args.y], marker="o", linewidth=2.8, color=palette[0])
    elif args.kind == "scatter":
        if args.series:
            for i, (name, group) in enumerate(df.groupby(args.series)):
                ax.scatter(group[args.x], group[args.y], s=90, label=str(name), color=palette[i % len(palette)], alpha=0.85)
        else:
            ax.scatter(df[args.x], df[args.y], s=90, color=palette[0], alpha=0.85)
    elif args.kind == "hist":
        col = args.y or args.x
        ax.hist(df[col].dropna(), bins=args.bins, color=palette[0], alpha=0.85, edgecolor="#ffffff")
        ax.set_xlabel(args.xlabel or col)
    else:
        raise ValueError(f"Unsupported chart kind: {args.kind}")

    if args.kind != "hist":
        ax.set_xlabel(args.xlabel or args.x)
        ax.set_ylabel(args.ylabel or args.y)
    elif args.ylabel:
        ax.set_ylabel(args.ylabel)

    ax.grid(axis="y", linestyle="-", linewidth=1)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_title(args.title, loc="left", fontsize=22, fontweight="bold", color="#172634", pad=24)

    if args.subtitle:
        fig.text(0.1, 0.835, args.subtitle, fontsize=12, color="#52606d")
    if args.source:
        fig.text(0.1, 0.055, args.source, fontsize=10.5, color="#667783")
    if args.series:
        ax.legend(frameon=False, loc="best")

    plt.xticks(rotation=args.x_rotation, ha="right" if args.x_rotation else "center")
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, bbox_inches="tight", pad_inches=0.18)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a WeChat-friendly data chart from CSV.")
    parser.add_argument("csv", help="Input CSV path")
    parser.add_argument("output", help="Output PNG path")
    parser.add_argument("--kind", choices=["bar", "line", "scatter", "hist"], required=True)
    parser.add_argument("--x", required=True, help="X column, or histogram value column when --y is omitted")
    parser.add_argument("--y", help="Y column")
    parser.add_argument("--series", help="Optional grouping column")
    parser.add_argument("--title", required=True)
    parser.add_argument("--subtitle", default="")
    parser.add_argument("--source", default="")
    parser.add_argument("--xlabel", default="")
    parser.add_argument("--ylabel", default="")
    parser.add_argument("--bins", type=int, default=10)
    parser.add_argument("--x-rotation", type=int, default=0)
    args = parser.parse_args()

    if args.kind != "hist" and not args.y:
        parser.error("--y is required for bar, line, and scatter charts")

    df = pd.read_csv(args.csv)
    plot_chart(df, args)


if __name__ == "__main__":
    main()

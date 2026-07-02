""" 
Generic Helper Functions for creating Visualizations are present here.
"""

import matplotlib.pyplot as plt
import pandas as pd

def plot_metric_by_fold(
    metrics_df,
    metrics_col,
    title,
    ylabel,
    scale=1.0
):
    
    plot_df = (
        metrics_df
        .pivot(index="fold_id",columns="weight_method",values=metrics_col)
        .sort_index()
        *scale
    )
    
    ax = plot_df.plot(
        kind="bar",
        figsize=(10,5)
    )
    
    ax.axhline(0, linewidth=1)
    ax.set_title(title)
    ax.set_xlabel("Fold")
    ax.set_ylabel(ylabel)
    ax.legend(title="Weight Method", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

def plot_cumulative_returns_by_fold(returns_by_fold, title_prefix):
    for fold_id, returns_df in returns_by_fold.items():
        cumulative_returns_df = (1 + returns_df).cumprod() - 1

        ax = (cumulative_returns_df * 100).plot(figsize=(10, 5))
        ax.axhline(0, linewidth=1)

        plt.title(f"{title_prefix} Cumulative Returns - {fold_id}")
        plt.xlabel("Date")
        plt.ylabel("Cumulative Return (%)")
        plt.legend(title="Weight Method")
        plt.tight_layout()
        plt.show()

def compute_drawdown_df(returns_df):
    
    df = returns_df.copy().fillna(0)
    cumulative_prod_df = (1+df).cumprod()
    run_max = cumulative_prod_df.cummax()
    drawdown = cumulative_prod_df / run_max -1 
    
    return drawdown

def plot_drawdowns_by_fold(returns_by_fold, title_prefix):
    
    for fold_id, returns_df in returns_by_fold.items():
        drawdown_df = compute_drawdown_df(returns_df)

        ax = (drawdown_df * 100).plot(figsize=(10, 5))
        ax.axhline(0, linewidth=1)

        plt.title(f"{title_prefix} Drawdown - {fold_id}")
        plt.xlabel("Date")
        plt.ylabel("Drawdown (%)")
        plt.legend(title="Weight Method")
        plt.tight_layout()
        plt.show()
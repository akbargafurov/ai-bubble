import matplotlib.pyplot as plt
import seaborn as sns


def plot_correlation_matrix(returns):
    """
    Plot the correlation matrix of stock returns.

    Parameters:
        returns (pd.DataFrame): pandas DataFrame of daily returns indexed by date.

    Returns:
        None
    """

    # plot correlation matrix of returns
    corr_matrix = returns.corr()

    # create a heatmap with specified settings
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", vmin=-1, vmax=1)
    plt.title("correlation matrix of AI stock returns")
    plt.tight_layout()
    plt.show()


def plot_rolling_correlation(rolling_corr):
    """
    Plot the rolling average correlation of stock returns.

    Parameters:
        rolling_corr (pd.Series): pandas Series of rolling average correlations indexed by date.

    Returns:
        None
    """

    # create a line plot with specified settings
    plt.figure(figsize=(10, 6))
    plt.plot(rolling_corr, color="purple", label="average 60 days rolling correlation")
    plt.axhline(y=0.5, color="gray", linestyle="--")

    plt.title("60-day rolling average correlation among AI stocks")
    plt.ylabel("average correlation")
    plt.xlabel("date")

    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_rolling_sharpe(rolling_sharpe):
    """
    Plot the rolling Sharpe ratio of stock returns.

    Parameters:
        rolling_sharpe (pd.Series): Series of rolling Sharpe ratios indexed by date.

    Returns:
        None
    """

    # create a line plot with specified settings
    plt.figure(figsize=(10, 6))
    plt.plot(
        rolling_sharpe.index,
        rolling_sharpe.values,
        color="purple",
        label="average 60 days rolling Sharpe ratio",
    )
    plt.axhline(y=0.0, color="gray", linestyle="--")

    plt.title("60-day rolling average Sharpe ratio among AI stocks")
    plt.ylabel("average Sharpe ratio")
    plt.xlabel("date")

    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_drawdown(drawdown):
    """
    Plot the drawdown curve.

    Parameters:
        drawdown (pd.Series): series of drawdown values indexed by date.

    Returns:
        None
    """

    # create a line plot with specified settings
    plt.figure(figsize=(10, 6))
    plt.fill_between(drawdown.index, drawdown.values, 0, alpha=0.25)
    plt.plot(
        drawdown.index,
        drawdown.values,
        color="purple",
        label="average drawdown among AI stocks",
    )

    plt.ylabel("drawdown")
    plt.xlabel("date")
    plt.title("drawdown curve for AI stocks")

    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_normalized_returns(returns):
    """
    Plot normalized returns of AI stocks.

    Parameters:
        returns (pd.DataFrame): DataFrame of daily returns indexed by date.

    Returns:
        None
    """

    # normalize returns to start at 1
    normalized_returns = returns / returns.iloc[0]

    # generate distinct colors for each stock line
    colors = sns.color_palette("deep", n_colors=len(normalized_returns.columns))

    # create a line plot with specified settings
    plt.figure(figsize=(10, 6))
    for idx, column in normalized_returns.columns:
        sns.lineplot(
            x=normalized_returns.index,
            y=normalized_returns[column],
            label=column,
            color=colors[idx],
        )

    plt.ylabel("normalized return (start @ 1.0)")
    plt.xlabel("date")
    plt.title("normalized return of selected AI-related stocks")

    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_index_vs_benchmark(
    ai_index, 
    benchmark_index, 
    ai_label="AI basket (equal weight)", 
    benchmark_label=None
):
    """
    Plot AI index versus benchmark index.

    Parameters:
        ai_index (pd.Series): Series of AI index values indexed by date.
        benchmark_index (pd.Series): Series of benchmark index values indexed by date.
        ai_label (str, optional): Label for the AI index line.
        benchmark_name (str, optional): Name of the benchmark index for labeling.

    Returns:
        None
    """

    # find common dates between the two indices
    common_index = ai_index.index.intersection(benchmark_index.index)
    ai = ai_index.loc[common_index]
    bench = benchmark_index.loc[common_index]

    # create a line plot with specified settings
    plt.figure(figsize=(10, 6))
    plt.plot(ai.index, ai, label=ai_label)
    plt.plot(bench.index, bench, label=benchmark_label)

    plt.ylabel("normalized index level")
    plt.xlabel("date")
    plt.title(f"{ai_label} vs {benchmark_label}")

    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_return_distribution(
    ai_returns, 
    benchmark_returns, 
    ai_label="AI basket", 
    benchmark_label="Benchmark"
):
    """
    Plot return distribution comparison between AI basket and benchmark.

    Parameters:
        ai_returns (pd.Series): Series of AI basket returns.
        benchmark_returns (pd.Series): Series of benchmark returns.
        ai_label (str, optional): Label for AI basket in the plot.
        benchmark_label (str, optional): Label for benchmark in the plot.

    Returns:
        None
    """

    # create a density plot with specified settings
    plt.figure(figsize=(10, 6))
    sns.kdeplot(ai_returns, label=ai_label)
    sns.kdeplot(benchmark_returns, label=benchmark_label)

    plt.ylabel("density")
    plt.xlabel("daily return")
    plt.title(f"return distribution comparison: {ai_label} vs {benchmark_label}")

    plt.legend()
    plt.tight_layout()
    plt.show()

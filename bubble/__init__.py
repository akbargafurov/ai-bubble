from .loader import load_stock_data

from .indicators import (
    calculate_returns,
    calculate_rolling_volatility,
    calculate_rolling_correlation,
    build_equal_weight_index,
    calculate_index_returns,
    calculate_rolling_sharpe,
    calculate_drawdown,
    calculate_max_drawdown
)

from .visualizations import (
    plot_correlation_matrix,
    plot_rolling_correlation,
    plot_normalized_returns,
    plot_index_vs_benchmark,
    plot_rolling_sharpe,
    plot_drawdown,
    plot_return_distribution
)

__version__ = "0.1.0"
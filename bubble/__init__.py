from .loader import load_stock_data

from .indicators import (
    build_equal_weight_index,
    calculate_drawdown,
    calculate_index_returns,
    calculate_max_drawdown,
    calculate_returns,
    calculate_rolling_correlation,
    calculate_rolling_sharpe,
    calculate_rolling_volatility,
)

from .visualizations import (
    plot_correlation_matrix,
    plot_drawdown,
    plot_index_vs_benchmark,
    plot_normalized_prices,
    plot_return_distribution,
    plot_rolling_correlation,
    plot_rolling_sharpe,
    plot_rolling_volatility,
)

__version__ = "0.1.0"

import datetime as dt
import pandas as pd
import streamlit as st

from bubble.loader import load_stock_data

# -------------------------------------------------------------------
# 1. configuration: tickers and presets
# -------------------------------------------------------------------

AI_TICKERS = [
    "NVDA",
    "MSFT",
    "GOOGL",
    "META",
    "AMZN",
    "TSM",
    "AMD",
    "AVGO",
    "ASML",
    "BOTZ",
    "ARKQ",
    "AIQ",
]

TICKER_CATEGORIES = {
    "core AI leaders": ["NVDA", "MSFT", "GOOGL", "META"],
    "AI hardware / semis": ["NVDA", "AMD", "AVGO", "ASML", "TSM"],
    "AI platforms": ["MSFT", "GOOGL", "META", "AMZN"],
    "AI ETFs": ["BOTZ", "ARKQ", "AIQ"],
    "all AI names": AI_TICKERS,
    "custom selection": [],
}

PRESET_DESCRIPTIONS = {
    "core AI leaders": "mixture of big tech and flagship AI names (NVDA, MSFT, GOOGL, META, AMZN).",
    "AI hardware / semis": "chip designers / manufacturers most exposed to AI workloads.",
    "AI platforms": "large platforms integrating AI into products and services.",
    "AI ETFs": "thematic ETFs focused on AI, robotics and automation.",
    "all AI names": "all stocks and ETFs in the AI universe.",
    "custom selection": "choose any combination you like below.",
}


# -------------------------------------------------------------------
# 2. data utilities
# -------------------------------------------------------------------

@st.cache_data(show_spinner=True)
def get_all_prices() -> pd.DataFrame:
    """
    Download full history once for all AI tickers.
    Then only slice this DataFrame in memory to speed up everything.
    """
    return load_stock_data(AI_TICKERS, start="2020-01-01")


def compute_start_date(label: str) -> dt.date:
    """Map a time-frame label to a start date."""
    today = dt.date.today()

    if label == "last 1 month":
        return today - dt.timedelta(days=30)
    if label == "last 6 months":
        return today - dt.timedelta(days=182)
    if label == "last 1 year":
        return today - dt.timedelta(days=365)
    if label == "last 3 years":
        return today - dt.timedelta(days=3 * 365)
    # default: last 5 years
    return today - dt.timedelta(days=5 * 365)


# -------------------------------------------------------------------
# 3. main app
# -------------------------------------------------------------------

def main():
    # ----- page layout -----
    st.set_page_config(
        page_title="AI Bubble – Normalized Price Explorer",
        layout="wide",
    )

    st.title("are we in an AI bubble? – normalized price explorer")

    st.markdown(
        """
        this app lets you explore **normalized price paths** for AI-related stocks and ETFs.

        data are fetched **once** from Yahoo finance. use the sidebar to:

        - choose a **time frame**,
        - pick a **preset group of tickers** (core AI leaders, hardware, ETFs, etc.),
        - or switch to **custom selection** to choose any combination.
        """
    )

    # ----- sidebar controls -----
    st.sidebar.header("settings")

    period = st.sidebar.radio(
        "time frame",
        options=[
            "last 1 month",
            "last 6 months",
            "last 1 year",
            "last 3 years",
            "last 5 years",
        ],
        index=2,
    )

    start_date = compute_start_date(period)
    st.sidebar.write(f"start date: **{start_date.isoformat()}**")

    preset = st.sidebar.selectbox(
        "ticker preset",
        options=list(TICKER_CATEGORIES.keys()),
        index=0,
    )

    st.sidebar.caption(PRESET_DESCRIPTIONS[preset])

    # what should the selection be for this preset?
    if preset == "custom selection":
        preset_selection = ["NVDA", "MSFT", "GOOGL", "META"]
    else:
        preset_selection = TICKER_CATEGORIES[preset]

    # session state: remember current preset + selection
    if "current_preset" not in st.session_state:
        st.session_state.current_preset = preset
        st.session_state.selected_tickers = preset_selection

    if preset != st.session_state.current_preset:
        st.session_state.current_preset = preset
        st.session_state.selected_tickers = preset_selection

    selected_tickers = st.sidebar.multiselect(
        "tickers (starting from preset)",
        options=AI_TICKERS,
        key="selected_tickers",
        help="choose a preset above, then tweak the selection here if you like.",
    )

    st.sidebar.markdown("all available AI tickers:")
    st.sidebar.write(", ".join(AI_TICKERS))

    # downsampling (faster for long periods)
    short_periods = {"last 1 month"}
    downsample_default = period not in short_periods

    downsample = st.sidebar.checkbox(
        "downsample to weekly data (faster)", value=downsample_default
    )

    # ----- data loading & filtering -----
    prices_all = get_all_prices()

    if not selected_tickers:
        st.warning("select at least one ticker to display.")
        st.stop()

    prices = prices_all.loc[
        prices_all.index >= pd.to_datetime(start_date), selected_tickers
    ]

    if prices.empty:
        st.warning("no data available for this combination of date range and tickers.")
        st.stop()

    if downsample:
        prices = prices.resample("W").last()

    # normalize and compute cumulative returns
    normalized = prices / prices.iloc[0]
    cum_return = (normalized - 1.0) * 100.0

    # ----- main chart -----
    st.subheader("cumulative return since start date (%)")
    st.line_chart(cum_return)

    # ----- performance summary table -----
    last = cum_return.iloc[-1]
    summary = (
        pd.DataFrame({"total return (%)": last.round(1)})
        .sort_values("total return (%)", ascending=False)
    )

    st.subheader("performance over selected period")

    styler = (
        summary.style.format({"total return (%)": "{:.1f}"})
        .set_properties(subset=["total return (%)"], **{"text-align": "right"})
        .set_table_styles(
            [
                {
                    "selector": "th.col_heading",
                    "props": [("text-align", "right")],
                }
            ]
        )
    )

    st.dataframe(styler)

    # ----- explanation -----
    with st.expander("how to read this chart"):
        st.markdown(
            f"""
            - each line starts at **0%** on `{start_date.isoformat()}` (the chosen start date).
            - a value of **200%** means “the stock is 3x the starting value”.
            - the **performance over selected period** table shows total return for each selected ticker
            over this window.
            - use **time frame**, **ticker preset** and **tickers (starting from preset)** to explore
            how different parts of the AI universe have moved relative to each other.
            """
        )


# -------------------------------------------------------------------
# 4. entry point
# -------------------------------------------------------------------

if __name__ == "__main__":
    main()
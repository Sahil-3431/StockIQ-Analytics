import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.database import (
    database_health_check,
    get_all_data,
)
from utils.theme import apply_theme

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SQL - Stock Market Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION STATE
# ============================================================

if "current_page" not in st.session_state:
    st.session_state.current_page = "📊 Executive Dashboard"


# ============================================================
# APPLY PREMIUM THEME
# ============================================================

apply_theme()


# ============================================================
# PREMIUM UI CSS
# ============================================================

st.markdown(
    """
    <style>
    /* ========================================================
       MAIN LAYOUT
       ======================================================== */

    .block-container {
        max-width: 100% !important;
        padding-top: 2rem !important;
        padding-bottom: 2.5rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    /* ========================================================
       SIDEBAR INTERNAL SPACING
       ======================================================== */

    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }

    /* ========================================================
       SIDEBAR SCROLLBAR
       ======================================================== */

    section[data-testid="stSidebar"] ::-webkit-scrollbar {
        width: 5px;
    }
    section[data-testid="stSidebar"] ::-webkit-scrollbar-thumb {
        border-radius: 10px;
        background: rgba(148, 163, 184, 0.30);
    }

    /* ========================================================
       BRAND
       ======================================================== */

    .brand-wrapper {
        padding: 5px 5px 14px 5px;
    }
    .brand-row {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .brand-icon {
        width: 40px;
        height: 40px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 21px;
        background: linear-gradient(
            135deg,
            #4F46E5,
            #7C3AED
        );
        box-shadow:
            0 7px 18px rgba(79, 70, 229, 0.22);
    }
    .brand-name {
        color: #F8FAFC !important;
        font-size: 19px;
        font-weight: 800;
        letter-spacing: -0.3px;
    }
    .brand-description {
        color: #94A3B8 !important;
        margin-top: 7px;
        font-size: 11px;
        line-height: 1.45;
    }

    /* ========================================================
       SIDEBAR LABELS
       ======================================================== */

    .sidebar-label {
        color: #94A3B8 !important;
        font-size: 11px;
        font-weight: 750;
        letter-spacing: 0.7px;
        text-transform: uppercase;
        margin-top: 8px;
        margin-bottom: 7px;
    }

    /* ========================================================
       SIDEBAR DIVIDER
       ======================================================== */

    .sidebar-divider {
        height: 1px;
        width: 100%;
        margin: 9px 0 14px 0;
        background: rgba(148, 163, 184, 0.16);
    }

    /* ========================================================
       SIDEBAR NAVIGATION
       ======================================================== */

    section[data-testid="stSidebar"]
    div[role="radiogroup"] {
        gap: 4px;
    }
    section[data-testid="stSidebar"]
    div[role="radiogroup"] > label {
        border-radius: 10px;
        padding: 8px 10px !important;
        margin: 0 !important;
        transition:
            background 0.15s ease,
            transform 0.15s ease;
    }
    section[data-testid="stSidebar"]
    div[role="radiogroup"] > label:hover {
        background: rgba(99, 102, 241, 0.10);
    }
    section[data-testid="stSidebar"]
    div[role="radiogroup"] > label[data-checked="true"] {
        background: linear-gradient(
            135deg,
            rgba(99, 102, 241, 0.18),
            rgba(139, 92, 246, 0.12)
        );
        border: 1px solid rgba(99, 102, 241, 0.25);
    }

    /* ========================================================
       DATABASE CARD
       ======================================================== */

    .database-card {
        padding: 11px 12px;
        border-radius: 12px;
        background: #111827;
        border: 1px solid #1E293B;
    }
    .database-status {
        display: flex;
        align-items: center;
        gap: 7px;
        font-size: 12px;
        font-weight: 700;
        color: #E2E8F0 !important;
    }
    .status-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #22C55E;
        box-shadow:
            0 0 0 4px rgba(34, 197, 94, 0.12);
    }
    .database-info {
        margin-top: 8px;
        font-size: 10px;
        line-height: 1.7;
        color: #94A3B8 !important;
    }
    .database-info b {
        color: #E2E8F0 !important;
    }

    /* ========================================================
       PAGE HEADER
       ======================================================== */

    .page-header {
        margin-bottom: 26px;
    }
    .page-title {
        display: flex;
        align-items: center;
        gap: 11px;
        color: #F8FAFC !important;
        font-size: 32px;
        font-weight: 800;
        letter-spacing: -0.8px;
        margin-bottom: 6px;
    }
    .page-title-icon {
        width: 42px;
        height: 42px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 13px;
        background: linear-gradient(
            135deg,
            #4F46E5,
            #7C3AED
        );
        font-size: 22px;
        box-shadow:
            0 8px 20px rgba(79, 70, 229, 0.18);
    }
    .page-description {
        color: #94A3B8 !important;
        font-size: 13px;
        margin-left: 53px;
    }

    /* ========================================================
       METRIC CARDS
       ======================================================== */

    div[data-testid="stMetric"] {
        padding: 17px 18px !important;
        border-radius: 14px !important;
        background: #111827 !important;
        border: 1px solid #1E293B !important;
        box-shadow:
            0 5px 18px rgba(0, 0, 0, 0.18);
    }
    div[data-testid="stMetricLabel"] {
        color: #94A3B8 !important;
        font-size: 12px;
        font-weight: 600;
    }
    div[data-testid="stMetricValue"] {
        color: #F8FAFC !important;
        font-size: 25px;
        font-weight: 750;
    }

    /* ========================================================
       SECTION TITLE
       ======================================================== */

    .section-title {
        color: #F8FAFC !important;
        font-size: 18px;
        font-weight: 750;
        margin-top: 24px;
        margin-bottom: 12px;
    }

    /* ========================================================
       PROJECT CARD
       ======================================================== */

    .project-card {
        padding: 22px 24px;
        border-radius: 16px;
        background: #111827;
        border: 1px solid #1E293B;

        box-shadow:
            0 6px 22px rgba(0, 0, 0, 0.16);
    }
    .project-title {
        color: #F8FAFC !important;
        font-size: 17px;
        font-weight: 750;
        margin-bottom: 10px;
    }
    .project-text {
        color: #CBD5E1 !important;
        font-size: 13px;
        line-height: 1.75;
    }
    .project-text b {
        color: #F8FAFC !important;
    }

    /* ========================================================
       ALERTS
       ======================================================== */

    .stAlert {
        border-radius: 12px;
    }

    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        border-radius: 10px;
        font-weight: 650;
        background: #111827 !important;
        color: #F8FAFC !important;
        border: 1px solid #334155 !important;
    }
    .stButton > button:hover {
        background: #1E293B !important;
        border-color: #6366F1 !important;
    }

    /* ========================================================
       FOOTER
       ======================================================== */

    .app-footer {
        color: #64748B !important;
        text-align: center;
        margin-top: 42px;
        padding-top: 17px;
        font-size: 11px;
        border-top: 1px solid rgba(148, 163, 184, 0.14);
    }


    /* ========================================================
       PLOTLY CONTAINER
       ======================================================== */

    .js-plotly-plot {
        width: 100% !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # --------------------------------------------------------
    # BRAND
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="brand-wrapper">
            <div class="brand-row">
                <div class="brand-icon">
                    📊
                </div>
                <div class="brand-name">
                    StockIQ Analytics
                </div>
            </div>
            <div class="brand-description">
                SQL-Powered Stock Market Intelligence
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-divider"></div>',
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # NAVIGATION
    # --------------------------------------------------------

    st.markdown(
        '<div class="sidebar-label">Navigation</div>',
        unsafe_allow_html=True,
    )

    pages = [
        "📊 Executive Dashboard",
        "📈 Stock Analysis",
        "🏆 Performance Comparison",
        "💹 Trading & Volume",
        "💡 Insights & Recommendations",
        "🧪 SQL Playground",
    ]

    selected_page = st.radio(
        "Navigation",
        pages,
        index=pages.index(
            st.session_state.current_page
        ),
        label_visibility="collapsed",
    )

    st.session_state.current_page = selected_page

    st.markdown(
        '<div class="sidebar-divider"></div>',
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # SYSTEM STATUS
    # --------------------------------------------------------

    st.markdown(
        '<div class="sidebar-label">System Status</div>',
        unsafe_allow_html=True,
    )

    try:
        health = database_health_check()
        st.markdown(
            f"""
            <div class="database-card">
                <div class="database-status">
                    <span class="status-dot"></span>
                    Database Connected
                </div>
                <div class="database-info">
                    Records:
                    <b>{health["total_records"]:,}</b>
                    <br>
                    Companies:
                    <b>{health["total_companies"]}</b>
                    <br>
                    Period:
                    <b>{health["start_date"]}</b>
                    →
                    <b>{health["end_date"]}</b>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    except Exception:

        st.error(
            "Database connection failed"
        )


    # --------------------------------------------------------
    # SIDEBAR FOOTER
    # --------------------------------------------------------

    st.markdown(
        """
        <div style="
            text-align:center;
            margin-top:18px;
            font-size:10px;
            color:#64748B;
        ">
            SQL • Python • Streamlit • Plotly
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# CURRENT PAGE
# ============================================================

page = st.session_state.current_page

# ============================================================
# EXECUTIVE DASHBOARD
# ============================================================

if page == "📊 Executive Dashboard":

    # ========================================================
    # PAGE HEADER
    # ========================================================

    st.markdown(
        """
        <div class="page-header">
            <div class="page-title">
                <div class="page-title-icon">📊</div>
                Executive Dashboard
            </div>
            <div class="page-description">
                High-level overview of stock market activity,
                pricing, returns, trading volume and delivery.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ========================================================
    # LOAD DATA
    # ========================================================

    try:
        df = get_all_data()
        if df.empty:
            st.warning("No stock market data available.")
            st.stop()

        # ----------------------------------------------------
        # DATE CONVERSION
        # ----------------------------------------------------

        df["trade_date"] = pd.to_datetime(
            df["trade_date"],
            errors="coerce"
        )

        # ----------------------------------------------------
        # NUMERIC CONVERSION
        # ----------------------------------------------------

        numeric_columns = [
            "open_price",
            "high_price",
            "low_price",
            "close_price",
            "wap",
            "no_of_shares",
            "no_of_trades",
            "total_turnover",
            "deliverable_quantity",
            "delivery_percentage",
            "daily_return_percentage",
            "price_range",
            "intraday_return_percentage",
            "turnover_crore",
            "volume_lakh",
        ]

        for column in numeric_columns:
            if column in df.columns:
                df[column] = pd.to_numeric(
                    df[column],
                    errors="coerce"
                )

        # ----------------------------------------------------
        # CLEAN ANALYTICS DATA
        # ----------------------------------------------------

        df = df.dropna(
            subset=[
                "trade_date",
                "company",
                "close_price"
            ]
        ).copy()

        # ====================================================
        # KPI CALCULATIONS
        # ====================================================

        total_records = len(df)
        total_companies = df["company"].nunique()
        total_turnover = (
            df["turnover_crore"].sum()
            if "turnover_crore" in df.columns
            else 0
        )

        positive_days = (
            (df["daily_return_percentage"] > 0).sum()
            if "daily_return_percentage" in df.columns
            else 0
        )

        total_return_days = (
            df["daily_return_percentage"].notna().sum()
            if "daily_return_percentage" in df.columns
            else 0
        )

        positive_day_percentage = (
            (positive_days / total_return_days) * 100
            if total_return_days > 0
            else 0
        )

        average_close = df["close_price"].mean()

        average_trades = (
            df["no_of_trades"].mean()
            if "no_of_trades" in df.columns
            else 0
        )

        # ====================================================
        # KPI CARDS
        # ====================================================

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total Records",
                f"{total_records:,}",
            )

        with col2:
            st.metric(
                "Companies",
                f"{total_companies}",
            )

        with col3:
            st.metric(
                "Total Turnover",
                f"₹{total_turnover:,.2f} Cr",
            )

        with col4:
            st.metric(
                "Positive Trading Days",
                f"{positive_day_percentage:.1f}%",
            )

        # ====================================================
        # SECOND KPI ROW
        # ====================================================

        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                "Average Close Price",
                f"₹{average_close:,.2f}",
            )
        with col2:
            st.metric(
                "Average Daily Trades",
                f"{average_trades:,.0f}",
            )
        with col3:
            st.metric(
                "Highest Close",
                f"₹{df['close_price'].max():,.2f}",
            )
        with col4:
            st.metric(
                "Lowest Close",
                f"₹{df['close_price'].min():,.2f}",
            )

        # ====================================================
        # FILTERS
        # ====================================================

        st.markdown(
            '<div class="section-title">🔎 Dashboard Filters</div>',
            unsafe_allow_html=True,
        )

        filter_col1, filter_col2, filter_col3 = st.columns(3)
        with filter_col1:
            company_options = [
                "All Companies"
            ] + sorted(
                df["company"].dropna().unique().tolist()
            )

            selected_company = st.selectbox(
                "Company",
                company_options,
                key="executive_company",
            )

        with filter_col2:
            min_date = df["trade_date"].min().date()
            max_date = df["trade_date"].max().date()
            selected_dates = st.date_input(
                "Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date,
                key="executive_dates",
            )

        with filter_col3:
            chart_metric = st.selectbox(
                "Price Metric",
                [
                    "Close Price",
                    "Open Price",
                    "High Price",
                    "Low Price",
                    "WAP",
                ],
                key="executive_price_metric",
            )

        # ====================================================
        # APPLY FILTERS
        # ====================================================

        filtered_df = df.copy()
        if selected_company != "All Companies":
            filtered_df = filtered_df[
                filtered_df["company"] == selected_company
            ]

        if isinstance(selected_dates, tuple):
            if len(selected_dates) == 2:
                start_date = pd.Timestamp(
                    selected_dates[0]
                )
                end_date = pd.Timestamp(
                    selected_dates[1]
                )
                filtered_df = filtered_df[
                    (
                        filtered_df["trade_date"]
                        >= start_date
                    )
                    &
                    (
                        filtered_df["trade_date"]
                        <= end_date
                    )
                ]
        elif selected_dates:
            selected_date = pd.Timestamp(
                selected_dates
            )
            filtered_df = filtered_df[
                filtered_df["trade_date"]
                == selected_date
            ]

        # ====================================================
        # FILTERED DATA VALIDATION
        # ====================================================

        if filtered_df.empty:
            st.warning("No data available for the selected filters.")
            st.stop()

        # ====================================================
        # PLOTLY DARK THEME SETTINGS
        # ====================================================

        plotly_template = "plotly_dark"
        chart_background = "#111827"
        paper_background = "#111827"

        # ====================================================
        # SECTION 1
        # CLOSING PRICE TREND
        # ====================================================

        st.markdown(
            '<div class="section-title">📈 Historical Price Trend</div>',
            unsafe_allow_html=True,
        )
        price_column_map = {
            "Close Price": "close_price",
            "Open Price": "open_price",
            "High Price": "high_price",
            "Low Price": "low_price",
            "WAP": "wap",
        }
        selected_price_column = price_column_map[chart_metric]
        price_df = (
            filtered_df
            .sort_values("trade_date")
            .copy()
        )

        if selected_company == "All Companies":
            fig_price = px.line(
                price_df,
                x="trade_date",
                y=selected_price_column,
                color="company",
                title=f"{chart_metric} Trend by Company",
            )
        else:
            fig_price = px.line(
                price_df,
                x="trade_date",
                y=selected_price_column,
                title=f"{selected_company} — {chart_metric} Trend",
            )
        fig_price.update_layout(
            template=plotly_template,
            height=430,
            paper_bgcolor=paper_background,
            plot_bgcolor=chart_background,
            font=dict(
                color="#E5E7EB"
            ),
            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20,
            ),
            hovermode="x unified",
        )
        fig_price.update_xaxes(
            title="Trade Date",
            gridcolor="#263449",
        )
        fig_price.update_yaxes(
            title="Price (₹)",
            gridcolor="#263449",
        )
        st.plotly_chart(
            fig_price,
            use_container_width=True,
        )

        # ====================================================
        # SECTION 2
        # COMPANY AVERAGE CLOSE
        # ====================================================

        st.markdown(
            '<div class="section-title">🏢 Average Closing Price by Company</div>',
            unsafe_allow_html=True,
        )
        company_avg = (
            filtered_df
            .groupby("company", as_index=False)
            ["close_price"]
            .mean()
            .sort_values(
                "close_price",
                ascending=False,
            )
        )
        fig_company = px.bar(
            company_avg,
            x="company",
            y="close_price",
            text_auto=".2f",
            title="Average Closing Price",
        )
        fig_company.update_layout(
            template=plotly_template,
            height=400,
            paper_bgcolor=paper_background,
            plot_bgcolor=chart_background,
            font=dict(
                color="#E5E7EB"
            ),
            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20,
            ),
            showlegend=False,
        )
        fig_company.update_xaxes(
            title="Company",
            gridcolor="#263449",
        )
        fig_company.update_yaxes(
            title="Average Close Price (₹)",
            gridcolor="#263449",
        )
        st.plotly_chart(
            fig_company,
            use_container_width=True,
        )

        # ====================================================
        # SECTION 3
        # TURNOVER TREND
        # ====================================================

        st.markdown(
            '<div class="section-title">💰 Turnover Trend</div>',
            unsafe_allow_html=True,
        )
        turnover_df = (
            filtered_df
            .groupby(
                "trade_date",
                as_index=False
            )["turnover_crore"]
            .sum()
            .sort_values("trade_date")
        )
        fig_turnover = px.area(
            turnover_df,
            x="trade_date",
            y="turnover_crore",
            title="Daily Total Market Turnover",
        )
        fig_turnover.update_layout(
            template=plotly_template,
            height=400,
            paper_bgcolor=paper_background,
            plot_bgcolor=chart_background,
            font=dict(
                color="#E5E7EB"
            ),
            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20,
            ),
        )
        fig_turnover.update_xaxes(
            title="Trade Date",
            gridcolor="#263449",
        )
        fig_turnover.update_yaxes(
            title="Turnover (₹ Crore)",
            gridcolor="#263449",
        )
        st.plotly_chart(
            fig_turnover,
            use_container_width=True,
        )

        # ====================================================
        # SECTION 4
        # POSITIVE VS NEGATIVE DAYS
        # ====================================================

        st.markdown(
            '<div class="section-title">📊 Market Direction</div>',
            unsafe_allow_html=True,
        )
        direction_df = pd.DataFrame(
            {
                "Direction": [
                    "Positive Days",
                    "Negative Days",
                    "Flat Days",
                ],
                "Days": [
                    (
                        filtered_df[
                            filtered_df[
                                "daily_return_percentage"
                            ] > 0
                        ].shape[0]
                    ),
                    (
                        filtered_df[
                            filtered_df[
                                "daily_return_percentage"
                            ] < 0
                        ].shape[0]
                    ),
                    (
                        filtered_df[
                            filtered_df[
                                "daily_return_percentage"
                            ] == 0
                        ].shape[0]
                    ),
                ],
            }
        )
        fig_direction = px.bar(
            direction_df,
            x="Direction",
            y="Days",
            text="Days",
            title="Trading Day Direction",
        )
        fig_direction.update_layout(
            template=plotly_template,
            height=380,
            paper_bgcolor=paper_background,
            plot_bgcolor=chart_background,
            font=dict(
                color="#E5E7EB"
            ),
            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20,
            ),
            showlegend=False,
        )
        fig_direction.update_xaxes(
            title="Market Direction",
            gridcolor="#263449",
        )
        fig_direction.update_yaxes(
            title="Number of Days",
            gridcolor="#263449",
        )
        st.plotly_chart(
            fig_direction,
            use_container_width=True,
        )

        # ====================================================
        # SECTION 5
        # TRADING ACTIVITY
        # ====================================================

        st.markdown(
            '<div class="section-title">📦 Trading Activity</div>',
            unsafe_allow_html=True,
        )
        activity_df = (
            filtered_df
            .groupby("company", as_index=False)
            .agg(
                Average_Trades=(
                    "no_of_trades",
                    "mean",
                ),
                Average_Volume=(
                    "volume_lakh",
                    "mean",
                ),
            )
            .sort_values(
                "Average_Trades",
                ascending=False,
            )
        )
        fig_activity = px.bar(
            activity_df,
            x="company",
            y="Average_Trades",
            text_auto=".0f",
            title="Average Daily Trades by Company",
        )
        fig_activity.update_layout(
            template=plotly_template,
            height=400,
            paper_bgcolor=paper_background,
            plot_bgcolor=chart_background,
            font=dict(
                color="#E5E7EB"
            ),
            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20,
            ),
            showlegend=False,
        )
        fig_activity.update_xaxes(
            title="Company",
            gridcolor="#263449",
        )
        fig_activity.update_yaxes(
            title="Average Number of Trades",
            gridcolor="#263449",
        )
        st.plotly_chart(
            fig_activity,
            use_container_width=True,
        )

        # ====================================================
        # SECTION 6
        # DELIVERY PARTICIPATION
        # ====================================================

        st.markdown(
            '<div class="section-title">🚚 Delivery Participation</div>',
            unsafe_allow_html=True,
        )
        delivery_df = (
            filtered_df
            .groupby("company", as_index=False)
            ["delivery_percentage"]
            .mean()
            .sort_values(
                "delivery_percentage",
                ascending=False,
            )
        )
        fig_delivery = px.bar(
            delivery_df,
            x="company",
            y="delivery_percentage",
            text_auto=".2f",
            title="Average Delivery Percentage",
        )
        fig_delivery.update_layout(
            template=plotly_template,
            height=400,
            paper_bgcolor=paper_background,
            plot_bgcolor=chart_background,
            font=dict(
                color="#E5E7EB"
            ),
            margin=dict(
                l=20,
                r=20,
                t=60,
                b=20,
            ),
            showlegend=False,
        )
        fig_delivery.update_xaxes(
            title="Company",
            gridcolor="#263449",
        )
        fig_delivery.update_yaxes(
            title="Delivery (%)",
            gridcolor="#263449",
        )
        st.plotly_chart(
            fig_delivery,
            use_container_width=True,
        )

        # ====================================================
        # MARKET SUMMARY
        # ====================================================

        st.markdown(
            '<div class="section-title">📌 Market Summary</div>',
            unsafe_allow_html=True,
        )
        summary_col1, summary_col2 = st.columns(2)
        with summary_col1:
            highest_company = (
                company_avg.iloc[0]["company"]
                if not company_avg.empty
                else "N/A"
            )
            highest_average_close = (
                company_avg.iloc[0]["close_price"]
                if not company_avg.empty
                else 0
            )
            st.markdown(
                f"""
                <div class="project-card">
                    <div class="project-title">
                        🏆 Highest Average Closing Price
                    </div>
                    <div class="project-text">
                        <b>{highest_company}</b>
                        recorded the highest average closing
                        price in the selected period.
                        <br><br>
                        Average Close:
                        <b>₹{highest_average_close:,.2f}</b>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with summary_col2:
            highest_delivery_company = (
                delivery_df.iloc[0]["company"]
                if not delivery_df.empty
                else "N/A"
            )
            highest_delivery = (
                delivery_df.iloc[0]["delivery_percentage"]
                if not delivery_df.empty
                else 0
            )

            st.markdown(
                f"""
                <div class="project-card">
                    <div class="project-title">
                        🚚 Highest Average Delivery
                    </div>
                    <div class="project-text">
                        <b>{highest_delivery_company}</b>
                        recorded the highest average delivery
                        participation.
                        <br><br>
                        Average Delivery:
                        <b>{highest_delivery:.2f}%</b>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    except Exception as e:
        st.error(f"Unable to load Executive Dashboard: {e}")

# ============================================================
# STOCK ANALYSIS
# ============================================================

elif page == "📈 Stock Analysis":
    st.markdown(
        """
        <div class="page-header">
            <h1>📈 Stock Analysis</h1>
            <p>Explore detailed price movement, returns, volatility and trading activity for individual stocks.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    df = get_all_data()
    if df.empty:
        st.warning("No stock market data available.")
        st.stop()

    df["trade_date"] = pd.to_datetime(df["trade_date"])

    # --------------------------------------------------------
    # FILTER SECTION
    # --------------------------------------------------------

    st.markdown("### 🔎 Analysis Filters")
    filter_col1, filter_col2, filter_col3 = st.columns([1.2, 1.5, 1.2])
    companies = sorted(df["company"].dropna().unique().tolist())

    with filter_col1:
        selected_company = st.selectbox(
            "Select Company",
            companies,
            key="stock_analysis_company",
        )

    company_df = df[df["company"] == selected_company].copy()
    min_date = company_df["trade_date"].min().date()
    max_date = company_df["trade_date"].max().date()

    with filter_col2:
        selected_dates = st.date_input(
            "Select Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            key="stock_analysis_dates",
        )

    with filter_col3:
        price_metric = st.selectbox(
            "Price Metric",
            [
                "Close Price",
                "Open Price",
                "High Price",
                "Low Price",
                "WAP",
            ],
            key="stock_analysis_metric",
        )

    # --------------------------------------------------------
    # APPLY DATE FILTER
    # --------------------------------------------------------

    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        start_date = pd.to_datetime(selected_dates[0])
        end_date = pd.to_datetime(selected_dates[1])
        company_df = company_df[
            (company_df["trade_date"] >= start_date)
            & (company_df["trade_date"] <= end_date)
        ].copy()

    if company_df.empty:
        st.warning("No data available for the selected date range.")
        st.stop()

    company_df = company_df.sort_values("trade_date")

    # --------------------------------------------------------
    # CALCULATED METRICS
    # --------------------------------------------------------

    avg_close = company_df["close_price"].mean()
    highest_close = company_df["close_price"].max()
    lowest_close = company_df["close_price"].min()
    total_turnover = company_df["total_turnover"].sum()
    avg_trades = company_df["no_of_trades"].mean()
    avg_delivery = company_df["delivery_percentage"].mean()
    volatility = company_df["daily_return_percentage"].std()

    positive_days = (
        company_df["daily_return_percentage"] > 0
    ).sum()

    total_days = len(company_df)

    positive_day_percentage = (
        positive_days / total_days * 100
        if total_days > 0
        else 0
    )

    # --------------------------------------------------------
    # KPI CARDS
    # --------------------------------------------------------

    st.markdown("### 📊 Company Overview")

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric(
            "Average Close",
            f"₹{avg_close:,.2f}",
        )
    with k2:
        st.metric(
            "Highest Close",
            f"₹{highest_close:,.2f}",
        )
    with k3:
        st.metric(
            "Lowest Close",
            f"₹{lowest_close:,.2f}",
        )
    with k4:
        st.metric(
            "Volatility",
            f"{volatility:.2f}%",
        )

    k5, k6, k7, k8 = st.columns(4)
    with k5:
        st.metric(
            "Total Turnover",
            f"₹{total_turnover / 10_000_000:,.2f} Cr",
        )
    with k6:
        st.metric(
            "Avg Daily Trades",
            f"{avg_trades:,.0f}",
        )
    with k7:
        st.metric(
            "Avg Delivery",
            f"{avg_delivery:.2f}%",
        )
    with k8:
        st.metric(
            "Positive Days",
            f"{positive_day_percentage:.1f}%",
        )
    st.markdown("---")

    # --------------------------------------------------------
    # PRICE TREND
    # --------------------------------------------------------

    st.markdown("### 📈 Price Trend")
    fig_price = px.line(
        company_df,
        x="trade_date",
        y=price_metric.lower().replace(" ", "_"),
        title=f"{selected_company} — {price_metric} Trend",
        markers=False,
    )
    fig_price.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(color="#E5E7EB"),
        xaxis_title="Date",
        yaxis_title=price_metric,
        hovermode="x unified",
    )
    fig_price.update_xaxes(
        showgrid=True,
        gridcolor="#263449",
    )
    fig_price.update_yaxes(
        showgrid=True,
        gridcolor="#263449",
    )
    st.plotly_chart(
        fig_price,
        use_container_width=True,
    )

    # --------------------------------------------------------
    # OHLC CHART
    # --------------------------------------------------------

    st.markdown("### 🕯️ OHLC Price Movement")
    fig_ohlc = go.Figure(
        data=[
            go.Candlestick(
                x=company_df["trade_date"],
                open=company_df["open_price"],
                high=company_df["high_price"],
                low=company_df["low_price"],
                close=company_df["close_price"],
                name=selected_company,
            )
        ]
    )
    fig_ohlc.update_layout(
        title=f"{selected_company} — Open, High, Low & Close",
        template="plotly_dark",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(color="#E5E7EB"),
        xaxis_title="Date",
        yaxis_title="Price (₹)",
        xaxis_rangeslider_visible=False,
        hovermode="x unified",
    )
    fig_ohlc.update_xaxes(
        showgrid=True,
        gridcolor="#263449",
    )
    fig_ohlc.update_yaxes(
        showgrid=True,
        gridcolor="#263449",
    )
    st.plotly_chart(
        fig_ohlc,
        use_container_width=True,
    )

    # --------------------------------------------------------
    # DAILY RETURNS
    # --------------------------------------------------------

    st.markdown("### 📉 Daily Returns")
    returns_df = company_df[
        ["trade_date", "daily_return_percentage"]
    ].copy()

    fig_returns = px.bar(
        returns_df,
        x="trade_date",
        y="daily_return_percentage",
        title=f"{selected_company} — Daily Return %",
    )
    fig_returns.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(color="#E5E7EB"),
        xaxis_title="Date",
        yaxis_title="Daily Return (%)",
        hovermode="x unified",
    )
    fig_returns.update_xaxes(
        showgrid=True,
        gridcolor="#263449",
    )
    fig_returns.update_yaxes(
        showgrid=True,
        gridcolor="#263449",
        zeroline=True,
    )
    st.plotly_chart(
        fig_returns,
        use_container_width=True,
    )

    # --------------------------------------------------------
    # MONTHLY PERFORMANCE
    # --------------------------------------------------------

    st.markdown("### 📅 Monthly Performance")
    monthly_df = (
        company_df
        .set_index("trade_date")
        .resample("ME")
        .agg(
            {
                "close_price": "last",
                "daily_return_percentage": "mean",
                "total_turnover": "sum",
                "no_of_trades": "sum",
            }
        )
        .reset_index()
    )
    monthly_df["month"] = monthly_df["trade_date"].dt.strftime(
        "%b %Y"
    )
    fig_monthly = px.line(
        monthly_df,
        x="trade_date",
        y="close_price",
        markers=True,
        title=f"{selected_company} — Monthly Closing Price",
    )
    fig_monthly.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(color="#E5E7EB"),
        xaxis_title="Month",
        yaxis_title="Closing Price (₹)",
        hovermode="x unified",
    )
    fig_monthly.update_xaxes(
        showgrid=True,
        gridcolor="#263449",
    )
    fig_monthly.update_yaxes(
        showgrid=True,
        gridcolor="#263449",
    )
    st.plotly_chart(
        fig_monthly,
        use_container_width=True,
    )

    # --------------------------------------------------------
    # TRADING ACTIVITY
    # --------------------------------------------------------

    st.markdown("### 💹 Trading Activity")
    activity_col1, activity_col2 = st.columns(2)
    with activity_col1:
        fig_turnover = px.area(
            company_df,
            x="trade_date",
            y="turnover_crore",
            title=f"{selected_company} — Daily Turnover",
        )
        fig_turnover.update_layout(
            template="plotly_dark",
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            font=dict(color="#E5E7EB"),
            xaxis_title="Date",
            yaxis_title="Turnover (₹ Crore)",
            hovermode="x unified",
        )
        fig_turnover.update_xaxes(
            showgrid=True,
            gridcolor="#263449",
        )
        fig_turnover.update_yaxes(
            showgrid=True,
            gridcolor="#263449",
        )
        st.plotly_chart(
            fig_turnover,
            use_container_width=True,
        )

    with activity_col2:
        fig_trades = px.line(
            company_df,
            x="trade_date",
            y="no_of_trades",
            title=f"{selected_company} — Number of Trades",
        )
        fig_trades.update_layout(
            template="plotly_dark",
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            font=dict(color="#E5E7EB"),
            xaxis_title="Date",
            yaxis_title="Number of Trades",
            hovermode="x unified",
        )
        fig_trades.update_xaxes(
            showgrid=True,
            gridcolor="#263449",
        )
        fig_trades.update_yaxes(
            showgrid=True,
            gridcolor="#263449",
        )
        st.plotly_chart(
            fig_trades,
            use_container_width=True,
        )

    # --------------------------------------------------------
    # COMPANY STATISTICS
    # --------------------------------------------------------

    st.markdown("### 📋 Detailed Statistics")
    stats_df = pd.DataFrame(
        {
            "Metric": [
                "Company",
                "Analysis Start Date",
                "Analysis End Date",
                "Trading Days",
                "Average Open Price",
                "Average High Price",
                "Average Low Price",
                "Average Close Price",
                "Average WAP",
                "Average Daily Return",
                "Maximum Daily Return",
                "Minimum Daily Return",
                "Average Price Range",
                "Average Delivery %",
                "Total Shares Traded",
                "Total Trades",
            ],
            "Value": [
                selected_company,
                company_df["trade_date"].min().strftime("%d %b %Y"),
                company_df["trade_date"].max().strftime("%d %b %Y"),
                f"{len(company_df):,}",
                f"₹{company_df['open_price'].mean():,.2f}",
                f"₹{company_df['high_price'].mean():,.2f}",
                f"₹{company_df['low_price'].mean():,.2f}",
                f"₹{company_df['close_price'].mean():,.2f}",
                f"₹{company_df['wap'].mean():,.2f}",
                f"{company_df['daily_return_percentage'].mean():.2f}%",
                f"{company_df['daily_return_percentage'].max():.2f}%",
                f"{company_df['daily_return_percentage'].min():.2f}%",
                f"₹{company_df['price_range'].mean():,.2f}",
                f"{company_df['delivery_percentage'].mean():.2f}%",
                f"{company_df['no_of_shares'].sum():,.0f}",
                f"{company_df['no_of_trades'].sum():,.0f}",
            ],
        }
    )

    st.dataframe(
        stats_df,
        use_container_width=True,
        hide_index=True,
    )

# ============================================================
# PERFORMANCE COMPARISON
# ============================================================

elif page == "🏆 Performance Comparison":
    st.markdown(
        """
        <div class="page-header">
            <h1>🏆 Performance Comparison</h1>
            <p>Compare stock performance, returns, volatility, trading activity and delivery across companies.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    df = get_all_data()
    if df.empty:
        st.warning("No stock market data available.")
        st.stop()
    df["trade_date"] = pd.to_datetime(df["trade_date"])

    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    st.markdown("### 🔎 Comparison Filters")
    filter_col1, filter_col2 = st.columns([1.4, 1.6])
    companies = sorted(
        df["company"].dropna().unique().tolist()
    )

    with filter_col1:
        selected_companies = st.multiselect(
            "Select Companies",
            companies,
            default=companies,
            key="comparison_companies",
        )
    min_date = df["trade_date"].min().date()
    max_date = df["trade_date"].max().date()

    with filter_col2:
        selected_dates = st.date_input(
            "Select Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            key="comparison_dates",
        )
    if not selected_companies:
        st.info("Please select at least one company.")
        st.stop()

    comparison_df = df[
        df["company"].isin(selected_companies)
    ].copy()

    # --------------------------------------------------------
    # DATE FILTER
    # --------------------------------------------------------

    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        start_date = pd.to_datetime(selected_dates[0])
        end_date = pd.to_datetime(selected_dates[1])
        comparison_df = comparison_df[
            (comparison_df["trade_date"] >= start_date)
            & (comparison_df["trade_date"] <= end_date)
        ].copy()

    if comparison_df.empty:
        st.warning("No data available for the selected filters.")
        st.stop()

    # --------------------------------------------------------
    # COMPANY PERFORMANCE SUMMARY
    # --------------------------------------------------------

    summary = (
        comparison_df
        .groupby("company")
        .agg(
            {
                "close_price": ["mean", "max", "min"],
                "daily_return_percentage": [
                    "mean",
                    "std",
                    "sum",
                ],
                "total_turnover": "sum",
                "no_of_trades": "sum",
                "delivery_percentage": "mean",
                "no_of_shares": "sum",
            }
        )
        .reset_index()
    )
    summary.columns = [
        "company",
        "avg_close",
        "highest_close",
        "lowest_close",
        "avg_return",
        "volatility",
        "total_return",
        "total_turnover",
        "total_trades",
        "avg_delivery",
        "total_shares",
    ]

    # --------------------------------------------------------
    # PERIOD RETURN
    # --------------------------------------------------------

    period_returns = []

    for company in selected_companies:
        company_data = comparison_df[
            comparison_df["company"] == company
        ].sort_values("trade_date")

        if len(company_data) >= 2:
            first_close = company_data.iloc[0]["close_price"]
            last_close = company_data.iloc[-1]["close_price"]
            period_return = (
                (last_close - first_close)
                / first_close
                * 100
            )
        else:
            period_return = 0
        period_returns.append(
            {
                "company": company,
                "period_return": period_return,
            }
        )
    return_df = pd.DataFrame(period_returns)
    summary = summary.merge(
        return_df,
        on="company",
        how="left",
    )

    # --------------------------------------------------------
    # KPI SECTION
    # --------------------------------------------------------

    st.markdown("### 📊 Market Comparison Overview")
    total_companies = len(summary)
    highest_return = summary.loc[
        summary["period_return"].idxmax()
    ]
    highest_avg_price = summary.loc[
        summary["avg_close"].idxmax()
    ]
    highest_turnover = summary.loc[
        summary["total_turnover"].idxmax()
    ]
    highest_delivery = summary.loc[
        summary["avg_delivery"].idxmax()
    ]
    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.metric(
            "Companies Compared",
            f"{total_companies}",
        )
    with k2:
        st.metric(
            "Highest Period Return",
            f"{highest_return['period_return']:.2f}%",
            delta=str(highest_return["company"]),
        )
    with k3:
        st.metric(
            "Highest Avg Price",
            f"₹{highest_avg_price['avg_close']:,.2f}",
            delta=str(highest_avg_price["company"]),
        )
    with k4:
        st.metric(
            "Highest Turnover",
            f"₹{highest_turnover['total_turnover'] / 10_000_000:,.2f} Cr",
            delta=str(highest_turnover["company"]),
        )

    # --------------------------------------------------------
    # PERIOD RETURN COMPARISON
    # --------------------------------------------------------

    st.markdown("### 📈 Period Return Comparison")
    fig_return = px.bar(
        summary.sort_values(
            "period_return",
            ascending=False,
        ),
        x="company",
        y="period_return",
        title="Stock Return During Selected Period",
        text="period_return",
    )
    fig_return.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
    )
    fig_return.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(color="#E5E7EB"),
        xaxis_title="Company",
        yaxis_title="Period Return (%)",
    )
    fig_return.update_xaxes(
        showgrid=False,
    )
    fig_return.update_yaxes(
        showgrid=True,
        gridcolor="#263449",
        zeroline=True,
    )

    st.plotly_chart(
        fig_return,
        use_container_width=True,
    )

    # --------------------------------------------------------
    # AVERAGE PRICE COMPARISON
    # --------------------------------------------------------

    st.markdown("### 💰 Average Price Comparison")
    fig_price = px.bar(
        summary.sort_values(
            "avg_close",
            ascending=False,
        ),
        x="company",
        y="avg_close",
        title="Average Closing Price",
        text="avg_close",
    )
    fig_price.update_traces(
        texttemplate="₹%{text:.2f}",
        textposition="outside",
    )
    fig_price.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(color="#E5E7EB"),
        xaxis_title="Company",
        yaxis_title="Average Close Price (₹)",
    )
    fig_price.update_xaxes(
        showgrid=False,
    )
    fig_price.update_yaxes(
        showgrid=True,
        gridcolor="#263449",
    )

    st.plotly_chart(
        fig_price,
        use_container_width=True,
    )

    # --------------------------------------------------------
    # VOLATILITY COMPARISON
    # --------------------------------------------------------

    st.markdown("### 📉 Volatility Comparison")
    fig_volatility = px.bar(
        summary.sort_values(
            "volatility",
            ascending=False,
        ),
        x="company",
        y="volatility",
        title="Daily Return Volatility",
        text="volatility",
    )
    fig_volatility.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
    )
    fig_volatility.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(color="#E5E7EB"),
        xaxis_title="Company",
        yaxis_title="Volatility (%)",
    )
    fig_volatility.update_xaxes(
        showgrid=False,
    )
    fig_volatility.update_yaxes(
        showgrid=True,
        gridcolor="#263449",
    )

    st.plotly_chart(
        fig_volatility,
        use_container_width=True,
    )

    # --------------------------------------------------------
    # TURNOVER COMPARISON
    # --------------------------------------------------------

    st.markdown("### 💹 Trading Turnover Comparison")
    turnover_chart_df = summary.copy()
    turnover_chart_df["turnover_crore"] = (
        turnover_chart_df["total_turnover"]
        / 10_000_000
    )
    fig_turnover = px.bar(
        turnover_chart_df.sort_values(
            "turnover_crore",
            ascending=False,
        ),
        x="company",
        y="turnover_crore",
        title="Total Turnover",
        text="turnover_crore",
    )
    fig_turnover.update_traces(
        texttemplate="₹%{text:.2f} Cr",
        textposition="outside",
    )
    fig_turnover.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(color="#E5E7EB"),
        xaxis_title="Company",
        yaxis_title="Turnover (₹ Crore)",
    )
    fig_turnover.update_xaxes(
        showgrid=False,
    )
    fig_turnover.update_yaxes(
        showgrid=True,
        gridcolor="#263449",
    )

    st.plotly_chart(
        fig_turnover,
        use_container_width=True,
    )

    # --------------------------------------------------------
    # DELIVERY COMPARISON
    # --------------------------------------------------------

    st.markdown("### 📦 Delivery Percentage Comparison")
    fig_delivery = px.bar(
        summary.sort_values(
            "avg_delivery",
            ascending=False,
        ),
        x="company",
        y="avg_delivery",
        title="Average Delivery Percentage",
        text="avg_delivery",
    )
    fig_delivery.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
    )
    fig_delivery.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(color="#E5E7EB"),
        xaxis_title="Company",
        yaxis_title="Delivery (%)",
    )
    fig_delivery.update_xaxes(
        showgrid=False,
    )
    fig_delivery.update_yaxes(
        showgrid=True,
        gridcolor="#263449",
    )

    st.plotly_chart(
        fig_delivery,
        use_container_width=True,
    )

    # --------------------------------------------------------
    # PERFORMANCE TABLE
    # --------------------------------------------------------

    st.markdown("### 📋 Company Performance Summary")
    display_summary = summary[
        [
            "company",
            "period_return",
            "avg_close",
            "highest_close",
            "lowest_close",
            "avg_return",
            "volatility",
            "total_turnover",
            "total_trades",
            "avg_delivery",
        ]
    ].copy()

    display_summary.columns = [
        "Company",
        "Period Return %",
        "Avg Close ₹",
        "Highest Close ₹",
        "Lowest Close ₹",
        "Avg Daily Return %",
        "Volatility %",
        "Total Turnover ₹",
        "Total Trades",
        "Avg Delivery %",
    ]

    display_summary["Period Return %"] = (
        display_summary["Period Return %"].round(2)
    )
    display_summary["Avg Close ₹"] = (
        display_summary["Avg Close ₹"].round(2)
    )
    display_summary["Highest Close ₹"] = (
        display_summary["Highest Close ₹"].round(2)
    )
    display_summary["Lowest Close ₹"] = (
        display_summary["Lowest Close ₹"].round(2)
    )
    display_summary["Avg Daily Return %"] = (
        display_summary["Avg Daily Return %"].round(2)
    )
    display_summary["Volatility %"] = (
        display_summary["Volatility %"].round(2)
    )
    display_summary["Total Turnover ₹"] = (
        display_summary["Total Turnover ₹"].round(0)
    )
    display_summary["Avg Delivery %"] = (
        display_summary["Avg Delivery %"].round(2)
    )

    st.dataframe(
        display_summary,
        use_container_width=True,
        hide_index=True,
    )

# ============================================================
# TRADING & VOLUME
# ============================================================

elif page == "💹 Trading & Volume":
    st.markdown(
        """
        <div class="page-header">
            <h1>💹 Trading & Volume</h1>
            <p>Analyze market liquidity, trading activity, turnover, volume and delivery patterns.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    df = get_all_data()
    if df.empty:
        st.warning("No stock market data available.")
        st.stop()

    df["trade_date"] = pd.to_datetime(df["trade_date"])

    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    st.markdown("### 🔎 Trading Filters")
    filter_col1, filter_col2, filter_col3 = st.columns(
        [1.2, 1.5, 1.2]
    )
    companies = sorted(
        df["company"].dropna().unique().tolist()
    )

    with filter_col1:
        selected_company = st.selectbox(
            "Select Company",
            ["All Companies"] + companies,
            key="trading_company",
        )

    min_date = df["trade_date"].min().date()
    max_date = df["trade_date"].max().date()

    with filter_col2:
        selected_dates = st.date_input(
            "Select Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            key="trading_dates",
        )

    with filter_col3:
        activity_metric = st.selectbox(
            "Activity Metric",
            [
                "Turnover",
                "Number of Trades",
                "Shares Traded",
                "Volume Lakh",
            ],
            key="trading_metric",
        )

    # --------------------------------------------------------
    # APPLY FILTERS
    # --------------------------------------------------------

    trading_df = df.copy()
    if selected_company != "All Companies":
        trading_df = trading_df[
            trading_df["company"] == selected_company
        ].copy()

    if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
        start_date = pd.to_datetime(selected_dates[0])
        end_date = pd.to_datetime(selected_dates[1])
        trading_df = trading_df[
            (trading_df["trade_date"] >= start_date)
            & (trading_df["trade_date"] <= end_date)
        ].copy()

    if trading_df.empty:
        st.warning("No data available for the selected filters.")
        st.stop()

    trading_df = trading_df.sort_values("trade_date")

    # --------------------------------------------------------
    # MARKET ACTIVITY KPIs
    # --------------------------------------------------------

    total_turnover = trading_df["total_turnover"].sum()
    total_trades = trading_df["no_of_trades"].sum()
    total_shares = trading_df["no_of_shares"].sum()
    total_volume_lakh = trading_df["volume_lakh"].sum()
    avg_delivery = trading_df["delivery_percentage"].mean()
    avg_trades = trading_df["no_of_trades"].mean()
    avg_turnover = trading_df["turnover_crore"].mean()
    max_turnover = trading_df["turnover_crore"].max()
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric(
            "Total Turnover",
            f"₹{total_turnover / 10_000_000:,.2f} Cr",
        )
    with k2:
        st.metric(
            "Total Trades",
            f"{total_trades:,.0f}",
        )
    with k3:
        st.metric(
            "Shares Traded",
            f"{total_shares / 1_000_000:,.2f} M",
        )
    with k4:
        st.metric(
            "Avg Delivery",
            f"{avg_delivery:.2f}%",
        )
    k5, k6, k7, k8 = st.columns(4)

    with k5:
        st.metric(
            "Total Volume",
            f"{total_volume_lakh:,.2f} L",
        )
    with k6:
        st.metric(
            "Avg Daily Trades",
            f"{avg_trades:,.0f}",
        )
    with k7:
        st.metric(
            "Avg Daily Turnover",
            f"₹{avg_turnover:,.2f} Cr",
        )
    with k8:
        st.metric(
            "Peak Daily Turnover",
            f"₹{max_turnover:,.2f} Cr",
        )

    st.markdown("---")

    # --------------------------------------------------------
    # DAILY TURNOVER
    # --------------------------------------------------------

    st.markdown("### 💰 Daily Turnover")
    if selected_company == "All Companies":
        daily_turnover = (
            trading_df
            .groupby("trade_date", as_index=False)
            ["turnover_crore"]
            .sum()
        )

    else:
        daily_turnover = trading_df[
            ["trade_date", "turnover_crore"]
        ].copy()

    fig_turnover = px.area(
        daily_turnover,
        x="trade_date",
        y="turnover_crore",
        title="Daily Market Turnover",
    )
    fig_turnover.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(color="#E5E7EB"),
        xaxis_title="Date",
        yaxis_title="Turnover (₹ Crore)",
        hovermode="x unified",
    )
    fig_turnover.update_xaxes(
        showgrid=True,
        gridcolor="#263449",
    )
    fig_turnover.update_yaxes(
        showgrid=True,
        gridcolor="#263449",
    )

    st.plotly_chart(
        fig_turnover,
        use_container_width=True,
    )

    # --------------------------------------------------------
    # TRADING ACTIVITY
    # --------------------------------------------------------

    st.markdown("### 📊 Trading Activity")
    activity_col1, activity_col2 = st.columns(2)
    if selected_company == "All Companies":
        daily_trades = (
            trading_df
            .groupby("trade_date", as_index=False)
            ["no_of_trades"]
            .sum()
        )
        daily_volume = (
            trading_df
            .groupby("trade_date", as_index=False)
            ["volume_lakh"]
            .sum()
        )

    else:
        daily_trades = trading_df[
            ["trade_date", "no_of_trades"]
        ].copy()

        daily_volume = trading_df[
            ["trade_date", "volume_lakh"]
        ].copy()

    with activity_col1:
        fig_trades = px.line(
            daily_trades,
            x="trade_date",
            y="no_of_trades",
            title="Daily Number of Trades",
        )
        fig_trades.update_layout(
            template="plotly_dark",
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            font=dict(color="#E5E7EB"),
            xaxis_title="Date",
            yaxis_title="Number of Trades",
            hovermode="x unified",
        )
        fig_trades.update_xaxes(
            showgrid=True,
            gridcolor="#263449",
        )
        fig_trades.update_yaxes(
            showgrid=True,
            gridcolor="#263449",
        )

        st.plotly_chart(
            fig_trades,
            use_container_width=True,
        )

    with activity_col2:
        fig_volume = px.area(
            daily_volume,
            x="trade_date",
            y="volume_lakh",
            title="Daily Trading Volume",
        )
        fig_volume.update_layout(
            template="plotly_dark",
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            font=dict(color="#E5E7EB"),
            xaxis_title="Date",
            yaxis_title="Volume (Lakh)",
            hovermode="x unified",
        )
        fig_volume.update_xaxes(
            showgrid=True,
            gridcolor="#263449",
        )
        fig_volume.update_yaxes(
            showgrid=True,
            gridcolor="#263449",
        )

        st.plotly_chart(
            fig_volume,
            use_container_width=True,
        )

    # --------------------------------------------------------
    # COMPANY-WISE TRADING ACTIVITY
    # --------------------------------------------------------

    st.markdown("### 🏢 Company-wise Trading Activity")
    company_activity = (
        trading_df
        .groupby("company")
        .agg(
            {
                "turnover_crore": "sum",
                "no_of_trades": "sum",
                "volume_lakh": "sum",
                "no_of_shares": "sum",
                "delivery_percentage": "mean",
            }
        )
        .reset_index()
    )

    company_activity.columns = [
        "Company",
        "Turnover Crore",
        "Total Trades",
        "Volume Lakh",
        "Shares Traded",
        "Avg Delivery %",
    ]

    company_activity = company_activity.sort_values(
        "Turnover Crore",
        ascending=False,
    )
    fig_company_turnover = px.bar(
        company_activity,
        x="Company",
        y="Turnover Crore",
        title="Company-wise Total Turnover",
        text="Turnover Crore",
    )
    fig_company_turnover.update_traces(
        texttemplate="₹%{text:.2f} Cr",
        textposition="outside",
    )
    fig_company_turnover.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(color="#E5E7EB"),
        xaxis_title="Company",
        yaxis_title="Turnover (₹ Crore)",
    )
    fig_company_turnover.update_xaxes(
        showgrid=False,
    )
    fig_company_turnover.update_yaxes(
        showgrid=True,
        gridcolor="#263449",
    )

    st.plotly_chart(
        fig_company_turnover,
        use_container_width=True,
    )

    # --------------------------------------------------------
    # DELIVERY ANALYSIS
    # --------------------------------------------------------

    st.markdown("### 📦 Delivery Analysis")
    delivery_col1, delivery_col2 = st.columns(2)
    with delivery_col1:
        fig_delivery = px.bar(
            company_activity.sort_values(
                "Avg Delivery %",
                ascending=False,
            ),
            x="Company",
            y="Avg Delivery %",
            title="Average Delivery Percentage",
            text="Avg Delivery %",
        )
        fig_delivery.update_traces(
            texttemplate="%{text:.2f}%",
            textposition="outside",
        )
        fig_delivery.update_layout(
            template="plotly_dark",
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            font=dict(color="#E5E7EB"),
            xaxis_title="Company",
            yaxis_title="Delivery (%)",
        )
        fig_delivery.update_xaxes(
            showgrid=False,
        )
        fig_delivery.update_yaxes(
            showgrid=True,
            gridcolor="#263449",
        )

        st.plotly_chart(
            fig_delivery,
            use_container_width=True,
        )

    # --------------------------------------------------------
    # HIGH DELIVERY DAYS
    # --------------------------------------------------------

    high_delivery_df = trading_df[
        trading_df["delivery_percentage"] >= 50
    ].copy()

    if not high_delivery_df.empty:
        if selected_company == "All Companies":
            high_delivery_summary = (
                high_delivery_df
                .groupby("company")
                .size()
                .reset_index(
                    name="High Delivery Days"
                )
            )

        else:
            high_delivery_summary = pd.DataFrame(
                {
                    "company": [selected_company],
                    "High Delivery Days": [
                        len(high_delivery_df)
                    ],
                }
            )
        fig_high_delivery = px.bar(
            high_delivery_summary,
            x="company",
            y="High Delivery Days",
            title="Trading Days With Delivery ≥ 50%",
            text="High Delivery Days",
        )
        fig_high_delivery.update_layout(
            template="plotly_dark",
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            font=dict(color="#E5E7EB"),
            xaxis_title="Company",
            yaxis_title="Number of Days",
        )
        fig_high_delivery.update_xaxes(
            showgrid=False,
        )
        fig_high_delivery.update_yaxes(
            showgrid=True,
            gridcolor="#263449",
        )
        with delivery_col2:
            st.plotly_chart(
                fig_high_delivery,
                use_container_width=True,
            )

    # --------------------------------------------------------
    # MONTHLY TRADING ACTIVITY
    # --------------------------------------------------------

    st.markdown("### 📅 Monthly Trading Activity")
    monthly_activity = (
        trading_df
        .set_index("trade_date")
        .resample("ME")
        .agg(
            {
                "turnover_crore": "sum",
                "no_of_trades": "sum",
                "volume_lakh": "sum",
            }
        )
        .reset_index()
    )
    monthly_activity["Month"] = (
        monthly_activity["trade_date"]
        .dt.strftime("%b %Y")
    )
    fig_monthly = px.bar(
        monthly_activity,
        x="trade_date",
        y="turnover_crore",
        title="Monthly Turnover",
    )
    fig_monthly.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(color="#E5E7EB"),
        xaxis_title="Month",
        yaxis_title="Turnover (₹ Crore)",
        hovermode="x unified",
    )
    fig_monthly.update_xaxes(
        showgrid=False,
    )
    fig_monthly.update_yaxes(
        showgrid=True,
        gridcolor="#263449",
    )

    st.plotly_chart(
        fig_monthly,
        use_container_width=True,
    )

    # --------------------------------------------------------
    # TRADING SUMMARY TABLE
    # --------------------------------------------------------

    st.markdown("### 📋 Trading Summary")
    summary_display = company_activity.copy()
    summary_display["Turnover Crore"] = (
        summary_display["Turnover Crore"].round(2)
    )
    summary_display["Volume Lakh"] = (
        summary_display["Volume Lakh"].round(2)
    )
    summary_display["Avg Delivery %"] = (
        summary_display["Avg Delivery %"].round(2)
    )

    st.dataframe(
        summary_display,
        use_container_width=True,
        hide_index=True,
    )

# ============================================================
# INSIGHTS & RECOMMENDATIONS
# ============================================================

elif page == "💡 Insights & Recommendations":
    st.markdown(
        """
        <div class="page-header">
            <h1>💡 Insights & Recommendations</h1>
            <p>Data-driven observations generated from stock price, return, trading and delivery metrics.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    df = get_all_data()
    if df.empty:
        st.warning("No stock market data available.")
        st.stop()

    df["trade_date"] = pd.to_datetime(df["trade_date"])

    # --------------------------------------------------------
    # COMPANY LEVEL ANALYSIS
    # --------------------------------------------------------

    company_summary = (
        df.groupby("company")
        .agg(
            {
                "close_price": "mean",
                "daily_return_percentage": [
                    "mean",
                    "std",
                ],
                "total_turnover": "sum",
                "no_of_trades": "sum",
                "delivery_percentage": "mean",
                "volume_lakh": "sum",
            }
        )
        .reset_index()
    )

    company_summary.columns = [
        "company",
        "avg_close",
        "avg_return",
        "volatility",
        "total_turnover",
        "total_trades",
        "avg_delivery",
        "total_volume",
    ]

    # --------------------------------------------------------
    # PERIOD RETURNS
    # --------------------------------------------------------

    period_return_list = []
    for company in sorted(df["company"].unique()):
        company_data = df[
            df["company"] == company
        ].sort_values("trade_date")
        first_close = company_data.iloc[0]["close_price"]
        last_close = company_data.iloc[-1]["close_price"]
        period_return = (
            (last_close - first_close)
            / first_close
            * 100
        )
        positive_days = (
            company_data["daily_return_percentage"] > 0
        ).sum()

        total_days = len(company_data)
        positive_day_pct = (
            positive_days / total_days * 100
            if total_days > 0
            else 0
        )
        period_return_list.append(
            {
                "company": company,
                "period_return": period_return,
                "positive_day_pct": positive_day_pct,
            }
        )

    period_df = pd.DataFrame(period_return_list)
    company_summary = company_summary.merge(
        period_df,
        on="company",
        how="left",
    )

    # --------------------------------------------------------
    # MARKET LEVEL METRICS
    # --------------------------------------------------------

    total_records = len(df)
    total_companies = df["company"].nunique()
    market_avg_return = df[
        "daily_return_percentage"
    ].mean()

    market_volatility = df[
        "daily_return_percentage"
    ].std()

    market_delivery = df[
        "delivery_percentage"
    ].mean()

    positive_days = (
        df["daily_return_percentage"] > 0
    ).sum()

    negative_days = (
        df["daily_return_percentage"] < 0
    ).sum()

    flat_days = (
        df["daily_return_percentage"] == 0
    ).sum()

    # --------------------------------------------------------
    # HEADER KPIs
    # --------------------------------------------------------

    st.markdown("### 📊 Market Intelligence Overview")
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric(
            "Companies Analyzed",
            f"{total_companies}",
        )
    with k2:
        st.metric(
            "Avg Daily Return",
            f"{market_avg_return:.2f}%",
        )
    with k3:
        st.metric(
            "Market Volatility",
            f"{market_volatility:.2f}%",
        )
    with k4:
        st.metric(
            "Avg Delivery",
            f"{market_delivery:.2f}%",
        )

    # --------------------------------------------------------
    # KEY INSIGHTS
    # --------------------------------------------------------

    st.markdown("### 🔍 Key Insights")
    highest_return = company_summary.loc[
        company_summary["period_return"].idxmax()
    ]
    lowest_return = company_summary.loc[
        company_summary["period_return"].idxmin()
    ]
    highest_volatility = company_summary.loc[
        company_summary["volatility"].idxmax()
    ]
    lowest_volatility = company_summary.loc[
        company_summary["volatility"].idxmin()
    ]
    highest_turnover = company_summary.loc[
        company_summary["total_turnover"].idxmax()
    ]
    highest_delivery = company_summary.loc[
        company_summary["avg_delivery"].idxmax()
    ]
    highest_positive_days = company_summary.loc[
        company_summary["positive_day_pct"].idxmax()
    ]

    insight_col1, insight_col2 = st.columns(2)
    with insight_col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <h4>📈 Period Return</h4>
                <p><strong>{highest_return['company']}</strong>
                recorded the highest overall price return of
                <strong>{highest_return['period_return']:.2f}%</strong>
                during the available analysis period.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="metric-card">
                <h4>💹 Trading Activity</h4>
                <p><strong>{highest_turnover['company']}</strong>
                recorded the highest cumulative turnover of
                <strong>₹{highest_turnover['total_turnover'] / 10_000_000:,.2f} Cr</strong>.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="metric-card">
                <h4>📦 Delivery Activity</h4>
                <p><strong>{highest_delivery['company']}</strong>
                had the highest average delivery percentage at
                <strong>{highest_delivery['avg_delivery']:.2f}%</strong>.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with insight_col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <h4>📉 Lowest Period Return</h4>
                <p><strong>{lowest_return['company']}</strong>
                recorded the lowest overall price return of
                <strong>{lowest_return['period_return']:.2f}%</strong>
                during the available analysis period.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="metric-card">
                <h4>⚡ Highest Volatility</h4>
                <p><strong>{highest_volatility['company']}</strong>
                showed the highest daily-return volatility at
                <strong>{highest_volatility['volatility']:.2f}%</strong>.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="metric-card">
                <h4>📊 Positive Trading Days</h4>
                <p><strong>{highest_positive_days['company']}</strong>
                had the highest percentage of positive-return trading days:
                <strong>{highest_positive_days['positive_day_pct']:.2f}%</strong>.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------
    # MARKET DAY DISTRIBUTION
    # --------------------------------------------------------

    st.markdown("### 📅 Market Trading-Day Distribution")
    day_distribution = pd.DataFrame(
        {
            "Type": [
                "Positive Days",
                "Negative Days",
                "Flat Days",
            ],
            "Days": [
                positive_days,
                negative_days,
                flat_days,
            ],
        }
    )
    fig_days = px.pie(
        day_distribution,
        names="Type",
        values="Days",
        hole=0.55,
        title="Distribution of Daily Market Returns",
    )
    fig_days.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(color="#E5E7EB"),
    )

    st.plotly_chart(
        fig_days,
        use_container_width=True,
    )

    # --------------------------------------------------------
    # RETURN VS VOLATILITY
    # --------------------------------------------------------

    st.markdown("### 📈 Return vs Volatility")
    fig_risk = px.scatter(
        company_summary,
        x="volatility",
        y="period_return",
        size="total_turnover",
        text="company",
        hover_data=[
            "avg_close",
            "avg_return",
            "avg_delivery",
            "positive_day_pct",
        ],
        title="Period Return vs Daily Volatility",
    )
    fig_risk.update_traces(
        textposition="top center",
    )
    fig_risk.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(color="#E5E7EB"),
        xaxis_title="Daily Volatility (%)",
        yaxis_title="Period Return (%)",
    )
    fig_risk.update_xaxes(
        showgrid=True,
        gridcolor="#263449",
    )
    fig_risk.update_yaxes(
        showgrid=True,
        gridcolor="#263449",
        zeroline=True,
    )

    st.plotly_chart(
        fig_risk,
        use_container_width=True,
    )

    # --------------------------------------------------------
    # POSITIVE DAY ANALYSIS
    # --------------------------------------------------------

    st.markdown("### 📊 Positive Trading-Day Analysis")
    positive_day_df = company_summary[
        [
            "company",
            "positive_day_pct",
        ]
    ].sort_values(
        "positive_day_pct",
        ascending=False,
    )
    fig_positive = px.bar(
        positive_day_df,
        x="company",
        y="positive_day_pct",
        title="Percentage of Positive Trading Days",
        text="positive_day_pct",
    )
    fig_positive.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
    )
    fig_positive.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font=dict(color="#E5E7EB"),
        xaxis_title="Company",
        yaxis_title="Positive Days (%)",
    )
    fig_positive.update_xaxes(
        showgrid=False,
    )
    fig_positive.update_yaxes(
        showgrid=True,
        gridcolor="#263449",
    )

    st.plotly_chart(
        fig_positive,
        use_container_width=True,
    )

    # --------------------------------------------------------
    # AUTOMATED OBSERVATIONS
    # --------------------------------------------------------

    st.markdown("### 🧠 Automated Observations")
    observations = []
    if market_avg_return > 0:
        observations.append(
            f"Average daily market return across the dataset was positive at "
            f"{market_avg_return:.2f}%."
        )
    elif market_avg_return < 0:
        observations.append(
            f"Average daily market return across the dataset was negative at "
            f"{market_avg_return:.2f}%."
        )
    else:
        observations.append(
            "Average daily market return across the dataset was approximately flat."
        )
    observations.append(
        f"{highest_return['company']} recorded the highest period return "
        f"at {highest_return['period_return']:.2f}%."
    )
    observations.append(
        f"{highest_volatility['company']} showed the highest daily-return "
        f"volatility at {highest_volatility['volatility']:.2f}%."
    )
    observations.append(
        f"{highest_turnover['company']} generated the highest cumulative "
        f"turnover during the available period."
    )
    observations.append(
        f"{highest_delivery['company']} recorded the highest average "
        f"delivery percentage at {highest_delivery['avg_delivery']:.2f}%."
    )

    for index, observation in enumerate(
        observations,
        start=1,
    ):
        st.markdown(
            f"""
            <div class="metric-card">
                <p><strong>{index}.</strong> {observation}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --------------------------------------------------------
    # COMPANY INSIGHT TABLE
    # --------------------------------------------------------

    st.markdown("### 📋 Company Insight Summary")
    insight_table = company_summary[
        [
            "company",
            "period_return",
            "positive_day_pct",
            "avg_return",
            "volatility",
            "total_turnover",
            "avg_delivery",
        ]
    ].copy()

    insight_table.columns = [
        "Company",
        "Period Return %",
        "Positive Days %",
        "Avg Daily Return %",
        "Volatility %",
        "Total Turnover ₹",
        "Avg Delivery %",
    ]

    insight_table["Period Return %"] = (
        insight_table["Period Return %"].round(2)
    )
    insight_table["Positive Days %"] = (
        insight_table["Positive Days %"].round(2)
    )
    insight_table["Avg Daily Return %"] = (
        insight_table["Avg Daily Return %"].round(2)
    )
    insight_table["Volatility %"] = (
        insight_table["Volatility %"].round(2)
    )
    insight_table["Total Turnover ₹"] = (
        insight_table["Total Turnover ₹"].round(0)
    )
    insight_table["Avg Delivery %"] = (
        insight_table["Avg Delivery %"].round(2)
    )

    st.dataframe(
        insight_table,
        use_container_width=True,
        hide_index=True,
    )

elif page == "🧪 SQL Playground":

    st.title("🧪 SQL Playground")
    st.caption("Run predefined SQL queries and explore stock market data directly from SQLite.")

    # ========================================================
    # DATABASE INFORMATION
    # ========================================================

    health = database_health_check()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Records",
            f"{health['total_records']:,}"
        )

    with col2:
        st.metric(
            "Companies",
            health["total_companies"]
        )

    with col3:
        st.metric(
            "Start Date",
            health["start_date"]
        )

    with col4:
        st.metric(
            "End Date",
            health["end_date"]
        )

    st.markdown("---")

    # ========================================================
    # IMPORT SQL QUERIES
    # ========================================================

    from utils.queries import (
        SQL_QUERIES,
        QUERY_CATEGORIES
    )

    from utils.database import run_query

    # ========================================================
    # QUERY CATEGORY
    # ========================================================

    category = st.selectbox(
        "Select Query Category",
        list(QUERY_CATEGORIES.keys())
    )

    # ========================================================
    # QUERY SELECTION
    # ========================================================

    category_queries = QUERY_CATEGORIES[category]

    selected_query_name = st.selectbox(
        "Select SQL Query",
        category_queries
    )

    selected_query = SQL_QUERIES[selected_query_name]

    # ========================================================
    # SQL CODE DISPLAY
    # ========================================================

    st.markdown("### 📝 SQL Query")

    st.code(
        selected_query,
        language="sql"
    )

    # ========================================================
    # EXECUTE QUERY
    # ========================================================

    if st.button(
        "▶️ Execute Query",
        use_container_width=True
    ):

        try:

            result = run_query(selected_query)

            st.success("Query executed successfully.")

            # Result statistics
            result_col1, result_col2 = st.columns(2)

            with result_col1:
                st.metric(
                    "Rows Returned",
                    f"{len(result):,}"
                )

            with result_col2:
                st.metric(
                    "Columns Returned",
                    f"{len(result.columns):,}"
                )

            st.markdown("### 📊 Query Result")

            st.dataframe(
                result,
                use_container_width=True,
                hide_index=True
            )

            # ====================================================
            # DOWNLOAD RESULT
            # ====================================================

            csv_data = result.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="⬇️ Download Result as CSV",
                data=csv_data,
                file_name="sql_query_result.csv",
                mime="text/csv",
                use_container_width=True
            )

        except Exception as e:

            st.error(
                f"SQL query execution failed: {e}"
            )

    # ========================================================
    # SQL QUERY CATALOG
    # ========================================================

    st.markdown("---")

    st.markdown("### 📚 SQL Query Catalog")

    catalog_rows = []

    for query_name, query_sql in SQL_QUERIES.items():

        catalog_rows.append({
            "Query": query_name,
            "Category": next(
                (
                    cat
                    for cat, queries in QUERY_CATEGORIES.items()
                    if query_name in queries
                ),
                "Other"
            )
        })

    catalog_df = pd.DataFrame(catalog_rows)

    st.dataframe(
        catalog_df,
        use_container_width=True,
        hide_index=True
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="project-footer">
        <div class="footer-line"></div>
        <div class="footer-content">
            <div>
                <span class="footer-title">
                    SQL - Stock Market Analysis
                </span>
                <span class="footer-separator">•</span>
                <span>
                    Real-World Stock Market Analytics
                </span>
            </div>
            <div class="footer-right">
                Built with Python • SQLite • SQL • Streamlit
            </div>
        </div>
        <div class="footer-bottom">
            Data Analysis • SQL Analytics • Interactive Visualization
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
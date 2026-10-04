import streamlit as st


def apply_theme():
    """
    Premium dark theme.
    Safe for Streamlit + Plotly charts.
    Native sidebar collapse/expand remains enabled.
    """

    st.markdown(
        """
        <style>

        /* =========================================================
           APP BACKGROUND
        ========================================================= */

        .stApp {
            background-color: #0B1120 !important;
        }

        .main {
            background-color: #0B1120 !important;
        }

        .block-container {
            max-width: 100% !important;
            padding-top: 1.8rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
            padding-bottom: 3rem !important;
        }


        /* =========================================================
           MAIN HEADINGS
        ========================================================= */

        h1 {
            color: #F8FAFC !important;
            font-weight: 800 !important;
        }

        h2 {
            color: #F8FAFC !important;
            font-weight: 750 !important;
        }

        h3 {
            color: #F8FAFC !important;
            font-weight: 700 !important;
        }

        h4,
        h5,
        h6 {
            color: #E2E8F0 !important;
        }


        /* =========================================================
           MARKDOWN / NORMAL STREAMLIT TEXT
        ========================================================= */

        .stMarkdown {
            color: #E2E8F0 !important;
        }

        .stMarkdown p {
            color: #E2E8F0 !important;
        }

        .stMarkdown strong {
            color: #F8FAFC !important;
        }

        .stCaption {
            color: #94A3B8 !important;
        }


        /* =========================================================
           SIDEBAR
        ========================================================= */

        section[data-testid="stSidebar"] {
            background-color: #0F172A !important;
        }

        section[data-testid="stSidebar"] > div {
            background-color: #0F172A !important;
        }

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] label {
            color: #E2E8F0 !important;
        }


        /* =========================================================
           SIDEBAR RADIO
        ========================================================= */

        section[data-testid="stSidebar"] .stRadio label {
            color: #CBD5E1 !important;
        }


        /* =========================================================
           METRICS
        ========================================================= */

        [data-testid="stMetric"] {
            background-color: #111827 !important;
            border: 1px solid #1E293B !important;
            border-radius: 14px !important;
            padding: 18px !important;
        }

        [data-testid="stMetricLabel"] {
            color: #94A3B8 !important;
        }

        [data-testid="stMetricValue"] {
            color: #F8FAFC !important;
        }

        [data-testid="stMetricDelta"] {
            color: #CBD5E1 !important;
        }


        /* =========================================================
           BUTTONS
        ========================================================= */

        .stButton > button {
            background-color: #111827 !important;
            color: #F8FAFC !important;
            border: 1px solid #334155 !important;
            border-radius: 10px !important;
        }

        .stButton > button:hover {
            background-color: #1E293B !important;
            color: #FFFFFF !important;
            border-color: #6366F1 !important;
        }


        /* =========================================================
           TEXT INPUT
        ========================================================= */

        .stTextInput input,
        .stTextArea textarea {
            background-color: #111827 !important;
            color: #F8FAFC !important;
            border: 1px solid #334155 !important;
        }

        .stTextInput input::placeholder,
        .stTextArea textarea::placeholder {
            color: #64748B !important;
        }


        /* =========================================================
           SELECTBOX
        ========================================================= */

        div[data-baseweb="select"] > div {
            background-color: #111827 !important;
            border-color: #334155 !important;
        }

        div[data-baseweb="select"] input {
            color: #F8FAFC !important;
        }


        /* =========================================================
           CHECKBOX / RADIO
        ========================================================= */

        .stCheckbox label,
        .stRadio label {
            color: #CBD5E1 !important;
        }


        /* =========================================================
           EXPANDERS
        ========================================================= */

        [data-testid="stExpander"] {
            background-color: #111827 !important;
            border: 1px solid #1E293B !important;
            border-radius: 12px !important;
        }

        [data-testid="stExpander"] summary {
            color: #F8FAFC !important;
        }


        /* =========================================================
           TABS
        ========================================================= */

        button[data-baseweb="tab"] {
            color: #94A3B8 !important;
        }

        button[data-baseweb="tab"][aria-selected="true"] {
            color: #F8FAFC !important;
        }


        /* =========================================================
           DATAFRAME
        ========================================================= */

        [data-testid="stDataFrame"] {
            border: 1px solid #1E293B !important;
            border-radius: 10px !important;
        }


        /* =========================================================
           PLOTLY CHARTS
           IMPORTANT:
           Do NOT apply generic color rules to Plotly.
        ========================================================= */

        .js-plotly-plot {
            width: 100% !important;
        }

        .js-plotly-plot .plot-container {
            width: 100% !important;
        }

        .js-plotly-plot .main-svg {
            background: transparent !important;
        }

        .js-plotly-plot .plotly .bg {
            fill: #111827 !important;
        }

        /* Plotly axis text */

        .js-plotly-plot .xtick text,
        .js-plotly-plot .ytick text {
            fill: #CBD5E1 !important;
        }

        /* Plotly axis titles */

        .js-plotly-plot .xtitle,
        .js-plotly-plot .ytitle {
            fill: #CBD5E1 !important;
        }

        /* Plotly chart title */

        .js-plotly-plot .gtitle {
            fill: #F8FAFC !important;
        }

        /* Plotly legend */

        .js-plotly-plot .legendtext {
            fill: #CBD5E1 !important;
        }

        /* Plotly grid */

        .js-plotly-plot .gridlayer path {
            stroke: #263449 !important;
        }

        .js-plotly-plot .zerolinelayer path {
            stroke: #475569 !important;
        }


        /* =========================================================
           DIVIDERS
        ========================================================= */

        hr {
            border-color: #1E293B !important;
        }


        /* =========================================================
           HEADER
        ========================================================= */

        header[data-testid="stHeader"] {
            background-color: transparent !important;
        }


        /* =========================================================
           HIDE STREAMLIT DEFAULT MENU / FOOTER
        ========================================================= */

        #MainMenu {
            visibility: hidden;
        }

        footer {
            visibility: hidden;
        }

        
        /* ====================================================
        PROJECT FOOTER
        ==================================================== */

        .project-footer {
            margin-top: 50px;
            padding: 20px 0 10px 0;
        }
        .footer-line {
            height: 1px;
            background: #1E293B;
            margin-bottom: 18px;
        }
        .footer-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 20px;
            flex-wrap: wrap;
            font-size: 13px;
            color: #94A3B8;
        }
        .footer-title {
            color: #E5E7EB;
            font-weight: 700;
        }
        .footer-separator {
            margin: 0 8px;
            color: #64748B;
        }
        .footer-right {
            text-align: right;
            color: #64748B;
        }
        .footer-bottom {
            margin-top: 10px;
            font-size: 11px;
            color: #475569;
        }
        @media (max-width: 768px) {

            .footer-content {
                flex-direction: column;
                align-items: flex-start;
            }
            .footer-right {
                text-align: left;
            }
        }

        /* =========================================================
           IMPORTANT:
           NO FIXED SIDEBAR WIDTH
           NATIVE COLLAPSE/EXPAND REMAINS
        ========================================================= */

        </style>
        """,
        unsafe_allow_html=True,
    )
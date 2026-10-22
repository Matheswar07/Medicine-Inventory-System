
import streamlit as st
import pandas as pd
import mysql.connector
from datetime import date
from html import escape

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="MediTrack",
    page_icon="💊",
    layout="wide"
)

# ---------------- DATABASE CONNECTION ----------------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mathesh_29",
        database="medicine_inventory_db",
        port=3306
    )


def format_date_columns_for_display(frame, columns):
    """Format copied date columns consistently for table display."""
    display_frame = frame.copy()
    for column in columns:
        display_frame[column] = (
            pd.to_datetime(display_frame[column], errors="coerce")
            .dt.strftime("%Y-%m-%d")
            .fillna("")
        )
    return display_frame

# ---------------- PAGE HEADER ----------------
st.markdown(
    """
    <style>
    :root {
        color-scheme: dark;
        --primary-color: #2DD4BF;
        --background-color: #0B1220;
        --secondary-background-color: #172338;
        --text-color: #F1F5F9;
    }
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background: #0B1220 !important;
        color: #F1F5F9 !important;
    }
    [data-testid="stHeader"] { background: #0B1220 !important; }
    .block-container {
        max-width: 1440px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3, h4,
    [data-testid="stHeading"],
    [data-testid="stHeading"] * {
        color: #F1F5F9 !important;
    }
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] *,
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] * {
        color: #A9B8CC !important;
    }
    [data-testid="stMain"] label,
    [data-testid="stMain"] label * {
        color: #F1F5F9 !important;
    }
    [data-testid="stMetric"] {
        background: #172338;
        border: 1px solid #2B3A50;
        border-top: 3px solid #2DD4BF;
        border-radius: 14px;
        padding: 1rem 1.1rem;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.18);
    }
    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] * {
        color: #A9B8CC !important;
    }
    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] * {
        color: #F1F5F9 !important;
        font-size: 1.8rem;
        font-weight: 700;
    }
    [data-testid="stDataFrame"] {
        --gdg-bg-cell: #111827;
        --gdg-bg-cell-medium: #172338;
        --gdg-bg-header: #172338;
        --gdg-bg-header-hover: #1D2B42;
        --gdg-text-dark: #F1F5F9;
        --gdg-text-medium: #A9B8CC;
        --gdg-border-color: #2B3A50;
        --gdg-accent-color: #2DD4BF;
        background: #111827;
        border: 1px solid #2B3A50;
        border-radius: 10px;
        overflow: hidden;
    }
    [data-testid="stSidebar"] { background-color: #0D1728; }
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] label * {
        color: #F1F5F9 !important;
    }
    .sidebar-brand {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.45rem 0.35rem 1.15rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid #27364A;
    }
    .sidebar-brand-icon {
        display: flex;
        width: 2.45rem;
        height: 2.45rem;
        align-items: center;
        justify-content: center;
        border-radius: 12px;
        background: #18394A;
        color: #2DD4BF !important;
        font-size: 1.25rem;
    }
    .sidebar-brand-name {
        color: #F1F5F9;
        font-size: 1.05rem;
        font-weight: 750;
        line-height: 1.15;
    }
    .sidebar-brand-subtitle {
        margin-top: 0.25rem;
        color: #91A4BD;
        font-size: 0.62rem;
        font-weight: 650;
        letter-spacing: 0.12em;
    }
    .sidebar-nav-label {
        margin: 0 0 0.55rem 0.45rem;
        color: #91A4BD;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.12em;
    }
    [data-testid="stSidebar"] div.stButton { margin-bottom: 0.32rem; }
    [data-testid="stSidebar"] button[kind="secondary"] {
        justify-content: flex-start;
        min-height: 2.75rem;
        padding-left: 0.8rem;
        background: transparent !important;
        border: 1px solid transparent !important;
        border-left: 3px solid transparent !important;
        border-radius: 10px;
        color: #91A4BD !important;
        text-align: left;
        white-space: nowrap;
        box-shadow: none !important;
    }
    [data-testid="stSidebar"] button[kind="secondary"] * {
        color: #91A4BD !important;
    }
    [data-testid="stSidebar"] button[kind="secondary"]:hover {
        background: rgba(24, 57, 74, 0.55) !important;
        border-color: #27364A !important;
        border-left-color: #42D6C5 !important;
        color: #F1F5F9 !important;
    }
    [data-testid="stSidebar"] button[kind="secondary"]:hover * {
        color: #F1F5F9 !important;
    }
    [data-testid="stSidebar"] button[kind="primary"] {
        justify-content: flex-start;
        min-height: 2.75rem;
        padding-left: 0.8rem;
        background: #18394A !important;
        border: 1px solid #27364A !important;
        border-left: 3px solid #42D6C5 !important;
        border-radius: 10px;
        color: #42D6C5 !important;
        text-align: left;
        white-space: nowrap;
        box-shadow: none !important;
    }
    [data-testid="stSidebar"] button[kind="primary"] * {
        color: #42D6C5 !important;
    }
    [data-testid="stSidebar"] button[kind="primary"]:hover {
        background: #1C4355 !important;
    }
    [data-testid="stSidebar"] button[kind="primary"]:hover * {
        color: #42D6C5 !important;
    }
    div.stButton > button {
        background: #172338 !important;
        border: 1px solid #2B3A50 !important;
        border-radius: 10px;
        color: #F1F5F9 !important;
        font-weight: 600;
        min-height: 2.75rem;
    }
    div.stButton > button * { color: #F1F5F9 !important; }
    div.stButton > button:hover {
        background: #1D2B42 !important;
        border-color: #2DD4BF !important;
        color: #2DD4BF !important;
    }
    div.stButton > button:hover * { color: #2DD4BF !important; }
    [data-baseweb="input"] > div,
    [data-baseweb="select"] > div,
    [data-testid="stDateInput"] input,
    textarea {
        background: #111827 !important;
        border-color: #2B3A50 !important;
        color: #F1F5F9 !important;
    }
    [data-baseweb="input"] input,
    [data-baseweb="select"] *,
    [data-testid="stDateInput"] input,
    textarea {
        color: #F1F5F9 !important;
    }
    [role="listbox"], [role="option"] {
        background: #172338 !important;
        color: #F1F5F9 !important;
    }
    [data-testid="stAlert"] {
        background: #172338 !important;
        border: 1px solid #2B3A50 !important;
        border-radius: 10px;
    }
    [data-testid="stAlert"] p { color: #F1F5F9 !important; }
    .dashboard-table-panel {
        width: 100%;
        box-sizing: border-box;
        overflow: hidden;
        padding: 0.35rem;
        background: #151F30;
        border: 1px solid #34445A;
        border-radius: 12px;
    }
    .dashboard-alert-table {
        width: 100%;
        table-layout: fixed;
        border-collapse: separate;
        border-spacing: 0;
        color: #E2EAF5;
        font-size: 0.82rem;
    }
    .dashboard-alert-table th {
        padding: 0.65rem 0.55rem;
        background: #243247;
        color: #A9B8CC;
        border-bottom: 1px solid #34445A;
        font-weight: 600;
        text-align: left;
        overflow-wrap: anywhere;
    }
    .dashboard-alert-table td {
        padding: 0.62rem 0.55rem;
        background: #1A273A;
        color: #E2EAF5;
        border-bottom: 1px solid #34445A;
        vertical-align: middle;
        overflow-wrap: anywhere;
    }
    .dashboard-alert-table tbody tr:nth-child(even) td {
        background: #202F44;
    }
    .dashboard-alert-table tbody tr:hover td { filter: brightness(1.08); }
    .dashboard-alert-table tbody tr:last-child td { border-bottom: 0; }
    .dashboard-alert-table .status-column { width: 104px; }
    .dashboard-alert-table .batch-column { width: 82px; }
    .dashboard-alert-table .date-column { width: 96px; white-space: nowrap; }
    .dashboard-alert-table .numeric-column {
        width: 72px;
        text-align: right;
        white-space: nowrap;
        font-variant-numeric: tabular-nums;
    }
    .dashboard-alert-table .reorder-column { width: 82px; }
    .dashboard-alert-table .status-cell { white-space: nowrap; }
    .dashboard-alert-table .status-badge {
        display: inline-block;
        padding: 0.2rem 0.42rem;
        border-radius: 999px;
        font-size: 0.72rem;
        font-weight: 700;
    }
    .dashboard-alert-table .status-low-stock {
        color: #FBBF24;
        background: rgba(251, 191, 36, 0.12);
    }
    .dashboard-alert-table .status-expired {
        color: #FB7185;
        background: rgba(251, 113, 133, 0.12);
    }
    .dashboard-alert-table .status-expiring-soon {
        color: #FBBF24;
        background: rgba(251, 191, 36, 0.12);
    }
    .stock-distribution-card {
        width: 100%;
        box-sizing: border-box;
        min-height: 310px;
        padding: 1.1rem 1.15rem;
        background: #151F30;
        border: 1px solid #29384D;
        border-radius: 16px;
    }
    .stock-distribution-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.75rem;
        margin-bottom: 1.2rem;
    }
    .stock-distribution-title {
        color: #E2EAF5;
        font-size: 1rem;
        font-weight: 700;
        letter-spacing: 0.01em;
    }
    .stock-distribution-label {
        color: #A9B8CC;
        font-size: 0.73rem;
        white-space: nowrap;
    }
    .stock-category-row { margin-bottom: 1.15rem; }
    .stock-category-meta {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 0.8rem;
        margin-bottom: 0.45rem;
    }
    .stock-category-name {
        min-width: 0;
        color: #A9B8CC;
        font-size: 0.82rem;
        line-height: 1.25;
        overflow-wrap: anywhere;
    }
    .stock-category-value {
        color: #E2EAF5;
        font-size: 0.82rem;
        font-weight: 650;
        white-space: nowrap;
        font-variant-numeric: tabular-nums;
    }
    .stock-category-track {
        width: 100%;
        height: 8px;
        overflow: hidden;
        background: #29384D;
        border-radius: 999px;
    }
    .stock-category-bar {
        height: 100%;
        background: #42D6C5;
        border-radius: inherit;
    }
    .stock-distribution-empty {
        padding: 1rem 0;
        color: #A9B8CC;
        font-size: 0.86rem;
    }
    .medicine-records-table-wrap {
        width: 100%;
        max-height: 70vh;
        overflow: auto;
        background: #151F30;
        border: 1px solid #34445A;
        border-top: 2px solid #42D6C5;
        border-radius: 12px;
    }
    .medicine-records-table {
        width: max-content;
        min-width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        color: #E5EDF7;
        font-size: 0.86rem;
    }
    .medicine-records-table th {
        position: sticky;
        top: 0;
        z-index: 1;
        padding: 0.72rem 0.8rem;
        background: #24364D;
        color: #C7D8EA;
        border-bottom: 1px solid #34445A;
        font-weight: 650;
        text-align: left;
        white-space: nowrap;
    }
    .medicine-records-table td {
        padding: 0.68rem 0.8rem;
        background: #19283B;
        color: #E5EDF7;
        border-bottom: 1px solid #34445A;
        vertical-align: top;
    }
    .medicine-records-table tbody tr:nth-child(even) td {
        background: #202F44;
    }
    .medicine-records-table tbody tr:hover td {
        box-shadow: inset 0 0 0 9999px rgba(66, 214, 197, 0.045);
    }
    .medicine-records-table tbody tr:last-child td { border-bottom: 0; }
    .medicine-records-table .medicine-name-cell,
    .medicine-records-table .category-cell {
        min-width: 150px;
        max-width: 260px;
        overflow-wrap: anywhere;
    }
    .medicine-records-table .numeric-cell {
        text-align: right;
        white-space: nowrap;
        font-variant-numeric: tabular-nums;
    }
    .medicine-records-table .date-cell { white-space: nowrap; }
    .expiry-alert-table-wrap {
        width: 100%;
        max-height: 60vh;
        overflow: auto;
        background: #151F30;
        border: 1px solid #34445A;
        border-top: 2px solid #42D6C5;
        border-radius: 12px;
    }
    .expiry-alert-table-wrap.expired { border-top-color: #FB7185; }
    .expiry-alert-table-wrap.expiring-soon { border-top-color: #FBBF24; }
    .expiry-alert-table-wrap.safe { border-top-color: #34D399; }
    .expiry-alert-table {
        width: max-content;
        min-width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        color: #E5EDF7;
        font-size: 0.86rem;
    }
    .expiry-alert-table th {
        position: sticky;
        top: 0;
        z-index: 1;
        padding: 0.72rem 0.8rem;
        background: #24364D;
        color: #C7D8EA;
        border-bottom: 1px solid #34445A;
        font-weight: 650;
        text-align: left;
        white-space: nowrap;
    }
    .expiry-alert-table td {
        padding: 0.68rem 0.8rem;
        background: #19283B;
        color: #E5EDF7;
        border-bottom: 1px solid #34445A;
        vertical-align: top;
    }
    .expiry-alert-table tbody tr:nth-child(even) td {
        background: #202F44;
    }
    .expiry-alert-table tbody tr:hover td {
        box-shadow: inset 0 0 0 9999px rgba(66, 214, 197, 0.045);
    }
    .expiry-alert-table tbody tr:last-child td { border-bottom: 0; }
    .expiry-alert-table .medicine-name-cell {
        min-width: 150px;
        max-width: 260px;
        overflow-wrap: anywhere;
    }
    .expiry-alert-table .numeric-cell {
        text-align: right;
        white-space: nowrap;
        font-variant-numeric: tabular-nums;
    }
    .expiry-alert-table .date-cell { white-space: nowrap; }
    .expiry-empty-state {
        padding: 0.85rem 1rem;
        background: #151F30;
        border: 1px solid #34445A;
        border-radius: 10px;
        color: #A9B8CC;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.title("MediTrack")
st.caption("Medicine Inventory Management System")

try:
    conn = None
    database_ready = False
    medicine_columns = [
        "Medicine_ID", "Medicine_Name", "Dosage_Form", "Strength",
        "Unit_Price_INR", "Quantity_In_Stock", "Reorder_Level",
        "Batch_Number", "Packing_Date", "Expiry_Date", "Category"
    ]
    df = pd.DataFrame(columns=medicine_columns)

    # Load records independently so navigation still renders if MySQL fails.
    try:
        conn = get_connection()
        read_cursor = conn.cursor(dictionary=True)
        try:
            read_cursor.execute(
                "SELECT * FROM Medicines ORDER BY Medicine_Name"
            )
            df = pd.DataFrame(
                read_cursor.fetchall(),
                columns=read_cursor.column_names
            )
        finally:
            read_cursor.close()

        missing_columns = [
            column for column in medicine_columns if column not in df.columns
        ]
        if missing_columns:
            raise ValueError(
                "Medicines table is missing required columns: "
                + ", ".join(missing_columns)
            )
        database_ready = True
    except mysql.connector.Error as error:
        st.error("Could not connect to MySQL or read the Medicines table.")
        st.info(
            "Check that MySQL Server is running and the database and "
            "Medicines table are available."
        )
        st.exception(error)
        if conn is not None:
            try:
                conn.close()
            except mysql.connector.Error:
                pass
            conn = None
        df = pd.DataFrame(columns=medicine_columns)
    except Exception as error:
        st.error(
            "Could not load medicine records. The selected page is still "
            "available."
        )
        st.exception(error)
        if conn is not None:
            try:
                conn.close()
            except mysql.connector.Error:
                pass
            conn = None
        df = pd.DataFrame(columns=medicine_columns)

    today = pd.Timestamp(date.today())
    df["Expiry_Date"] = pd.to_datetime(df["Expiry_Date"], errors="coerce")
    df["Packing_Date"] = pd.to_datetime(df["Packing_Date"], errors="coerce")

    expired = df["Expiry_Date"] < today
    expiring_soon = (
        (df["Expiry_Date"] >= today)
        & (df["Expiry_Date"] <= today + pd.Timedelta(days=30))
    )
    low_stock = df["Quantity_In_Stock"] <= df["Reorder_Level"]

    # ---------------- SIDEBAR ----------------
    navigation_items = [
        ("Dashboard", ":material/dashboard:"),
        ("View Medicines", ":material/medication:"),
        ("Expiry Alerts", ":material/event_busy:"),
        ("Stock Management", ":material/inventory_2:"),
        ("Add Medicine", ":material/add_circle:")
    ]

    def select_page(page_name):
        st.session_state["active_page"] = page_name

    valid_pages = [label for label, _ in navigation_items]
    if st.session_state.get("active_page") not in valid_pages:
        st.session_state["active_page"] = "Dashboard"

    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-brand">
                <div class="sidebar-brand-icon">💊</div>
                <div>
                    <div class="sidebar-brand-name">MediTrack</div>
                    <div class="sidebar-brand-subtitle">
                        INVENTORY MANAGEMENT
                    </div>
                </div>
            </div>
            <div class="sidebar-nav-label">WORKSPACE</div>
            """,
            unsafe_allow_html=True
        )
        for destination, icon in navigation_items:
            st.button(
                destination,
                key=f"sidebar_nav_{destination.lower().replace(' ', '_')}",
                type=(
                    "primary"
                    if st.session_state["active_page"] == destination
                    else "secondary"
                ),
                icon=icon,
                use_container_width=True,
                on_click=select_page,
                args=(destination,)
            )

    page = st.session_state["active_page"]

    # ---------------- DASHBOARD ----------------
    if page == "Dashboard":
        st.subheader("Welcome to your inventory")
        st.write(
            "Here is a current snapshot of your medicine stock and the "
            "items that need attention."
        )

        st.markdown("#### Quick actions")
        action_columns = st.columns(4)
        destinations = [
            ("Add Medicine", "Add Medicine"),
            ("View Medicines", "View Medicines"),
            ("Stock Management", "Stock Management"),
            ("Expiry Alerts", "Expiry Alerts")
        ]
        for action_column, (label, destination) in zip(
            action_columns, destinations
        ):
            action_column.button(
                label,
                key=f"dashboard_{destination.lower().replace(' ', '_')}",
                use_container_width=True,
                on_click=lambda target=destination: st.session_state.update(
                    {"active_page": target}
                )
            )

        total_records = len(df)
        usable_stock = int(
            pd.to_numeric(
                df.loc[~expired, "Quantity_In_Stock"], errors="coerce"
            ).fillna(0).sum()
        )
        low_stock_count = int(low_stock.sum())
        expiry_alert_count = int(expired.sum() + expiring_soon.sum())

        st.markdown("#### Inventory overview")
        kpi_columns = st.columns(4)
        kpi_columns[0].metric("Total medicine records", f"{total_records:,}")
        kpi_columns[1].metric("Usable stock units", f"{usable_stock:,}")
        kpi_columns[2].metric("Low-stock medicines", f"{low_stock_count:,}")
        kpi_columns[3].metric(
            "Expired or expiring soon", f"{expiry_alert_count:,}",
            help=(
                f"{int(expired.sum())} expired and "
                f"{int(expiring_soon.sum())} expiring within 30 days."
            )
        )

        st.divider()

        def render_dashboard_alert_table(table):
            column_classes = {
                "Status": "status-column",
                "Batch_Number": "batch-column",
                "Expiry_Date": "date-column",
                "Quantity_In_Stock": "numeric-column",
                "Reorder_Level": "numeric-column reorder-column"
            }
            badge_classes = {
                "Low stock": "status-low-stock",
                "Expired": "status-expired",
                "Expiring soon": "status-expiring-soon"
            }
            table_html = [
                '<div class="dashboard-table-panel">',
                '<table class="dashboard-alert-table">',
                "<thead><tr>"
            ]
            for column in table.columns:
                classes = column_classes.get(column, "")
                table_html.append(
                    f'<th class="{classes}">'
                    f"{escape(str(column).replace('_', ' '))}</th>"
                )
            table_html.append("</tr></thead><tbody>")

            for row in table.itertuples(index=False, name=None):
                table_html.append("<tr>")
                for column, value in zip(table.columns, row):
                    text = "" if pd.isna(value) else str(value)
                    classes = column_classes.get(column, "")
                    if column == "Status":
                        badge_class = badge_classes.get(text, "")
                        table_html.append(
                            '<td class="status-column status-cell">'
                            f'<span class="status-badge {badge_class}">'
                            f"{escape(text)}</span></td>"
                        )
                    else:
                        table_html.append(
                            f'<td class="{classes}">{escape(text)}</td>'
                        )
                table_html.append("</tr>")

            table_html.append("</tbody></table></div>")
            st.markdown("".join(table_html), unsafe_allow_html=True)

        chart_column, alerts_column = st.columns([1.2, 1])

        with chart_column:
            if df.empty:
                chart_data = pd.Series(dtype="int64")
            else:
                chart_data = (
                    df.assign(Category=df["Category"].fillna("Uncategorized"))
                    .groupby("Category")["Quantity_In_Stock"]
                    .sum()
                    .sort_values(ascending=False)
                )

            category_rows = []
            if not chart_data.empty:
                highest_stock = float(chart_data.max())
                for category, stock_units in chart_data.items():
                    stock_value = float(stock_units)
                    relative_width = (
                        min(100.0, max(0.0, stock_value / highest_stock * 100))
                        if highest_stock > 0
                        else 0.0
                    )
                    stock_label = (
                        f"{int(stock_units):,}"
                        if stock_value.is_integer()
                        else f"{stock_value:,.2f}"
                    )
                    category_rows.append(
                        '<div class="stock-category-row">'
                        '<div class="stock-category-meta">'
                        '<span class="stock-category-name">'
                        f"{escape(str(category))}</span>"
                        '<span class="stock-category-value">'
                        f"{stock_label} units</span></div>"
                        '<div class="stock-category-track">'
                        f'<div class="stock-category-bar" '
                        f'style="width: {relative_width:.2f}%"></div>'
                        "</div></div>"
                    )

            category_content = "".join(category_rows)
            if not category_content:
                category_content = (
                    '<div class="stock-distribution-empty">'
                    "No category stock data is available yet.</div>"
                )
            stock_distribution_html = (
                '<div class="stock-distribution-card">'
                '<div class="stock-distribution-header">'
                '<span class="stock-distribution-title">'
                "Stock distribution</span>"
                '<span class="stock-distribution-label">'
                "By category</span></div>"
                f"{category_content}</div>"
            )
            with st.container(height=350, border=False):
                st.markdown(
                    stock_distribution_html,
                    unsafe_allow_html=True
                )

        with alerts_column:
            st.subheader("Low-stock medicines")
            low_stock_records = df.loc[
                low_stock,
                ["Medicine_Name", "Quantity_In_Stock", "Reorder_Level"]
            ].sort_values("Quantity_In_Stock").head(5)
            if low_stock_records.empty:
                st.success("No medicines are below their reorder level.")
            else:
                low_stock_records.insert(0, "Status", "Low stock")
                render_dashboard_alert_table(low_stock_records)

            st.subheader("Expiry alerts")
            expiry_alert_mask = expired | expiring_soon
            expiry_alerts = df.loc[
                expiry_alert_mask,
                ["Medicine_Name", "Batch_Number", "Expiry_Date",
                 "Quantity_In_Stock"]
            ].copy().sort_values("Expiry_Date")
            if expiry_alerts.empty:
                st.success("No expired or soon-to-expire medicines.")
            else:
                expiry_alerts.insert(
                    0,
                    "Status",
                    [
                        "Expired" if expired.loc[index]
                        else "Expiring soon"
                        for index in expiry_alerts.index
                    ]
                )
                expiry_alerts = format_date_columns_for_display(
                    expiry_alerts, ["Expiry_Date"]
                )
                render_dashboard_alert_table(expiry_alerts.head(5))

    # ---------------- VIEW MEDICINES ----------------
    elif page == "View Medicines":
        st.subheader("Medicine Records")

        search_method = st.selectbox(
            "Search by",
            ["Medicine Name", "Medicine ID", "Batch Number"]
        )
        search_keys = {
            "Medicine Name": "search_medicine_name",
            "Medicine ID": "search_medicine_id",
            "Batch Number": "search_batch_number"
        }

        if st.button("Clear search"):
            for key in search_keys.values():
                st.session_state[key] = ""

        search = st.text_input(
            f"Enter {search_method.lower()}",
            key=search_keys[search_method]
        ).strip()
        result = df.copy()

        if search:
            if search_method == "Medicine Name":
                result = result[
                    result["Medicine_Name"].str.contains(
                        search, case=False, na=False, regex=False
                    )
                ]
            elif search_method == "Medicine ID":
                if search.isdigit():
                    result = result[
                        pd.to_numeric(
                            result["Medicine_ID"], errors="coerce"
                        ) == int(search)
                    ]
                else:
                    result = result.iloc[0:0]
            else:
                result = result[
                    result["Batch_Number"].str.contains(
                        search, case=False, na=False, regex=False
                    )
                ]

        if result.empty:
            st.info("No medicines found. Try another search.")
        else:
            display_result = format_date_columns_for_display(
                result, ["Packing_Date", "Expiry_Date"]
            )

            column_classes = {
                "Medicine_Name": "medicine-name-cell",
                "Category": "category-cell",
                "Medicine_ID": "numeric-cell",
                "Quantity_In_Stock": "numeric-cell",
                "Reorder_Level": "numeric-cell",
                "Unit_Price_INR": "numeric-cell",
                "Packing_Date": "date-cell",
                "Expiry_Date": "date-cell"
            }
            table_html = [
                '<div class="medicine-records-table-wrap">',
                '<table class="medicine-records-table">',
                "<thead><tr>"
            ]
            for column in display_result.columns:
                classes = column_classes.get(column, "")
                table_html.append(
                    f'<th class="{classes}">{escape(str(column))}</th>'
                )
            table_html.append("</tr></thead><tbody>")

            for row in display_result.itertuples(index=False, name=None):
                table_html.append("<tr>")
                for column, value in zip(display_result.columns, row):
                    cell_text = "" if pd.isna(value) else str(value)
                    classes = column_classes.get(column, "")
                    table_html.append(
                        f'<td class="{classes}">{escape(cell_text)}</td>'
                    )
                table_html.append("</tr>")

            table_html.append("</tbody></table></div>")
            st.markdown("".join(table_html), unsafe_allow_html=True)
            st.caption(f"{len(result)} medicine record(s) found.")

    # ---------------- EXPIRY ALERTS ----------------
    elif page == "Expiry Alerts":
        st.subheader("Expiry Tracking")

        expiry_dates = pd.to_datetime(
            df["Expiry_Date"], errors="coerce"
        ).dt.normalize()
        today = pd.Timestamp(date.today()).normalize()
        days_to_expiry = (expiry_dates - today).dt.days

        expiry_groups = [
            ("Expired", days_to_expiry < 0),
            (
                "Expiring in 30 Days",
                (days_to_expiry >= 0) & (days_to_expiry <= 30)
            )
        ]

        metric_columns = st.columns(2)
        for metric_column, (label, mask) in zip(metric_columns, expiry_groups):
            metric_column.metric(label, int(mask.sum()))

        expiry_columns = [
            "Medicine_ID", "Medicine_Name", "Batch_Number",
            "Expiry_Date", "Quantity_In_Stock"
        ]
        for label, mask in expiry_groups:
            st.subheader(label)
            category_records = df.loc[mask, expiry_columns].copy()
            category_records = category_records.sort_values("Expiry_Date")
            category_records = format_date_columns_for_display(
                category_records, ["Expiry_Date"]
            )
            if category_records.empty:
                st.markdown(
                    f'<div class="expiry-empty-state">'
                    f'No medicines currently in {escape(label.lower())}.'
                    "</div>",
                    unsafe_allow_html=True
                )
                continue

            category_class = {
                "Expired": "expired",
                "Expiring in 30 Days": "expiring-soon",
                "Expiring in 31–90 Days": "safe",
                "Safe for Now": "safe"
            }.get(label, "")
            column_classes = {
                "Medicine_ID": "numeric-cell",
                "Medicine_Name": "medicine-name-cell",
                "Expiry_Date": "date-cell",
                "Quantity_In_Stock": "numeric-cell"
            }
            table_html = [
                f'<div class="expiry-alert-table-wrap {category_class}">',
                '<table class="expiry-alert-table">',
                "<thead><tr>"
            ]
            for column in category_records.columns:
                classes = column_classes.get(column, "")
                table_html.append(
                    f'<th class="{classes}">'
                    f'{escape(str(column).replace("_", " "))}</th>'
                )
            table_html.append("</tr></thead><tbody>")

            for row in category_records.itertuples(index=False, name=None):
                table_html.append("<tr>")
                for column, value in zip(category_records.columns, row):
                    cell_text = "" if pd.isna(value) else str(value)
                    classes = column_classes.get(column, "")
                    table_html.append(
                        f'<td class="{classes}">{escape(cell_text)}</td>'
                    )
                table_html.append("</tr>")

            table_html.append("</tbody></table></div>")
            st.markdown("".join(table_html), unsafe_allow_html=True)

        missing_expiry_count = int(expiry_dates.isna().sum())
        if missing_expiry_count:
            st.warning(
                f"{missing_expiry_count} medicine record(s) have no valid "
                "expiry date and are not included in these categories."
            )

    # ---------------- STOCK MANAGEMENT ----------------
    elif page == "Stock Management":
        st.subheader("Update Medicine Stock")

        if not database_ready:
            st.info("Stock management is unavailable until MySQL reconnects.")
        else:
            medicine_options = dict(
                zip(df["Medicine_Name"], df["Medicine_ID"])
            )

            if not medicine_options:
                st.info("Add a medicine record before updating stock.")
            else:
                selected = st.selectbox(
                    "Select medicine",
                    list(medicine_options.keys())
                )

                medicine_id = int(medicine_options[selected])
                current = int(
                    df.loc[df["Medicine_ID"] == medicine_id,
                           "Quantity_In_Stock"].iloc[0]
                )

                st.write(f"Current recorded stock: **{current} units**")

                with st.form("stock_form"):
                    movement = st.radio(
                        "Stock action",
                        ["Add stock", "Remove stock"]
                    )
                    quantity = st.number_input(
                        "Quantity",
                        min_value=1,
                        step=1
                    )
                    submitted = st.form_submit_button("Update Stock")

                    if submitted:
                        if movement == "Remove stock" and quantity > current:
                            st.error(
                                "You cannot remove more than the recorded stock."
                            )
                        else:
                            new_quantity = (
                                current + quantity
                                if movement == "Add stock"
                                else current - quantity
                            )

                            cursor = conn.cursor()
                            cursor.execute(
                                """
                                UPDATE Medicines
                                SET Quantity_In_Stock = %s
                                WHERE Medicine_ID = %s
                                """,
                                (new_quantity, medicine_id)
                            )
                            conn.commit()
                            cursor.close()

                            st.success(
                                f"Stock updated to {new_quantity} units. "
                                "Refresh the page to see the latest totals."
                            )

    # ---------------- ADD MEDICINE ----------------
    elif page == "Add Medicine":
        st.subheader("Add a New Medicine")

        if not database_ready:
            st.warning("Medicine entry is unavailable until MySQL reconnects.")

        with st.form("add_medicine_form"):
            name = st.text_input("Medicine name")
            form = st.selectbox(
                "Dosage form",
                ["Tablet", "Capsule", "Syrup", "Cream",
                 "Inhaler", "Sachet", "Solution", "Other"]
            )
            strength = st.text_input("Strength")
            price = st.number_input(
                "Unit price (₹)", min_value=0.0, step=0.5
            )
            quantity = st.number_input(
                "Quantity in stock", min_value=0, step=1
            )
            reorder = st.number_input(
                "Reorder level", min_value=0, value=10, step=1
            )
            batch = st.text_input("Batch number")
            packing = st.date_input("Packing date", value=date.today())
            expiry = st.date_input("Expiry date")
            category = st.text_input("Category")

            submitted = st.form_submit_button(
                "Save Medicine", disabled=not database_ready
            )

            if submitted:
                if not name.strip() or not batch.strip():
                    st.error("Medicine name and batch number are required.")
                elif packing > expiry:
                    st.error("Packing date cannot be after expiry date.")
                elif expiry < date.today():
                    st.error("Please check the expiry date before adding.")
                else:
                    cursor = None
                    try:
                        cursor = conn.cursor()
                        cursor.execute(
                            """
                            SELECT 1 FROM Medicines
                            WHERE Medicine_Name = %s AND Batch_Number = %s
                            LIMIT 1
                            """,
                            (name.strip(), batch.strip())
                        )

                        if cursor.fetchone():
                            st.warning(
                                "This medicine with the same batch number "
                                "already exists."
                            )
                        else:
                            cursor.execute(
                                """
                                INSERT INTO Medicines (
                                    Medicine_Name, Dosage_Form, Strength,
                                    Unit_Price_INR, Quantity_In_Stock,
                                    Reorder_Level, Batch_Number,
                                    Packing_Date, Expiry_Date, Category
                                )
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                """,
                                (
                                    name.strip(), form, strength.strip(),
                                    price, quantity, reorder, batch.strip(),
                                    packing, expiry, category.strip()
                                )
                            )
                            conn.commit()
                            st.success("Medicine added successfully!")
                    except mysql.connector.Error as error:
                        conn.rollback()
                        st.error(
                            "Could not add medicine due to a database error: "
                            f"{error}"
                        )
                    finally:
                        if cursor is not None:
                            cursor.close()
                    

    if conn is not None:
        conn.close()

except mysql.connector.Error as error:
    st.error("Could not connect to MySQL or read the database.")
    st.info(
        "Check that MySQL Server is running, the database and table "
        "exist, and the password in app.py is correct."
    )
    st.exception(error)

except Exception as error:
    st.error("Something went wrong while loading the dashboard.")
    st.exception(error)

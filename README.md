# Institutional Stock Analysis & Portfolio Manager

A robust, modular web application built with **Python**, **Streamlit**, and **SQLAlchemy** designed for institutional-grade stock analysis and dynamic portfolio management.

## 🏗️ Architecture & Tech Stack

This project follows a clean, component-based architecture isolating the UI, database, logic, and data abstraction layers.

- **Frontend / UI:** Streamlit (v1.40+) with `plotly` for advanced charting.
- **Backend Framework:** Python (Modular).
- **Database:** SQLite initialized via SQLAlchemy ORM mapping (`models.py`, `db.py`).
- **Authentication:** Role-based local session management using `bcrypt` for secure hashing.
- **Data Source:** `yfinance` for realtime market and fundamental data access.

### 📁 Project Structure

```text
P03-PortfolioManager/
│
├── app.py                      # Main entry point (Streamlit App Layout)
├── requirements.txt            # Python environment dependencies
│
├── database/
│   ├── db.py                   # Engine initialization and session builder
│   └── models.py               # SQLAlchemy Tables (User, Portfolio, Watchlist, AnalysisHistory)
│
├── auth/
│   ├── auth_utils.py           # Bcrypt hashing utilities
│   ├── login.py                # UI Login Component
│   └── register.py             # UI Registration Component
│
├── modules/
│   ├── analysis_engine.py      # Core wrapper running technical vs fundamental scores
│   ├── history.py              # CRUD for historical execution snapshots
│   ├── indicators.py           # Mathematical modeling (RSI, DMAs, Support/Resistance)
│   ├── portfolio.py            # Tab 2: Dashboard visualization and P&L tracking
│   ├── stock_analysis.py       # Tab 1: On-demand stock evaluation layouts
│   ├── watchlist.py            # CRUD logic against the Watchlist table
│   └── watchlist_ui.py         # Tab 3: Intelligent searching and tracking UI
│
└── utils/
    ├── data_fetcher.py         # YFinance integrations and fallbacks
    ├── scoring.py              # Quantitative scoring criteria logic
    └── stock_list.py           # NSE lookup index dictionary
```

## ⚙️ How It Works

### 1. Data Ingestion & Scoring Logic
The **Analysis Engine** fetches real-time quote structures from `yfinance`.
- `compute_fundamental_score`: Uses trailing PE, ROE, Revenue Growth, and Margins to synthesize a 0-10 grade.
- `compute_technical_signal`: Validates 50/200 Day Moving Averages and 14-day RSI (relative strength index).
These components are piped together to resolve a simple **BUY / HOLD / SELL** final recommendation.

### 2. Portfolio Layer
User holdings (`Portfolio` table) are iteratively priced. Weightings determine if any single asset breaches the **40% Allocation Rule**, generating actionable rebalancing alerts dynamically.

### 3. Intelligence Layer
The **Watchlist** uses partial string searching mapping localized queries (e.g., `"infosys"`) to exchange tickers. Users can capture point-in-time assessments saving the exact pricing, score, and technical states for historical comparisons against the `AnalysisHistory` schemas.

## 🚀 Setup Instructions

1. Clone or download the repository to your local machine.
2. Setup a clean virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```
   *The SQLite database (`portfolio_manager.db`) will auto-generate seamlessly.*

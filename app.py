import re
from datetime import datetime

import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import google.generativeai as genai

# ==================================
# PAGE CONFIG
# ==================================

st.set_page_config(
    page_title="Stock AI Assistant",
    page_icon="📈",
    layout="wide"
)

# ==================================
# CUSTOM CSS
# ==================================

st.markdown("""
<style>

.stApp{
    background: linear-gradient(
        135deg,
        #FFD54F,
        #FFEB3B
    );
}

.stock-banner{
    padding:25px;
    border-radius:20px;
    background: linear-gradient(135deg,#1e3a8a,#2563eb);
    color:white;
    text-align:center;
    margin-bottom:20px;
    box-shadow:0px 8px 20px rgba(0,0,0,0.3);
}

.metric-card{
    background:rgba(255,255,255,0.08);
    border-radius:15px;
    padding:20px;
    color:white;        
    text-align:center;
    backdrop-filter: blur(20px);
}

h1,h2,h3,p,label{
    color:black;
}

</style>
""", unsafe_allow_html=True)

# ==================================
# GEMINI CONFIG
# ==================================

GEMINI_API_KEY = "API_KEY_HERE"  # Replace with your actual Gemini API key

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

# ==================================
# STOCK MAPPING
# ==================================

COMPANY_MAP = {
    "TCS": "TCS.NS",
    "TATA CONSULTANCY SERVICES": "TCS.NS",
    "INFOSYS": "INFY.NS",
    "INFY": "INFY.NS",
    "RELIANCE": "RELIANCE.NS",
    "HDFC BANK": "HDFCBANK.NS",
    "ICICI BANK": "ICICIBANK.NS",
    "SBI": "SBIN.NS",
    "WIPRO": "WIPRO.NS",
    "APPLE": "AAPL",
    "MICROSOFT": "MSFT",
    "GOOGLE": "GOOGL",
    "AMAZON": "AMZN",
    "TESLA": "TSLA",
    "NVIDIA": "NVDA"
}

# ==================================
# HELPERS
# ==================================

def get_valid_ticker(text):
    text = text.upper().strip()

    if text in COMPANY_MAP:
        return COMPANY_MAP[text]

    ticker = re.sub(r"[^A-Z.]", "", text)

    try:
        data = yf.Ticker(ticker).history(period="5d")

        if not data.empty:
            return ticker

        data = yf.Ticker(f"{ticker}.NS").history(period="5d")

        if not data.empty:
            return f"{ticker}.NS"

    except:
        pass

    return None


def get_stock_data(ticker):
    try:
        data = yf.Ticker(ticker).history(period="1y")

        if data.empty:
            return None

        return data

    except:
        return None


def calculate_rsi(close):
    delta = close.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(com=13, adjust=False).mean()
    avg_loss = loss.ewm(com=13, adjust=False).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return round(rsi.iloc[-1], 2)


def calculate_macd(close):
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()

    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()

    return round(macd.iloc[-1], 2), round(signal.iloc[-1], 2)

# ==================================
# SIDEBAR
# ==================================

st.sidebar.title("📊 Dashboard")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "AI Analysis",
        "Chat Assistant"
    ]
)

selected_stock = st.sidebar.text_input(
    "Enter Company or Ticker",
    value="TCS"
)

st.sidebar.markdown("---")

watchlist = st.sidebar.multiselect(
    "⭐ Watchlist",
    [
        "AAPL",
        "MSFT",
        "TSLA",
        "NVDA",
        "TCS.NS",
        "INFY.NS"
    ]
)

st.sidebar.markdown("### Live Watchlist")

for stock in watchlist:
    try:
        p = yf.Ticker(stock).history(period="1d")

        if not p.empty:
            price = p["Close"].iloc[-1]
            st.sidebar.write(f"{stock}: ${price:.2f}")

    except:
        pass

# ==================================
# HEADER
# ==================================

st.markdown("""
<div class="stock-banner">
<h1>📈 AI Stock Market Assistant</h1>
<p>Real-Time Analysis • Technical Indicators • AI Insights</p>
</div>
""", unsafe_allow_html=True)

# ==================================
# MARKET STATUS
# ==================================

hour = datetime.now().hour

if 9 <= hour <= 16:
    st.success("🟢 Market Session Active")
else:
    st.error("🔴 Market Session Closed")

# ==================================
# STOCK DATA
# ==================================

ticker = get_valid_ticker(selected_stock)

if ticker:

    with st.spinner("Fetching stock data..."):

        data = get_stock_data(ticker)

        if data is not None:

            close_price = round(data["Close"].iloc[-1], 2)

            rsi = calculate_rsi(data["Close"])

            macd, signal = calculate_macd(data["Close"])

            info = yf.Ticker(ticker).info

            company_name = info.get("longName", ticker)

            st.subheader(company_name)

            # =====================
            # METRIC CARDS
            # =====================

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown(f"""
                <div class="metric-card">
                <h3>💰 Price</h3>
                <h2>${close_price}</h2>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"""
                <div class="metric-card">
                <h3>📊 RSI</h3>
                <h2>{rsi}</h2>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div class="metric-card">
                <h3>📈 MACD</h3>
                <h2>{macd}</h2>
                </div>
                """, unsafe_allow_html=True)

            # =====================
            # RSI GAUGE
            # =====================

            gauge = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=rsi,
                    title={"text": "RSI"},
                    gauge={
                        "axis": {"range": [0, 100]}
                    }
                )
            )

            st.plotly_chart(gauge, use_container_width=True)

            # =====================
            # CHART
            # =====================

            chart = go.Figure()

            chart.add_trace(
                go.Candlestick(
                    x=data.index,
                    open=data["Open"],
                    high=data["High"],
                    low=data["Low"],
                    close=data["Close"]
                )
            )

            chart.update_layout(height=600)

            # =====================
            # TABS
            # =====================

            tab1, tab2, tab3 = st.tabs(
                [
                    "📊 Chart",
                    "🏢 Company",
                    "🤖 AI Analysis"
                ]
            )

            with tab1:
                st.plotly_chart(chart, use_container_width=True)

            with tab2:

                st.write(
                    info.get(
                        "longBusinessSummary",
                        "No description available."
                    )
                )

            with tab3:

                if st.button("Generate AI Analysis"):

                    with st.spinner("Analyzing stock..."):

                        prompt = f"""
                        Analyze this stock:

                        Company: {company_name}
                        Ticker: {ticker}

                        Current Price: {close_price}
                        RSI: {rsi}
                        MACD: {macd}
                        Signal: {signal}

                        Provide:
                        - Trend
                        - Momentum
                        - Risk
                        - Short-term outlook
                        """

                        response = model.generate_content(prompt)

                        st.write(response.text)

            
# ==================================
# CHAT ASSISTANT
# ==================================

st.divider()

st.subheader("💬 Ask the AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_prompt = st.chat_input(
    "Ask a stock market question..."
)

if user_prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_prompt
        }
    )

    with st.chat_message("user"):
        st.write(user_prompt)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = model.generate_content(
                f"""
                You are an expert stock market analyst.

                Provide:
                - Clear explanations
                - Technical analysis
                - Risks
                - Important disclaimers

                User Question:
                {user_prompt}
                """
            )

            st.write(response.text)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response.text
        }
    )
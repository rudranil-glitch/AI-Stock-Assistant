📈 AI Stock Market Assistant

An AI-powered Stock Market Analysis Dashboard built with Streamlit, Yahoo Finance, Plotly, and Google Gemini AI. The application provides real-time stock insights, technical indicators, interactive charts, AI-generated analysis, and a stock market chatbot.

🚀 Features
📊 Real-Time Stock Analysis
Fetches live stock data using Yahoo Finance
Supports both Indian and US stocks
Automatic company-to-ticker mapping
Displays current stock price and company information
📈 Technical Indicators
Relative Strength Index (RSI)
Moving Average Convergence Divergence (MACD)
Momentum analysis
Trend evaluation
📉 Interactive Stock Charts
Candlestick chart visualization
One-year historical stock data
Interactive Plotly dashboard
🤖 AI-Powered Analysis
Uses Google Gemini AI for stock insights
Generates:
Trend analysis
Momentum evaluation
Risk assessment
Short-term outlook
💬 AI Chat Assistant
Ask stock market questions in natural language
Receive AI-generated explanations
Technical analysis support
Investment risk awareness
⭐ Watchlist
Track multiple stocks
View live stock prices from the sidebar
Quick access to favorite stocks
🎨 Modern UI
Responsive Streamlit interface
Custom styling and dashboard layout
Interactive metrics and gauges
🛠️ Technologies Used
Python
Streamlit
Yahoo Finance (yfinance)
Plotly
Google Gemini AI
Pandas
Datetime
Regular Expressions (re)
📂 Project Structure
AI-Stock-Market-Assistant/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
⚙️ Installation
1. Clone the Repository
git clone https://github.com/your-username/AI-Stock-Market-Assistant.git
cd AI-Stock-Market-Assistant
2. Install Dependencies
pip install -r requirements.txt
📦 Requirements

Create a requirements.txt file containing:

streamlit
yfinance
plotly
google-generativeai
pandas
🔑 Configure Gemini API Key

Replace the API key in the code:

GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

Or preferably use Streamlit Secrets:

# .streamlit/secrets.toml

GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

And load it using:

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
▶️ Run the Application
streamlit run app.py

The application will open in your browser at:

http://localhost:8501
📋 Supported Stocks
Indian Stocks
TCS
Infosys
Reliance
HDFC Bank
ICICI Bank
SBI
Wipro
US Stocks
Apple (AAPL)
Microsoft (MSFT)
Google (GOOGL)
Amazon (AMZN)
Tesla (TSLA)
Nvidia (NVDA)

You can also enter custom ticker symbols.

📊 AI Analysis Output

The AI generates insights including:

Market Trend
Technical Momentum
RSI Interpretation
MACD Signals
Risk Assessment
Short-Term Outlook
⚠️ Disclaimer

This project is intended for educational and informational purposes only. The AI-generated analysis should not be considered financial or investment advice. Always conduct your own research and consult a qualified financial advisor before making investment decisions.

🌟 Future Enhancements
Portfolio Tracker
Stock Price Prediction Models
News Sentiment Analysis
Multiple Timeframe Charts
Technical Indicator Library

👨‍💻 Author
Rudranil Dey
Developed as an AI-powered Stock Market Assistant using Streamlit, Yahoo Finance, Plotly, and Google Gemini AI.

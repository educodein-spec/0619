import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Global Market Cap Top10 Dashboard",
    layout="wide"
)

st.title("🌍 Global Market Cap Top10 Stocks")
st.markdown("최근 1년 주가 수익률 비교")

# Top10 종목
stocks = {
    "NVIDIA": "NVDA",
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Alphabet": "GOOGL",
    "Amazon": "AMZN",
    "Meta": "META",
    "Broadcom": "AVGO",
    "TSMC": "TSM",
    "Saudi Aramco": "2222.SR",
    "Tesla": "TSLA"
}

end_date = datetime.today()
start_date = end_date - timedelta(days=365)

@st.cache_data
def load_data():
    data = yf.download(
        list(stocks.values()),
        start=start_date,
        end=end_date,
        auto_adjust=True,
        progress=False
    )["Close"]

    # 종목명을 회사명으로 변경
    data.columns = stocks.keys()

    # 시작일 기준 100으로 정규화
    normalized = data.div(data.iloc[0]).mul(100)

    return normalized

df = load_data()

# Plotly
fig = go.Figure()

for col in df.columns:
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df[col],
            mode="lines",
            name=col,
            hovertemplate=
            f"<b>{col}</b><br>Date=%{{x|%Y-%m-%d}}<br>Index=%{{y:.2f}}<extra></extra>"
        )
    )

fig.update_layout(
    title="Top 10 Global Companies - 1Y Performance (Base=100)",
    xaxis_title="Date",
    yaxis_title="Normalized Price",
    hovermode="x unified",
    height=700,
    template="plotly_white",
    legend=dict(
        orientation="h",
        y=1.05
    )
)

st.plotly_chart(fig, use_container_width=True)

# 수익률 테이블
returns = ((df.iloc[-1] / df.iloc[0]) - 1) * 100
returns = returns.sort_values(ascending=False)

st.subheader("📈 1년 수익률 순위")
st.dataframe(
    pd.DataFrame({
        "Return (%)": returns.round(2)
    }),
    use_container_width=True
)

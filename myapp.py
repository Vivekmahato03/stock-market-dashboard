import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import date
import pandas_ta as ta
import plotly.express as px
import plotly.graph_objects as go
st.set_page_config('Trading dashboard',page_icon=':rocket:')
st.write("""
         # Top 50 Indian Companies in Stock Market Dashboard :bar_chart:
         Shown are closing price and volume of share
         """)
with st.sidebar:
    st.header("Fill Details")
    companies = {
        "Reliance Industries": "RELIANCE.NS",
        "Tata Consultancy Services": "TCS.NS",
        "HDFC Bank": "HDFCBANK.NS",
        "Infosys": "INFY.NS",
        "Hindustan Unilever": "HINDUNILVR.NS",
        "ICICI Bank": "ICICIBANK.NS",
        "State Bank of India": "SBIN.NS",
        "Kotak Mahindra Bank": "KOTAKBANK.NS",
        "Bajaj Finance": "BAJFINANCE.NS",
        "Bharti Airtel": "BHARTIARTL.NS",
        "Asian Paints": "ASIANPAINT.NS",
        "HCL Technologies": "HCLTECH.NS",
        "Wipro": "WIPRO.NS",
        "Maruti Suzuki": "MARUTI.NS",
        "Avenue Supermarts": "DMART.NS",
        "Nestle India": "NESTLEIND.NS",
        "Titan Company": "TITAN.NS",
        "Sun Pharmaceutical": "SUNPHARMA.NS",
        "Mahindra & Mahindra": "M&M.NS",
        "Larsen & Toubro": "LT.NS",
        "HDFC Life Insurance": "HDFCLIFE.NS",
        "Tech Mahindra": "TECHM.NS",
        "Bajaj Finserv": "BAJAJFINSV.NS",
        "UltraTech Cement": "ULTRACEMCO.NS",
        "Power Grid Corporation": "POWERGRID.NS",
        "IndusInd Bank": "INDUSINDBK.NS",
        "NTPC": "NTPC.NS",
        "SBI Life Insurance": "SBILIFE.NS",
        "Tata Steel": "TATASTEEL.NS",
        "Divi's Laboratories": "DIVISLAB.NS",
        "JSW Steel": "JSWSTEEL.NS",
        "Axis Bank": "AXISBANK.NS",
        "Hindalco Industries": "HINDALCO.NS",
        "Dr. Reddy's Laboratories": "DRREDDY.NS",
        "Bajaj Auto": "BAJAJ-AUTO.NS",
        "Grasim Industries": "GRASIM.NS",
        "Adani Green Energy": "ADANIGREEN.NS",
        "Britannia Industries": "BRITANNIA.NS",
        "Shree Cement": "SHREECEM.NS",
        "Cipla": "CIPLA.NS",
        "Coal India": "COALINDIA.NS",
        "Adani Ports & SEZ": "ADANIPORTS.NS",
        "Tata Motors": "TATAMOTORS.NS",
        "Pidilite Industries": "PIDILITIND.NS",
        "Godrej Consumer Products": "GODREJCP.NS",
        "IOC": "IOC.NS",
        "Havells India": "HAVELLS.NS",
        "Eicher Motors": "EICHERMOT.NS",
        "Hero MotoCorp": "HEROMOTOCO.NS",
        "Vedanta": "VEDL.NS"
    }
    company_name = st.selectbox("Select the company", list(companies.keys()))
    tickerSymbol = companies[company_name]
    shortTickerSymbol = tickerSymbol.split('.')[0]
    start_date = st.date_input("Start Date", date(2019, 4, 1), key='start_date')
    end_date = st.date_input("End Date", date.today(), max_value=date.today(), key='end_date')

tickerData = yf.Ticker(tickerSymbol)
tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)
current_price = tickerData.history(period='1d').tail(1)['Close'].iloc[0]
previous_price = tickerDf['Close'].iloc[-2] if len(tickerDf) > 1 else current_price
price_change = current_price - previous_price
triangle = "▲" if price_change > 0 else "▼"
triangle_color = "green" if price_change > 0 else "red"
st.write(f"## {shortTickerSymbol} : <span style='color:{triangle_color}; font-size: 1em;'>{triangle}</span>  {current_price:.2f} INR", unsafe_allow_html=True)
macd = ta.macd(tickerDf['Close'].dropna())
fig=go.Figure(data=[go.Candlestick(x=tickerDf.index,open=tickerDf['Open'],close=tickerDf['Close'],high=tickerDf['High'],low=tickerDf['Low'])])
st.write("## Candlestick")
st.plotly_chart(fig)
st.write("## Volume")
st.bar_chart(tickerDf.Volume,color=['#33FF4C'])
st.write("## Moving Average Convergence Divergence")
st.bar_chart(macd)
ema_5=ta.ema(tickerDf['Close'],length=5)
ema_13=ta.ema(tickerDf['Close'],length=13)
ema_26=ta.ema(tickerDf['Close'],length=26)
ema_df=pd.concat([ema_5,ema_13,ema_26],axis=1)
ema_df.columns=['EMA_5','EMA_13','EMA_26']
st.write("## Exponential Moving Averages (EMA)")
fig = px.line(ema_df, title="Exponential Moving Averages (EMA)", color_discrete_map={
    "EMA_5": "red",
    "EMA_13": "green",
    "EMA_26": "blue"
})
st.plotly_chart(fig, use_container_width=True)
import streamlit as st
import time
import datetime
import yfinance as yf
import pandas as pd
import altair as alt

list_of_stocks = ("DABUR.NS","BHARTIARTL.NS","APOLLOTYRE.NS","VEDL.NS","SHOPERSTOP.NS","VGUARD.NS")

col1, col2 = st.sidebar.beta_columns(2)

with col1:
    start_d = st.date_input(
    "Start Date",
    datetime.datetime.today().date() - datetime.timedelta(30))

with col2:
    end_d = st.date_input(
    "End Date",
    datetime.datetime.today().date())


option = st.sidebar.multiselect('How would you like to be contacted?',list_of_stocks)

#st.write("Selected",option)

if st.sidebar.button('Get Data'):
    stock_data = []
    for stock in option:
        my_tick = yf.Ticker(stock)
        date_to_compare_1 = start_d
        date_to_compare_2 = end_d
        stock_status_today = my_tick.history(start=date_to_compare_1, end=date_to_compare_2, interval="1d")
        stock_status = stock_status_today.reset_index()
        stock_status['TICKER_NAME'] = stock
        stock_data.append(stock_status)
    complete_data = pd.concat(stock_data,axis=0)
    complete_data.sort_values(by=['TICKER_NAME','Date'],ascending=True,inplace=True)
    complete_data['Date'] = complete_data['Date'].dt.date.apply(lambda x: str(x))
	
    obj = alt.Chart(complete_data).mark_line().encode(
        x='Date',
        y='Close',
        color='TICKER_NAME',
        strokeDash='TICKER_NAME')
    st.altair_chart(obj,use_container_width=True)
else:
    st.write('Nothing')

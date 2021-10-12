# Import libraries

import yfinance as yf
import plotly.express as px
import streamlit as st
import pandas as pd
st.sidebar.title('AECOM')
st.sidebar.write('by Yulei')
st.title('AECOM Visualisation')
st.header('Financials')
# Get stock ticker
stock_code='acm WSP.TO SNC.TO WBD.MI J FLR EME MTZ'
company_ls = ['AECOM','WSP Global Inc.','SNC-Lavalin Group Inc.','Webuild','Jacobs Engineering Group Inc.','Fluor','EMCOR Group, Inc.','MasTec, Inc.']
aecom_stock = yf.Tickers(stock_code)
st.dataframe('financial.csv')
st.subheader('Key Figures')

aecom_financial = aecom_stock.tickers['ACM'].financials
aecom_financial.to_csv('aecom_financial.csv')
wsp_financial = aecom_stock.tickers['WSP.TO'].financials

snc_financial = aecom_stock.tickers['SNC.TO'].financials
wbd_financial = aecom_stock.tickers['WBD.MI'].financials
jacob_financial = aecom_stock.tickers['J'].financials
flr_financial = aecom_stock.tickers['FLR'].financials
eme_financial = aecom_stock.tickers['EME'].financials
mtz_financial = aecom_stock.tickers['MTZ'].financials
st.dataframe(aecom_financial)

financial_df = pd.DataFrame()
financial_df['Company'] = company_ls
financial_df['Revenue'] =  [aecom_financial.loc['Total Revenue'][0],wsp_financial.loc['Total Revenue'][0],snc_financial.loc['Total Revenue'][0],wbd_financial.loc['Total Revenue'][0],jacob_financial.loc['Total Revenue'][0],flr_financial.loc['Total Revenue'][0],eme_financial.loc['Total Revenue'][0],mtz_financial.loc['Total Revenue'][0]]
financial_df['Expenses'] = [aecom_financial.loc['Total Operating Expenses'][0],
                            wsp_financial.loc['Total Operating Expenses'][0],
                            snc_financial.loc['Total Operating Expenses'][0],
                            wbd_financial.loc['Total Operating Expenses'][0],
                            jacob_financial.loc['Total Operating Expenses'][0],
                            flr_financial.loc['Total Operating Expenses'][0],
                            eme_financial.loc['Total Operating Expenses'][0],
                            mtz_financial.loc['Total Operating Expenses'][0]
                            ]
financial_df['Profit'] = [aecom_financial.loc['Gross Profit'][0],
                            wsp_financial.loc['Gross Profit'][0],
                            snc_financial.loc['Gross Profit'][0],
                            wbd_financial.loc['Gross Profit'][0],
                            jacob_financial.loc['Gross Profit'][0],
                            flr_financial.loc['Gross Profit'][0],
                            eme_financial.loc['Gross Profit'][0],
                            mtz_financial.loc['Gross Profit'][0]
                            ]

profit_fig = px.bar(financial_df,x='Company', y='Profit',labels = {'x':'Companies','y':'Gross Profit'},color='Company')
st.plotly_chart(profit_fig)
revenue_fig = px.bar(financial_df,x='Company', y='Revenue',labels = {'x':'Companies','y':'Total Revenue'},color='Company')
st.plotly_chart(revenue_fig)
expenses_fig = px.bar(financial_df,x='Company', y='Expenses',labels = {'x':'Companies','y':'Total Expenses'},color='Company')
st.plotly_chart(expenses_fig)

st.sidebar.subheader('Stock Price')
st.subheader('Stock Price')
stock_period = st.sidebar.selectbox('Please choose the period for stock prices', ('1d','5d','1mo','3mo','6mo','1y','2y','5y','10y','ytd','max'), index = 10)
stock_price_df = aecom_stock.history(period=stock_period)
# Stock price comparison plot (before scaling)
origin_stock_fig = px.line(stock_price_df, x=stock_price_df.index, y=stock_price_df['Close']['ACM'],
              labels={
                     "x": "Date",
                     "y": "Close Price"

                 },
        )
if st.sidebar.checkbox('Include competitors'):
    origin_stock_fig.add_scatter(x=stock_price_df.index, y=stock_price_df['Close']['WSP.TO'], mode='lines',name='WSP Global Inc.')
    origin_stock_fig.add_scatter(x=stock_price_df.index, y=stock_price_df['Close']['SNC.TO'], mode='lines',name='SNC-Lavalin Group Inc.')
    origin_stock_fig.add_scatter(x=stock_price_df.index, y=stock_price_df['Close']['WBD.MI'], mode='lines',name='Webuild')
    origin_stock_fig.add_scatter(x=stock_price_df.index, y=stock_price_df['Close']['J'], mode='lines',name='Jacobs Engineering Group Inc.')
    origin_stock_fig.add_scatter(x=stock_price_df.index, y=stock_price_df['Close']['FLR'], mode='lines',name='Fluor')
    origin_stock_fig.add_scatter(x=stock_price_df.index, y=stock_price_df['Close']['EME'], mode='lines',name='EMCOR Group, Inc.')
    origin_stock_fig.add_scatter(x=stock_price_df.index, y=stock_price_df['Close']['MTZ'], mode='lines',name='MasTec, Inc.')
st.plotly_chart(origin_stock_fig)

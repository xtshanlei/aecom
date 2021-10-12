# Import libraries

import yfinance as yf
import plotly.express as px
import streamlit as st
st.sidebar.title('AECOM')
st.sidebar.write('by Yulei')
st.title('AECOM Visualisation')
st.header('Financials')
# Get stock ticker
stock_code='acm WSP.TO SNC.TO WBD.MI J FLR EME MTZ '
aecom_stock = yf.Tickers(stock_code)

st.subheader('Key Figures')
st.dataframe(aecom_stock.tickers['ACM'].financials)
revenue_ls = ['AECOM','WSP Global Inc.','SNC-Lavalin Group Inc.','Webuild','Jacobs Engineering Group Inc.','Fluor','EMCOR Group, Inc.','MasTec, Inc.']
revenue_fig = px.bar(x=revenue_ls, y=[aecom_stock.tickers['ACM'].financials.loc['Total Revenue'][0],
                    aecom_stock.tickers['WSP.TO'].financials.loc['Total Revenue'][0],
                    aecom_stock.tickers['SNC.TO'].financials.loc['Total Revenue'][0],
                    aecom_stock.tickers['WBD.MI'].financials.loc['Total Revenue'][0],
                    aecom_stock.tickers['J'].financials.loc['Total Revenue'][0],
                    aecom_stock.tickers['FLR'].financials.loc['Total Revenue'][0],
                    aecom_stock.tickers['EME'].financials.loc['Total Revenue'][0],
                    aecom_stock.tickers['MTZ'].financials.loc['Total Revenue'][0]
                    ])
st.plotly_chart(revenue_fig)
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


# Stock price comparison plot (after scaling)
from sklearn.preprocessing import MinMaxScaler
aecom_scaler = MinMaxScaler()
aecom_stock_scale = aecom_scaler.fit_transform(stock_price_df['Close']['ACM'].values.reshape(-1,1))
wsp_scaler = MinMaxScaler()
wsp_stock_scale = aecom_scaler.fit_transform(stock_price_df['Close']['WSP.TO'].values.reshape(-1,1))
snc_scaler = MinMaxScaler()
snc_stock_scale = snc_scaler.fit_transform(stock_price_df['Close']['SNC.TO'].values.reshape(-1,1))

scale_stock_fig = px.line(stock_price_df, x=stock_price_df.index, y=aecom_stock_scale,
              labels={
                     "x": "Date",
                     "y": "Close Price"

                 },
        )
scale_stock_fig.add_scatter(x=stock_price_df.index, y=wsp_stock_scale,mode='lines',name='WSP Global Inc.')
scale_stock_fig.show()

scale_stock_fig = px.line(stock_price_df, x=stock_price_df.index, y=snc_stock_scale,
              labels={
                     "x": "Date",
                     "y": "Close Price"

                 },
        )
scale_stock_fig.show()

aecom_stock.sustainability

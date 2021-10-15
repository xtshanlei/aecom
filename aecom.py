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
st.subheader('Key Figures')
@st.cache(suppress_st_warning=True)
def get_financial(item):
    aecom_financial = aecom_stock.tickers['ACM'].financials
    wsp_financial = aecom_stock.tickers['WSP.TO'].financials
    snc_financial = aecom_stock.tickers['SNC.TO'].financials
    wbd_financial = aecom_stock.tickers['WBD.MI'].financials
    jacob_financial = aecom_stock.tickers['J'].financials
    flr_financial = aecom_stock.tickers['FLR'].financials
    eme_financial = aecom_stock.tickers['EME'].financials
    mtz_financial = aecom_stock.tickers['MTZ'].financials
    financial_df = pd.DataFrame()
    financial_df['Company'] = company_ls

    financial_df[item] = [aecom_financial.loc[item][0],
                                wsp_financial.loc[item][0],
                                snc_financial.loc[item][0],
                                wbd_financial.loc[item][0],
                                jacob_financial.loc[item][0],
                                flr_financial.loc[item][0],
                                eme_financial.loc[item][0],
                                mtz_financial.loc[item][0]
                                ]

    return financial_df
def get_financial_item(item):
    financial_df = pd.DataFrame()
    financial_df['Company'] = company_ls
    financial_df[item] = [aecom_financial.loc[item][0],
                                wsp_financial.loc[item][0],
                                snc_financial.loc[item][0],
                                wbd_financial.loc[item][0],
                                jacob_financial.loc[item][0],
                                flr_financial.loc[item][0],
                                eme_financial.loc[item][0],
                                mtz_financial.loc[item][0]
                                ]
    return financial_df


def format_number(num):
    num = safe_num(num)
    sign = ''

    metric = {'T': 1000000000000, 'B': 1000000000, 'M': 1000000, 'K': 1000, '': 1}

    for index in metric:
        num_check = num / metric[index]

        if(num_check >= 1):
            num = num_check
            sign = index
            break

    return f"{str(num).rstrip('0').rstrip('.')}{sign}"
st.sidebar.header('Financials')
st.sidebar.subheader('Key Figures')
item = st.sidebar.selectbox('Choose item you want to compare',('Research Development', 'Effect Of Accounting Charges',
       'Income Before Tax', 'Minority Interest', 'Net Income',
       'Selling General Administrative', 'Gross Profit', 'Ebit',
       'Operating Income', 'Other Operating Expenses', 'Interest Expense',
       'Extraordinary Items', 'Non Recurring', 'Other Items',
       'Income Tax Expense', 'Total Revenue', 'Total Operating Expenses',
       'Cost Of Revenue', 'Total Other Income Expense Net',
       'Discontinued Operations', 'Net Income From Continuing Ops',
       'Net Income Applicable To Common Shares'),index=15)

financial_df = get_financial(item)
st.markdown('**{}:**'.format(item)+'  **{}**'.format(format_number(financial_df[financial_df['Company']=='AECOM'][item].values)))

financial_fig = px.bar(financial_df,x='Company', y=item,labels = {'x':'Companies','y':item},color='Company')
st.plotly_chart(financial_fig)

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

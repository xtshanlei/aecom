# Import libraries

import yfinance as yf
import plotly.express as px
import streamlit as st
import pandas as pd
import requests
import json
import datetime
from bertopic import BERTopic
st.sidebar.image(image='https://www.ersg-global.com/rails/active_storage/representations/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBNmN3RkE9PSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--e7f7d7b3b40a8c8270c816aa95b02144356d3e79/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaDdCam9VWTI5dFltbHVaVjl2Y0hScGIyNXpld2c2QzNKbGMybDZaVWtpRGpJd01EQjRPVEF3WGdZNkJrVlVPZ3huY21GMmFYUjVTU0lMUTJWdWRHVnlCanNIVkRvSlkzSnZjRWtpRVRJd01EQjRPVEF3S3pBck1BWTdCMVE9IiwiZXhwIjpudWxsLCJwdXIiOiJ2YXJpYXRpb24ifX0=--0fb7870a4f06a87ce586fe2cf3dfb8c5759b4cb0/aecom.jpg',use_column_width='auto')
st.sidebar.write('by Yulei for the role: Senior Data Visualisation')
st.title('AECOM Interactive Visualisation')

##########Financial related##########
st.header('Financials')
# Get stock ticker
stock_code='acm WSP.TO SNC.TO WBD.MI J FLR EME MTZ'
company_ls = ['AECOM','WSP Global Inc.','SNC-Lavalin Group Inc.','Webuild','Jacobs Engineering Group Inc.','Fluor','EMCOR Group, Inc.','MasTec, Inc.']
aecom_stock = yf.Tickers(stock_code)
st.subheader('Key Figures')
@st.cache
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

def human_format(num):
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])

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
st.markdown('**{}: ${}**'.format(item,human_format(financial_df[financial_df['Company']=='AECOM'][item].values[0])))

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
##########Twitter related##########
st.sidebar.header('Twitter')
st.header('Twitter')
st.subheader('Recent 5 tweets:')
def create_headers(bearer_token): #build HEADERS
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers
headers=create_headers(st.secrets['bearer_token'])
#Get Twiter timeline
timeline_url = "https://api.twitter.com/2/users/19404869/tweets"
timeline_params ={'max_results':5, 'tweet.fields':"created_at,public_metrics"}
def connect_to_endpoint(url, headers, params): #链接ENDPOINT
    response = requests.request("GET", timeline_url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()
timeline_response = connect_to_endpoint(timeline_url,headers=headers,params=timeline_params)
for tweet in timeline_response['data']:
    st.markdown('**@AECOM:**{}'.format(tweet['text']))
    st.markdown('**Retweets:**{}    **Reply:**{}    **Likes: **{}'.format(tweet['public_metrics']['retweet_count'],tweet['public_metrics']['reply_count'],tweet['public_metrics']['like_count']))
    st.write('----------------------------------------')
# Get topic dynamics
import urllib.request
topic_model_url = 'https://media.githubusercontent.com/media/xtshanlei/aecom/a21a8bb4316e8559fc48b5767d0d8b971a3029a8/topic_model'
response = urllib.request.urlopen(topic_model_url)
data = response.read()
topic_model = BERTopic.load(data)
topics_over_time = pd.read_csv('https://raw.githubusercontent.com/xtshanlei/aecom/main/topics_over_time.csv')
topic_model.visualize_topics_over_time(topics_over_time, top_n_topics=20, normalize_frequency=True)

# Import libraries

import yfinance as yf
import plotly.express as px
import streamlit as st
import pandas as pd
import requests
import json
import datetime
st.sidebar.image(image='https://www.ersg-global.com/rails/active_storage/representations/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBNmN3RkE9PSIsImV4cCI6bnVsbCwicHVyIjoiYmxvYl9pZCJ9fQ==--e7f7d7b3b40a8c8270c816aa95b02144356d3e79/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaDdCam9VWTI5dFltbHVaVjl2Y0hScGIyNXpld2c2QzNKbGMybDZaVWtpRGpJd01EQjRPVEF3WGdZNkJrVlVPZ3huY21GMmFYUjVTU0lMUTJWdWRHVnlCanNIVkRvSlkzSnZjRWtpRVRJd01EQjRPVEF3S3pBck1BWTdCMVE9IiwiZXhwIjpudWxsLCJwdXIiOiJ2YXJpYXRpb24ifX0=--0fb7870a4f06a87ce586fe2cf3dfb8c5759b4cb0/aecom.jpg',use_column_width='auto')
st.sidebar.write('by Yulei')
st.sidebar.markdown("""---""")
st.title('AECOM Interactive Visualisation')
st.write('This project is developed using Python and multiple packages by Yulei for the application for the role role as Data Visualisation at AECOM. All data are available publicly including webiste, public financial API and social media data. The project used various techniques of data collection, data pre-processing, Natual Language Processing (NLP) and visualisation')
st.markdown('**How to Use**:')
st.write('Users can use the left panel to navigate and interact with the visualisation below. For example, choose a particular financial item to compare with competitors')
##########Basic Information##########
st.header('Descriptive')
st.sidebar.header('Descriptive')
st.subheader('History',anchor='history')
st.sidebar.subheader('[History](#history)')
st.write("AECOM launched when a handful of employees from design and engineering companies shared a dream of creating an industry-leading firm dedicated to delivering a better world.We became an independent company formed by the merger of five entities. While our official founding was in 1990, many of our predecessor firms had distinguished histories dating back more than 120 years.Since then, more than 50 companies have joined us and, in 2007, we became a publicly traded company on the New York Stock Exchange.")

office_df= pd.read_csv('uk_offices.csv')
st.subheader('30 UK Offices on Map', anchor='office')
st.markdown('**Data Source**: [ENDS DIRECTORY](https://www.endsdirectory.com/entry/57/aecom/details)')
st.markdown('**Data Collection**: Web Crawler (ScrapeStorm)')
st.markdown('**Data Pre-processing**: Converting address to latitude and longitude (GEOPY + BING API)')
st.markdown('**Visualisation**: Plotly')
st.sidebar.subheader('[UK Offices](#office)')
st.sidebar.markdown("""---""")
px.set_mapbox_access_token(st.secrets['mapbox_token'])
map_fig = px.scatter_mapbox(office_df, lat="lat", lon="lon", size_max=10, hover_name = 'office',zoom=5, size = [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,6,2,2,2,2,2,2,2,2,2,2,2], center = {'lat':51.5147672,'lon':-0.072115})
st.plotly_chart(map_fig)
##########Financial related##########
st.markdown("""---""")
st.header('Financials',anchor='financials')
st.markdown('**Data Source**: Real-time public financial information from Yahoo Finance')
# Get stock ticker
stock_code='acm WSP.TO SNC.TO WBD.MI J FLR EME MTZ'
company_ls = ['AECOM','WSP Global Inc.','SNC-Lavalin Group Inc.','Webuild','Jacobs Engineering Group Inc.','Fluor','EMCOR Group, Inc.','MasTec, Inc.']
aecom_stock = yf.Tickers(stock_code)
st.subheader('Key Figures',anchor='key')
@st.cache
def get_financial():
    aecom_financial = aecom_stock.tickers['ACM'].financials
    wsp_financial = aecom_stock.tickers['WSP.TO'].financials
    snc_financial = aecom_stock.tickers['SNC.TO'].financials
    wbd_financial = aecom_stock.tickers['WBD.MI'].financials
    jacob_financial = aecom_stock.tickers['J'].financials
    flr_financial = aecom_stock.tickers['FLR'].financials
    eme_financial = aecom_stock.tickers['EME'].financials
    mtz_financial = aecom_stock.tickers['MTZ'].financials
    return aecom_financial,wsp_financial,snc_financial,wbd_financial,jacob_financial,flr_financial,eme_financial,mtz_financial
with st.spinner('Extracting latest financial information, please wait...'):
    aecom_financial,wsp_financial,snc_financial,wbd_financial,jacob_financial,flr_financial,eme_financial,mtz_financial = get_financial()
st.success('Extraction completed!')
st.write(aecom_financial)


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
st.sidebar.subheader('Financials')
st.sidebar.subheader('[Key Figures](#key)')
item = st.sidebar.selectbox('Choose item you want to compare',('Research Development', 'Effect Of Accounting Charges',
       'Income Before Tax', 'Minority Interest', 'Net Income',
       'Selling General Administrative', 'Gross Profit', 'Ebit',
       'Operating Income', 'Other Operating Expenses', 'Interest Expense',
       'Extraordinary Items', 'Non Recurring', 'Other Items',
       'Income Tax Expense', 'Total Revenue', 'Total Operating Expenses',
       'Cost Of Revenue', 'Total Other Income Expense Net',
       'Discontinued Operations', 'Net Income From Continuing Ops',
       'Net Income Applicable To Common Shares'),index=15)

financial_df = get_financial_item(item)
st.markdown('**{}: ${}**'.format(item,human_format(financial_df[financial_df['Company']=='AECOM'][item].values[0])))

financial_fig = px.bar(financial_df,x='Company', y=item,labels = {'x':'Companies','y':item},color='Company')
st.plotly_chart(financial_fig)

st.sidebar.subheader('[Stock Price](#stock_price)')
st.subheader('Stock Price',anchor='stock_price')
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
st.sidebar.markdown("""---""")
def create_headers(bearer_token): #build HEADERS
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers
headers=create_headers(st.secrets['bearer_token'])
def connect_to_endpoint(url, headers, params): #链接ENDPOINT
    response = requests.request("GET", url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()
user_url = 'https://api.twitter.com/2/users/19404869'
user_params={'user.fields':'public_metrics'}
user_response = connect_to_endpoint(user_url,headers=headers,params=user_params)

st.sidebar.header('Twitter')
st.markdown("""---""")
st.header('Twitter')
st.sidebar.subheader('[Public Metrics](#metrics)')
st.subheader('Real Time Public Metrics',anchor='metrics')
st.markdown('**Followers:  {}**'.format(user_response['data']['public_metrics']['followers_count']))
st.markdown('**Following:  {}**'.format(user_response['data']['public_metrics']['following_count']))
st.markdown('**Tweet count:  {}**'.format(user_response['data']['public_metrics']['tweet_count']))
st.markdown('**Listed count:  {}**'.format(user_response['data']['public_metrics']['listed_count']))
st.sidebar.subheader('[Recent tweets](#recent_tweet)')
tweet_num = st.sidebar.slider('Slide to choose how many recent tweets to watch below',min_value=1,max_value=10,value=5,step=1)
st.subheader('Recent {} tweet:'.format(tweet_num),anchor='recent_tweet')

#Get Twiter timeline
timeline_url = "https://api.twitter.com/2/users/19404869/tweets"
timeline_params ={'max_results':tweet_num, 'tweet.fields':"created_at,public_metrics"}
timeline_response = connect_to_endpoint(timeline_url,headers=headers,params=timeline_params)
for tweet in timeline_response['data']:
    st.markdown('**@AECOM:**{}'.format(tweet['text']))
    st.markdown('**Retweets:**{}    **Reply:**{}    **Likes: **{}'.format(tweet['public_metrics']['retweet_count'],tweet['public_metrics']['reply_count'],tweet['public_metrics']['like_count']))
    st.write('----------------------------------------')
# Get topic dynamics
import streamlit.components.v1 as components
st.subheader('TOP 10 Topics Discussed on Twitter Since 2020',anchor='top_topics')
st.markdown('**Data source**: Collected tweets mentioning AECOM')
st.markdown('**Topic Model**: BERTopic (Utilising state-of-the-art BERT model for better interpretability than popular LDA model)')
st.markdown('**Topic visualisation**: Plotly')
st.write('Topics extrated from over 44K public tweets since 2020 using state-of-the-art topic modelling.')
st.sidebar.subheader('[Top Topics](#top_topics)')
top_topics=pd.read_csv('top_10_topics.csv')
top_topics_fig = px.bar(top_topics.sort_values(by='Count'),x='Count', y='Name',labels = {'x':'Count','y':'Topic with keywords'},orientation='h')
st.plotly_chart(top_topics_fig)
st.subheader('Topics Discussed over Time',anchor='topics_time')
st.sidebar.subheader('[Topics Over Time](#topics_time)')
st.write('Explore the spikes for special events')
HtmlFile = open("dynamic_topic.html", 'r', encoding='utf-8')
source_code = HtmlFile.read()
components.html(source_code,height=600,width=1200)

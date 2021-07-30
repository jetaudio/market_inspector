from binance.client import Client
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
from talib import *
import numpy as np
from plotly.subplots import make_subplots
from time import sleep
import threading
def start_thread(func, name=None, args = []):
    threading.Thread(target=func, name=name, args=args).start()
####################################################################

patterns_list=[CDL2CROWS, CDL3BLACKCROWS, CDL3INSIDE, CDL3LINESTRIKE, CDL3OUTSIDE, CDL3STARSINSOUTH, CDL3WHITESOLDIERS, CDLABANDONEDBABY, CDLADVANCEBLOCK, CDLBELTHOLD, CDLBREAKAWAY, CDLCLOSINGMARUBOZU, CDLCONCEALBABYSWALL, CDLCOUNTERATTACK, CDLDARKCLOUDCOVER, CDLDOJI, CDLDOJISTAR, CDLDRAGONFLYDOJI, CDLENGULFING, CDLEVENINGDOJISTAR, CDLEVENINGSTAR, CDLGAPSIDESIDEWHITE , CDLGRAVESTONEDOJI, CDLHAMMER, CDLHANGINGMAN, CDLHARAMI, CDLHARAMICROSS, CDLHIGHWAVE, CDLHIKKAKE, CDLHIKKAKEMOD, CDLHOMINGPIGEON, CDLIDENTICAL3CROWS, CDLINNECK, CDLINVERTEDHAMMER, CDLKICKING, CDLKICKINGBYLENGTH, CDLLADDERBOTTOM, CDLLONGLEGGEDDOJI, CDLLONGLINE, CDLMARUBOZU, CDLMATCHINGLOW, CDLMATHOLD, CDLMORNINGDOJISTAR, CDLMORNINGSTAR, CDLONNECK, CDLPIERCING, CDLRICKSHAWMAN, CDLRISEFALL3METHODS, CDLSEPARATINGLINES, CDLSHOOTINGSTAR, CDLSHORTLINE, CDLSPINNINGTOP, CDLSTALLEDPATTERN, CDLSTICKSANDWICH, CDLTAKURI, CDLTASUKIGAP, CDLTHRUSTING, CDLTRISTAR, CDLUNIQUE3RIVER, CDLUPSIDEGAP2CROWS, CDLXSIDEGAP3METHODS]

####################################################################          
def heikin_ashi(df):
    heikin_ashi_df = pd.DataFrame(index=df.index.values, columns=['open', 'high', 'low', 'close'])
    heikin_ashi_df['close'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
    for i in range(len(df)):
        if i == 0:
            heikin_ashi_df.iat[0, 0] = df['open'].iloc[0]
        else:
            heikin_ashi_df.iat[i, 0] = (heikin_ashi_df.iat[i-1, 0] + heikin_ashi_df.iat[i-1, 3]) / 2
        
    heikin_ashi_df['high'] = heikin_ashi_df.loc[:, ['open', 'close']].join(df['high']).max(axis=1)
    heikin_ashi_df['low'] = heikin_ashi_df.loc[:, ['open', 'close']].join(df['low']).min(axis=1)
    return heikin_ashi_df
####################################################################
def data_prep(candles):
    df=pd.DataFrame(candles)
    df=df.rename(columns={0:'time'})
    df=df.rename(columns={1:'open'})
    df=df.rename(columns={2:'high'})
    df=df.rename(columns={3:'low'})
    df=df.rename(columns={4:'close'})
    for i in range(5,12):
        df=df.drop(columns=i)

    df['time']=pd.DataFrame(map(datetime.fromtimestamp,df['time']/1000))
    df['open']=df['open'].astype(float)
    df['close']=df['close'].astype(float)
    df['high']=df['high'].astype(float)
    df['low']=df['low'].astype(float)
    df['patterns']=''
    for func in patterns_list:
        pattern(df,func)
    return df
####################################################################
def pattern(df, func):
    patterns = pd.DataFrame()
    patterns['patterns'] = func(df['open'], df['high'], df['low'], df['close']).astype('str')
    for i in range(0,len(patterns['patterns']),1):
        if patterns['patterns'][i] == '100' or patterns['patterns'][i] == '-100':
            df.at[i,'patterns']=func.__name__
        elif patterns['patterns'][i] == '200' or patterns['patterns'][i] == '-200':
            df.at[i,'patterns']=func.__name__ + "+"
####################################################################
def get_price():
    key = open('key.txt', 'r').read().split(":",2)
    coin='BTCUSDT'
    client = Client(key[0], key[1])
    global dfp
    dfp = pd.DataFrame()
    while 1:
        try:
            dfp = dfp.append({'price':client.get_all_tickers(symbol=coin)['price']},ignore_index=True)
            sleep(1)
        except:
            print('failed to get data')
####################################################################
start_thread(get_price)


















##
##while (True):
##    if (datetime.now().second == 59):
##        candles = client.get_klines(symbol=coin, interval=client.KLINE_INTERVAL_1MINUTE,limit=100)
##        #candles_15min = client.get_klines(symbol=coin, interval=client.KLINE_INTERVAL_15MINUTE,limit=992)
##        #candles_1hour = client.get_klines(symbol=coin, interval=client.KLINE_INTERVAL_1HOUR,limit=248)
##        df = data_prep(candles)
##        print(df[(len(df)-1):].to_string(index=False, header=False))
##        sleep(30)


##df_1=data_prep(candles_1min)
##df_15=data_prep(candles_15min)
##df_1hour = data_prep(candles_1hour)
##df_4hour_BTC = data_prep(candles_4hour_BTC)
#hdf_4hour=heikin_ashi(df_4hour)
#macd_15,signal_15,hist_15 = MACD(df_15['close'].astype('double'), fastperiod = 12, slowperiod = 26, signalperiod = 9)
#macd_1hour,signal_1hour,hist_1hour = MACD(df_1hour['close'].astype('double'), fastperiod = 12, slowperiod = 26, signalperiod = 9)
##macd_4hour,signal_4hour,hist_4hour = MACD(df_4hour['close'].astype('double'), fastperiod = 12, slowperiod = 26, signalperiod = 9)
##
##fig = make_subplots(rows=2,cols=1)
##fig.add_trace(go.Candlestick(name=coin+' 4hour',x=df_4hour['time'],open=df_4hour['open'],high=df_4hour['high'],low=df_4hour['low'],close=df_4hour['close']),row=1,col=1)
##fig.add_trace(go.Candlestick(name='BTCUSDT 4hour',x=df_4hour_BTC['time'],open=df_4hour_BTC['open'],high=df_4hour_BTC['high'],low=df_4hour_BTC['low'],close=df_4hour_BTC['close']),row=2,col=1)
#fig.add_trace(go.Candlestick(name=coin+' 1hour',x=df_1hour['time'],open=df_1hour['open'],high=df_1hour['high'],low=df_1hour['low'],close=df_1hour['close']),row=1,col=1)
#fig.add_trace(go.Candlestick(name=coin+' 15min',x=df_15['time'],open=df_15['open'],high=df_15['high'],low=df_15['low'],close=df_15['close']),row=1,col=1)
#fig.add_trace(go.Candlestick(name=coin,x=df_15['time'],open=hdf_15['open'],high=hdf_15['high'],low=hdf_15['low'],close=hdf_15['close']),row=1,col=1)
#fig.add_trace(go.Scatter(y=macd,x=df_15['time'],name='MACD'),row=2,col=1)
#fig.add_trace(go.Scatter(y=signal,x=df_15['time'],name='Signal'),row=2,col=1)
#fig.add_trace(go.Scatter(y=hist_15,x=df_15['time'],name='Historam_15'),row=2,col=1)
#fig.add_trace(go.Scatter(y=hist_1hour,x=df_1hour['time'],name='Historam_1hour'),row=2,col=1)
#fig.add_trace(go.Scatter(y=hist_4hour,x=df_4hour['time'],name='Historam_4hour'),row=2,col=1)
#fig.update(layout_xaxis_rangeslider_visible=False)
#fig.update(layout_xaxis_rangeslider_visible=False)
#fig.show()
##fig=go.Figure(data)
##fig1=go.Figure(data=go.Scatter(y=macd,x=dt,name='MACD'))
##fig1.add_trace(go.Scatter(y=signal,x=dt,name='Signal'))
##fig1.add_bar(y=hist,x=dt,name='Histogram')
##fig0=make_subplots(rows=2,cols=1)
##fig0.add_trace(fig,row=1,col=1)
##fig0.add_trace(fig1,row=2,col=1)
##fig0.show()
#candles_1hour = client.get_historical_klines('ALICEUSDT', client.KLINE_INTERVAL_1HOUR,"1 Jul, 2021")
#candles_4hour = client.get_historical_klines('ALICEUSDT', client.KLINE_INTERVAL_4HOUR,"1 Jul, 2021")

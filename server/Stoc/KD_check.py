#導入pandas_datareader
import pandas_datareader as data
from talib import abstract
from datetime import datetime, timedelta, date
import pandas as pd 

def stock_m(s_id, st_d, beg_id, end_id):
    buy=[[],[],[],[]]
    sell=[[],[],[],[]]
    out_of_market = []
    
    start = datetime.now() - timedelta(days=360)
    end = date.today()
    pd.core.common.is_list_like = pd.api.types.is_list_like
    
    for i in s_id[beg_id:end_id]:
        #設定爬蟲時間
        try:
            stock_dr = data.get_data_yahoo(i+'.TW', start, end, interval='w')
        except:
            print(str(i)+ ' ' + st_d[i] +" 已經下市")
            out_of_market+=[i]
            continue
        stock_dr.columns=['high','low','open','close','volume','adj close']


        if stock_dr.iloc[-1].open < 3000 and stock_dr.iloc[-1].volume>5000000:  #取價格小於 300,且量大於5000張
#             #accuracy
#             if i in buy_last:
#                 if stock_dr.iloc[-1].open <  stock_dr.iloc[-1].close:
#                     sum_buy+=1
#             if i in sell_last:
#                 if stock_dr.iloc[-1].open >  stock_dr.iloc[-1].close:
#                     sum_sell+=1      
            try:
                kd=abstract.STOCH(stock_dr,fastk_period=9)
            except:
                print(str(i)+' kd fail')
                continue
            cross=kd.iloc[-2:]

            for j in range(len(cross)-1):
                #print(j)
                if cross.slowd.iloc[j] > cross.slowk.iloc[j] and cross.slowd.iloc[j+1] < cross.slowk.iloc[j+1]:
                    #print(' +  : ',cross.index[j])
                    if cross.slowk.iloc[j] < 20 :
                        buy[0] += [i,st_d[i],stock_dr.iloc[-1].open,cross.index[j],' + ']
                    elif cross.slowk.iloc[j] < 50 :
                        buy[1] += [i,st_d[i],stock_dr.iloc[-1].open,cross.index[j],' + ']
                    elif cross.slowk.iloc[j] < 80 :
                        buy[2] += [i,st_d[i],stock_dr.iloc[-1].open,cross.index[j],' + ']
                    else :
                        buy[3] += [i,st_d[i],stock_dr.iloc[-1].open,cross.index[j],' + ']
                    
                elif cross.slowd.iloc[j] < cross.slowk.iloc[j] and cross.slowd.iloc[j+1] > cross.slowk.iloc[j+1] :
                    if cross.slowd.iloc[j] > 80 :
                        sell[0] += [i,st_d[i],stock_dr.iloc[-1].open,cross.index[j],' - ']
                    elif cross.slowd.iloc[j] > 50 :
                        sell[1] += [i,st_d[i],stock_dr.iloc[-1].open,cross.index[j],' - ']
                    elif cross.slowd.iloc[j] > 20 :
                        sell[2] += [i,st_d[i],stock_dr.iloc[-1].open,cross.index[j],' - ']
                    else:
                        sell[3] += [i,st_d[i],stock_dr.iloc[-1].open,cross.index[j],' - ']
                    
                        
    return(buy, sell, out_of_market)
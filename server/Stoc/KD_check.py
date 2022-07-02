#導入pandas_datareader
import pandas_datareader as data
from talib import abstract
from datetime import datetime, timedelta, date
import pandas as pd 
from pandas import read_excel
#製作 Stock_ID
st_data = read_excel('D:\\Learn\\Stock_king_server\\server\\Stoc\\stock_id.xlsx',dtype=str)
s_id=[str(i) for i in list(st_data.num)] #全部的股票代號
s_name=list(st_data.name)
st_d={}
for i in range(len(s_id)):
    st_d[s_id[i]]=s_name[i]
    
class StockModel():
    def get_stock_data(self, stock_id, start_time= False, end_time=False):
        # ---test---
        start_time = datetime.now() - timedelta(days=360)
        end_time = date.today()
        # ---test---
        # try:
        stock_dr = data.get_data_yahoo(stock_id+'.TW', start_time, end_time, interval='w')
        stock_dr.columns=['high','low','open','close','volume','adj close']
        return stock_dr
        # except:
        #     print(str(stock_id)+ ' ' + st_d[stock_id] +" 已經下市")
        #     return False
            
        

    def select_logic(self, stock_dr):
        buy=[[],[],[],[]]
        sell=[[],[],[],[]]
        out_of_market = []

        if stock_dr.iloc[-1].open < 3000 and stock_dr.iloc[-1].volume>5000000:  #取價格小於 300,且量大於5000張
                # #accuracy
                # if i in buy_last:
                #     if stock_dr.iloc[-1].open <  stock_dr.iloc[-1].close:
                #         sum_buy+=1
                # if i in sell_last:
                #     if stock_dr.iloc[-1].open >  stock_dr.iloc[-1].close:
                #         sum_sell+=1      
            try:
                kd=abstract.STOCH(stock_dr,fastk_period=9)
            except:
                print(str(i)+' kd fail')
                # continue
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
        return buy, sell

    def stock_m(self, s_id, st_d, beg_id, end_id):
        out_of_market = []
        
        start = datetime.now() - timedelta(days=360)
        end = date.today()
        pd.core.common.is_list_like = pd.api.types.is_list_like
        
        
        for i in s_id[beg_id:end_id]:
            #設定爬蟲時間
            stock_dr = self.get_stock_data(start, end)
            if not stock_dr:
                out_of_market+=[i]
                


            buy, sell = self.select_logic(stock_dr)
                        
                            
        return(buy, sell, out_of_market)

if __name__ == '__main__':
    stock_model = StockModel()
    print(stock_model.get_stock_data('2330'))
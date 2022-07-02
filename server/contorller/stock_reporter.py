from datetime import datetime
from pandas import read_excel
from email.mime.text import MIMEText
from concurrent.futures import ThreadPoolExecutor
from smtplib import SMTP
from KD_check import StockModel
from mail import Mail
from config import cooperation_list
stock_model = StockModel()
mail = Mail()

#製作 Stock_ID
st_data = read_excel(cooperation_list,dtype=str)
s_id=[str(i) for i in list(st_data.num)] #全部的股票代號
s_name=list(st_data.name)
st_d={}
for i in range(len(s_id)):
    st_d[s_id[i]]=s_name[i]
##################################################################
#切割任務
#製作切割開始結束的位置list
div_list=[0]
part= 150 #建多少 thread 一起跑
start_div=0
for i in range(part-1):
    div_list+=[start_div + len(s_id)//part]
    start_div+=len(s_id)//part
div_list+=[len(s_id)]
t=[]
buy=[[],[],[],[]]
sell=[[],[],[],[]]
out_of_market=[]
#平行處理
with ThreadPoolExecutor() as executor:
    for i in range(part):
        t+=[executor.submit(stock_model.stock_m, s_id, st_d, div_list[i], div_list[i+1])]
    for i in range(part):
        
        for index, j in enumerate(t[i].result()[0]):
            if j != []:
                buy[index] += j
                
        for index, j in enumerate(t[i].result()[1]):
            if j != []:
                sell[index] += j
            
        if t[i].result()[2] != []:
            out_of_market+= t[i].result()[2][0]
    
print('Stock crawler Finish !')
buy_id=[[],[],[],[]]
sell_id=[[],[],[],[]]
for index, i in enumerate(buy):
    for j in range(len(i)):
        if j % 5 == 0 :
            buy_id[index] += [[i[j],i[j+1],i[j+2]]]
for index, i in enumerate(sell):
    for j in range(len(i)):
        if j % 5 == 0 :
            sell_id[index] += [[i[j],i[j+1],i[j+2]]]
print('buy : ',buy_id)
print('\n')
print('sell : ',sell_id)
print('#################################################################################')
##############################################################
mail.run(buy_id, sell_id)
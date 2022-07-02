from datetime import datetime
from pandas import read_excel
from email.mime.text import MIMEText
from concurrent.futures import ThreadPoolExecutor
from smtplib import SMTP
from KD_check import StockModel
stock_model = StockModel()
#製作 Stock_ID
st_data = read_excel('/root/server/Stoc/stock_id.xlsx',dtype=str)
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
#寄信

smtp = SMTP('smtp.gmail.com', 587)
smtp.ehlo()
smtp.starttls()
smtp.login('hsustock12345@gmail.com','mquwmfftoldbbyap')

#寄/收件人
from_addr='hsustock12345@gmail.com'
to_addr=['hsusean1219@gmail.com',
         'stevenlinlyc860415@gmail.com','spencer8005@yahoo.com.tw', 'ian84311@gmail.com', 'tim47964136tim@gmail.com',
         'kevinyu05062006@gmail.com','davidlv7621@yahoo.com.tw','anderson831208@gmail.com',  
         'LOVEYSTIN@gmail.com', 'kennyliao07@hotmail.com.tw',
         'Jeremy.Hsu@sti.com.tw','emailirene2006@gmail.com']
# to_addr=['hsusean1219@gmail.com']

#推薦名單
recommend_buy = buy_id
recommend_sell = sell_id

#編輯內文
msg=""
msg+="Buy\n\n"
if sum([len(i) for i in recommend_buy])==0:
    msg+="None!!\n\n"
else:
    for index, i in enumerate(recommend_buy):
        if index == 0:
            msg += '強力推薦:\n'
        elif index ==1:
            msg += '高度推薦:\n'
        elif index ==2:
            msg += '中度推薦:\n'
        elif index ==3:
            msg += '低度推薦:\n'
        if i== []:
            msg += "None!!\n\n"
        else:
            for j in i:
                if j == i[-1]:
                    msg+= j[0]+' '+j[1]+" Price "+ str(round(j[2],2))+" !\n\n"
                else:
                    msg+= j[0]+' '+j[1]+" Price "+ str(round(j[2],2))+",\n"
msg+="Sell\n\n"
if sum([len(i) for i in recommend_sell])==0:
    msg+="None!!\n\n"
else:
    for index, i in enumerate(recommend_sell):
        if index == 0:
            msg += '強力推薦:\n'
        elif index ==1:
            msg += '高度推薦:\n'
        elif index ==2:
            msg += '中度推薦:\n'
        elif index ==3:
            msg += '低度推薦:\n'
        if i== []:
            msg += "None!!\n\n"
        else:
            for j in i:
                if j == i[-1]:
                    msg+= j[0]+' '+j[1]+" Price "+ str(round(j[2],2))+" !\n\n"
                else:
                    msg+= j[0]+' '+j[1]+" Price "+ str(round(j[2],2))+",\n"

msg += '\n 投資一定有風險，申購前請詳閱公開說明書'
#輸入內容
text = MIMEText(msg, 'plain', 'utf-8')
text['From'] = u'台灣巴菲哲'
text['Subject'] =u'自動報明牌系統'

#寄信        
for k in to_addr:
    status=smtp.sendmail(from_addr, k, text.as_string())#加密文件，避免私密信息被截取 發現信的內容不能有":"            

#確認
if status=={}:
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"  郵件傳送成功!")
else:
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"  郵件傳送失敗!")
smtp.quit()

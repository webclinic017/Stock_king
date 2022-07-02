from datetime import datetime
from pandas import read_excel
from email.mime.text import MIMEText
from concurrent.futures import ThreadPoolExecutor
from smtplib import SMTP
from KD_check import StockModel
from mail import Mail
from config import cooperation_list, partition
stock_model = StockModel()
mail = Mail()

class StockReporter():
    def get_stock_id_name(self):
        #製作 Stock_ID
        st_data = read_excel(cooperation_list,dtype=str)
        s_id=[str(i) for i in list(st_data.num)] #全部的股票代號
        return s_id

    def split_for_parallel(s_id):
        #切割任務
        #製作切割開始結束的位置list
        div_list=[0]
        start_div=0
        for i in range(partition-1):
            div_list+=[start_div + len(s_id)//partition]
            start_div+=len(s_id)//partition
        div_list+=[len(s_id)]
        return div_list

    def run_algo(self, s_id, div_list):
        parallel_temp = []
        levels = ['highest', 'high', 'low', 'lowest']
        buy = sell = {}
        buy_id = sell_id = {}
        for level in levels:
            buy[level] = []
            sell[level] = []
        out_of_market=[]
        #平行處理
        with ThreadPoolExecutor() as executor:
            for i in range(partition):
                parallel_temp+=[executor.submit(stock_model.stock_m, s_id, div_list[i], div_list[i+1])]
            for i in range(partition):
                
                for level in parallel_temp[i].result().get('buy'):
                    if j != []:
                        buy[level] += j
                        
                for level in parallel_temp[i].result().get('sell'):
                    if j != []:
                        sell[level] += j
                    
                if parallel_temp[i].result().get('out_of_market') != []:
                    out_of_market+= parallel_temp[i].result().get('out_of_market')[0]
            
        print('Stock crawler Finish !')
        for level in levels:
            buy_id[level] = []
            sell_id[level] = []
        for level in buy:
            for j in range(len(buy[level])):
                if j % 5 == 0 :
                    buy_id[level] += [[i[j],i[j+1],i[j+2]]]
        for level in sell:
            for j in range(len(sell[level])):
                if j % 5 == 0 :
                    sell_id[level] += [[i[j],i[j+1],i[j+2]]]
        print('buy : ',buy_id)
        print('\n')
        print('sell : ',sell_id)
        print('#################################################################################')
        return buy_id, sell_id

    def run(self):
        stock_ids = self.get_stock_id_name()
        parallel_divide_list = self.split_for_parallel(stock_ids)
        buy_id, sell_id = self.run_algo(stock_ids, parallel_divide_list)
        # send report
        mail.run(buy_id, sell_id)

    if __name__ == '__main__':
        print(1)
from datetime import datetime
from email.mime.text import MIMEText
from smtplib import SMTP


from datetime import datetime
from pandas import read_excel
from email.mime.text import MIMEText
from concurrent.futures import ThreadPoolExecutor
from smtplib import SMTP
from KD_check import stock_m

#讀黨
#製作 Stock_ID
st_data = read_excel('Stoc/stock_id.xlsx',dtype=str)

#寄信

smtp = SMTP('smtp.gmail.com', 587)
smtp.ehlo()
smtp.starttls()
smtp.login('hsustock12345@gmail.com','mquwmfftoldbbyap')

#寄/收件人
from_addr='hsustock12345@gmail.com'
to_addr=['hsusean1219@gmail.com']


#編輯內文
msg=""

            
#輸入內容
text = MIMEText(msg, 'plain', 'utf-8')
text['From'] = u'台灣巴菲哲'
text['Subject'] =u'自動報明牌系統'

#寄信        
# for k in to_addr:
#     status=smtp.sendmail(from_addr, k, text.as_string())#加密文件，避免私密信息被截取 發現信的內容不能有":"            

# #確認
# if status=={}:
#     print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"  郵件傳送成功!")
# else:
#     print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"  郵件傳送失敗!")
# smtp.quit()
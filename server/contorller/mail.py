#寄信
from smtplib import SMTP
from email.mime.text import MIMEText
from datetime import datetime 
from config import from_addr, to_addr, mail_token
smtp = SMTP('smtp.gmail.com', 587)

class Mail():
    def mail_login(self):
        smtp.ehlo()
        smtp.starttls()
        smtp.login(from_addr, mail_token)

    def create_content(self, buy_ids, sell_ids):

        #推薦名單
        recommend_buy = buy_ids
        recommend_sell = sell_ids

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
        return text

    def send_mail(self, content):
        #寄信        
        
        # to_addr=['hsusean1219@gmail.com']
        for k in to_addr:
            status=smtp.sendmail(from_addr, k, content.as_string())#加密文件，避免私密信息被截取 發現信的內容不能有":"            

        #確認
        if status=={}:
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"  郵件傳送成功!")
        else:
            print(datetime.now().strftime('%Y-%m-%d %H:%M:%S')+"  郵件傳送失敗!")
        smtp.quit()

    def run(self, buy_ids, sell_ids):
        self.mail_login()
        content = self.create_content(buy_ids, sell_ids)
        self. send_mail(content)
        return True
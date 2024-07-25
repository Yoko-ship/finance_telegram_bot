import telebot,sqlite3
from datetime import date
import time

current_time = date.today()

data = sqlite3.connect("finance.db",check_same_thread=False)
cursor = data.cursor()

with data:
    data.execute("""
    CREATE TABLE IF NOT EXISTS Finance_Bot(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                Current_Time INT,
                Product TEXT,
                Price INT,
                Overall FLOAT
    )
""")



class TeleBot:
    def __init__(self,token):
        self.bot = telebot.TeleBot(token)
        self._setup_handlers()



    def _setup_handlers(self):
        @self.bot.message_handler(content_types=["text"])
        def send_welcome(message):
            if message.text == "/help":
                self.bot.send_message(message.chat.id,"Доступные команды: /finance_help")
            elif message.text == "/finance_help":
                self.bot.send_message(message.chat.id,"Укажите сумму бюджета,товар,и цену на товар через запятые")
                self.bot.register_next_step_handler(message,self.finance_accounting)
            else:
                self.bot.send_message(message.chat.id,"Попробуйте написать /help")


    def finance_accounting(self,message):
        self.userInput = message.text
        try:
            self.budget,self.goods,self.pricing = self.userInput.split(",")
            self.budget,self.goods,self.pricing = float(self.budget), str(self.goods),int(self.pricing)
            self.budget -= self.pricing
            self.bot.send_message(message.chat.id,"Данные были записаны ")
        except Exception:
            self.bot.send_message(message.chat.id,"Попробуйте написать бюджет, один товар и цену на товар через запятые в цифрах")
            self.bot.register_next_step_handler(message,self.finance_accounting)
        
        try:
            with data:
                sql = ("INSERT INTO Finance_Bot(Product,Price,Overall,Current_Time) VALUES(?,?,?,?)")
                info = (self.goods,self.pricing,self.budget,current_time)
                cursor.execute(sql,info)
        except AttributeError:
            print("")


    def run(self):
        self.bot.infinity_polling()


bot = TeleBot(api_token)
bot.run()




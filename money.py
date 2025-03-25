import time
import telebot
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

TOKEN = '7507265595:AAHl_YE6ivtsQo3roFKL5c21JEZkOlVzQhU'
bot = telebot.TeleBot(TOKEN)

options = Options()
options.add_experimental_option("detach", True)

url = "https://cbr.ru/currency_base/daily/"
driver = webdriver.Chrome(options=options)
driver.get(url)
def get_exchange_rates():
    driver.find_element(by=By.CLASS_NAME, value="datepicker-filter_button").click()
    driver.find_element(by=By.CLASS_NAME, value="ui-datepicker-month").click()
    driver.find_element(by=By.XPATH, value="/html/body/main/div/div/div/div[2]/form/div/div/div/div/div/div/div[2]/div/div/div/div/select[1]/option[2]").click()
    time.sleep(2)
    driver.find_element(by=By.XPATH, value="/html/body/main/div/div/div/div[2]/form/div/div/div/div/div/div/div[2]/div/div/table/tbody/tr[1]/td[6]/a").click()
    table_id = driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[3]/div/table")
    rows = table_id.find_elements(By.TAG_NAME, "td")
    text1 = []
    for row in rows:
        text1.append(row.text)
    values = text1[1::5]
    rate = text1[4::5]
    time.sleep(5)
    driver.find_element(by=By.XPATH, value="/html/body/main/div/div/div/div[2]/form/div/div/div/div/div/button").click()
    driver.find_element(by=By.XPATH, value="/html/body/main/div/div/div/div[2]/form/div/div/div/div/div/div/div[2]/div/div/table/tbody/tr[5]/td[5]/a").click()
    table_id = driver.find_element(By.XPATH, "/html/body/main/div/div/div/div[3]/div/table")
    rows2 = table_id.find_elements(By.TAG_NAME, "td")
    text2 = []
    for row in rows2:
        text2.append(row.text)
    rate2 = text2[4::5]
    return dict(zip(values, rate)), dict(zip(values, rate2))


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,"Привет! Напишите валюту (например, USD), чтобы сравнить курс на 1 и 28 февраля 2025г. Напишите /list, чтобы увидеть все доступные валюты.")

@bot.message_handler(commands=['list'])
def list_currencies(message):
    rates_1_feb, _ = get_exchange_rates()
    currency_list = ', '.join(rates_1_feb.keys())
    bot.send_message(message.chat.id, f"Доступные валюты: {currency_list}")

@bot.message_handler(func=lambda message: len(message.text) == 3)
def compare_exchange_rates(message):
    currency = message.text.upper()
    rates_1_feb, rates_28_feb = get_exchange_rates()

    if currency in rates_1_feb and currency in rates_28_feb:
        try:
            rate_1_feb = float(rates_1_feb[currency].replace(',', '.'))
            rate_28_feb = float(rates_28_feb[currency].replace(',', '.'))

            if rate_28_feb < rate_1_feb:
                bot.send_message(message.chat.id, '😊')
            else:
                bot.send_message(message.chat.id, '😞')
        except ValueError:
            bot.send_message(message.chat.id, "Ошибка")
    else:
        bot.send_message(message.chat.id, "Неверный ввод валюты. Попробуйте снова. Если нужен полный список доступных валют, напишите /list")

@bot.message_handler(func=lambda message: len(message.text) != 3)
def handle_invalid_currency_length(message):
    bot.send_message(message.chat.id, "Пожалуйста, введите наименовение валюты, состоящее из трех символов. Например: USD")

if __name__ == '__main__':
    bot.polling()
import requests # Позволяет выкачивать код целевой страницы
import random # Позволяет перемешать данные
import telebot # Позволяет работать с ботом
from bs4 import BeautifulSoup as b # Позволяет осуществлять парсинг

URL = 'https://www.anekdot.ru/' # Адрес целевой страницы
API_KEY = '5399599382:AAEcdahfiP8PnQb4kI0GHgdrVSC_RgR35OQ' # Токен бота

# Функция осуществляющая парсинг
def parser(url): # На вход принимает url-адрес
    r = requests.get(url) # Выкачивает код страницы
    soup = b(r.text, 'html.parser') # Запускаем html парсер
    anekdots = soup.find_all('div', class_='text') # Выкачиваем и парсим с сайта указанную информацию
    return [c.text for c in anekdots] # Возвращаем только текст без 'div'

list_of_jokes = parser(URL) # Создаём лист с выкаченной с URL информацией
random.shuffle(list_of_jokes) # Перемешиваем наш list_of_jokes

bot = telebot.TeleBot(API_KEY) # Идентифицируем нашего бота
@bot.message_handler(commands=['start']) # Декоратор с обработчиком сообщений (хендлер)

# Функция отправляющая сообщение конкретному пользователю
def hello(message):
    bot.send_message(message.chat.id, 'Привет! Введи "+", чтобы посмеяться. Лучшие анекдоты ждут тебя.')

@bot.message_handler(content_types=['text']) # Хендлер воспринимающий любой текст
def jokes(message): # Функция анализирующая релевантные данные
    if message.text.lower() in '+':
        bot.send_message(message.chat.id, list_of_jokes[0])
        del list_of_jokes[0] # Удаление использованной информации
    else:
        bot.send_message(message.chat.id, 'Введите "+"')

bot.polling() # Постоянное повторение запуска бота
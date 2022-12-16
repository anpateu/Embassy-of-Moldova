import requests
import shelve
import datetime
import pytz
import telebot
from config import Config


def init():
    names = []
    names.append('Оформление заграничного паспорта')
    names.append('Оформление внутреннего паспорта')
    names.append('Нотариальные действия')
    names.append('Признание')
    names.append('Выход из гражданства')
    names.append('Восстановление гражданства')
    names.append('Выезд на постоянное место жительства')
    names.append('Перерегистрация актов')

    uslugi = []
    uslugi.append('?filter[slotSize]=1200&filter[resourceId]=3558f672-9ee1-452b-a630-34437f09b4d1&filter[serviceId]=f8c23fdc-e908-47a5-80f7-a1b43732cf26')
    uslugi.append('?filter[slotSize]=900&filter[resourceId]=eb4e43fe-9b6d-4dfd-99ad-451ca81bb630&filter[serviceId]=c2fbd5eb-6966-4ead-b7c1-1a0eb65cf295')
    uslugi.append('?filter[slotSize]=1200&filter[resourceId]=0a840ab9-a324-4187-a502-d08ec0f5721e&filter[serviceId]=8e13743d-076d-4aa0-b0c2-c8d3c2b64de2')
    uslugi.append('?filter[slotSize]=1800&filter[resourceId]=1997eb33-01ac-44cb-b8e6-2dad771ac71a&filter[serviceId]=63fe0e8c-b127-43e3-874a-bac9c660045b')
    uslugi.append('?filter[slotSize]=1800&filter[resourceId]=f36c0d4f-71ec-4b39-8660-2337857176ed&filter[serviceId]=acc4f784-7535-4220-ae06-6e3648a8e829')
    uslugi.append('?filter[slotSize]=1800&filter[resourceId]=f36c0d4f-71ec-4b39-8660-2337857176ed&filter[serviceId]=038869df-58b5-437e-b3cf-60c5419ab053')
    uslugi.append('?filter[slotSize]=1800&filter[resourceId]=f36c0d4f-71ec-4b39-8660-2337857176ed&filter[serviceId]=429622e5-fac8-47fc-8f64-486810761984')
    uslugi.append('?filter[slotSize]=2700&filter[resourceId]=b6eae6ed-86ac-4ed7-9fe5-2482f0d0bcb9&filter[serviceId]=59c845fa-48c9-4f79-b7b2-1d07f895f2e6')

    return names, uslugi

def check_free_dates(usluga, name, i):
    current_time = datetime.datetime.now(pytz.timezone('Europe/Amsterdam')).strftime('[%H:%M:%S]')
    time_now = current_time
    print(f'{time_now}: {name}')

    start_date = current_time
    end_date = start_date + datetime.timedelta(days=179)

    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')

    url = f'https://api.reservio.com/v2/businesses/{businessId}/availability/booking-days{usluga}&filter[from]={start_date}&filter[to]={end_date}&sort=-createdAt'
    head = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=head)
    try:
        dates = response.json()
        for element in dates['data']:
            if element['attributes']['isAvailable'] != False:
                message = f"[!] {name}\nСвободная дата: {element['attributes']['date']}!"
                path = f'user/{i + 2}-noty-{i + 1}'
                with shelve.open(path) as data:
                    for key in data:
                        if data[key] == 'on':
                            bot.send_message(int(key), message)
                            print(f'Отправляю уведомление для {key}')
                            bot.send_message(owner, message)
    except:
        print(response)


if __name__ == '__main__':
    names, uslugi = init()

    owner = Config.OWNER_CHAT_ID
    bot = telebot.TeleBot(Config.TG_API_TOKEN)

    businessId = '09250556-2450-437f-aede-82e78712f114'

    while True:
        try:
            for i in range(8):
                check_free_dates(uslugi[i], names[i], i)
        except Exception as e:
            message = str(e)
            bot.send_message(owner, message)
            print(e)
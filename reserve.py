import requests
import datetime
import telebot
from config import Config

business_id = '09250556-2450-437f-aede-82e78712f114'
services = {
    'pasaportului': ['3558f672-9ee1-452b-a630-34437f09b4d1', 'f8c23fdc-e908-47a5-80f7-a1b43732cf26'], # загран
    'buletinului': ['eb4e43fe-9b6d-4dfd-99ad-451ca81bb630', 'c2fbd5eb-6966-4ead-b7c1-1a0eb65cf295'],  # паспорт
    'notariale': ['0a840ab9-a324-4187-a502-d08ec0f5721e', '8e13743d-076d-4aa0-b0c2-c8d3c2b64de2'],    # нотариус
    'recunoastere': ['1997eb33-01ac-44cb-b8e6-2dad771ac71a', '63fe0e8c-b127-43e3-874a-bac9c660045b'], # признание
    'renuntarea': ['f36c0d4f-71ec-4b39-8660-2337857176ed', 'acc4f784-7535-4220-ae06-6e3648a8e829'],   # выход
    'redobindirea': ['f36c0d4f-71ec-4b39-8660-2337857176ed', '038869df-58b5-437e-b3cf-60c5419ab053'], # восстановление
    'emigrare': ['f36c0d4f-71ec-4b39-8660-2337857176ed', '429622e5-fac8-47fc-8f64-486810761984'],     # выезд
    'transcrierea': ['b6eae6ed-86ac-4ed7-9fe5-2482f0d0bcb9', '59c845fa-48c9-4f79-b7b2-1d07f895f2e6'], # перерегистрация
}


def login(username, password):
    login_url = "https://accounts.reservio.com/api/login"
    payload = {
        "grant_type": "password",
        "password": password,
        "username": username
    }
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7",
        "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
        "sec-ch-ua": "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Google Chrome\";v=\"110\"",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin"
    }

    with requests.Session() as session:
        response = session.post(login_url, headers=headers, data=payload)
        cookies = response.cookies
    return cookies, headers


def get_available_dates(service, cookies, headers):
    today = datetime.datetime.utcnow()
    six_months = today + datetime.timedelta(days=120)
    booking_url = f"https://ambasada-r-moldova-in-f-rusa.reservio.com/api/v2/businesses/{business_id}/" \
                  "availability/booking-days?" \
                  f"filter[from]={today.isoformat()}Z" \
                  f"&filter[resourceId]={service[0]}" \
                  f"&filter[serviceId]={service[1]}" \
                  f"&filter[to]={six_months.isoformat()}Z" \
                  "&ignoreBookingBoundaries=0"

    headers.update({
        "accept": "application/vnd.api+json",
        "accept-encoding": "gzip, deflate, br",
        "cookie": '; '.join([f"{cookie.name}={cookie.value}" for cookie in cookies]),
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/110.0.0.0 Mobile Safari/537.36"
    })

    response = requests.get(booking_url, headers=headers)
    response.raise_for_status()
    data = response.json()

    available_dates = []
    for day in data["data"]:
        if day["attributes"]["isAvailable"]:
            available_dates.append(day["attributes"]["date"])
    return available_dates


if __name__ == "__main__":
    owner_id = Config.OWNER_ID
    bot = telebot.TeleBot(Config.TOKEN)
    cookies, headers = login(Config.LOGIN, Config.PASSWORD)

    while True:
        for service in services:
            available_dates = get_available_dates(services[service], cookies, headers)
            if available_dates:
                message = f"Доступные даты для услуги {service}: {', '.join(available_dates)}"
                bot.send_message(owner_id, message)
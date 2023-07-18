import random
import string
from flask import Flask, redirect, url_for, request
from urllib.parse import urlparse
import time
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

#Инициализация приложения
app = Flask(__name__, template_folder='templates')

#Словарь для приема ссылок (вместо БД)
shortened_urls = {}

#Функция генерация коротких ссылок (подается длина ссылки на вход)
#Используются символы (буква и цифры ascii), а также модуль random
#для случайного выбора символов
def genereate_short_url(lenght=6):
    chars = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(chars) for _ in range(lenght))
    return short_url

def delete_expired_urls():
    keys_to_delete = []
    for key,value in shortened_urls.items():
        lifetime = value.get('lifetime_seconds')
        if lifetime != None:
            creation_time = value.get('current_time')
            if time.time() > lifetime + creation_time:
                keys_to_delete.append(key)
    for key in keys_to_delete:
        shortened_urls.pop(key)

@app.route('/shorts', methods=['POST'])
def create_short_url():
    data = request.get_json()
    long_url = data['url']
    lifetime_seconds = data.get('lifetime')
    #генерация короткого url
    short_url = genereate_short_url()
    #проверка на то есть ли сгенерированный короткий url в словаре
    while short_url in shortened_urls:
        short_url = genereate_short_url()
    if lifetime_seconds != None:
        current_time = time.time()
        shortened_urls[short_url] = {"long_url":long_url, 'current_time': current_time, 'lifetime_seconds':lifetime_seconds}
    else:
        shortened_urls[short_url] = {"long_url":long_url}
    return {"url": short_url}

@app.route('/shorts/<url>', methods=['GET'])
def redirect_short_url(url):
    try:
        long_url = shortened_urls.get(url).get('long_url')
        return redirect(long_url)
    except:
        return {"error":"URL not found, 404"}

@app.route('/shorts/<url>', methods=['DELETE'])
def delete_url(url):
    if shortened_urls.pop(url) != -1:
        return 'deleted'
    else:
        return {"error":"unknown url"}
scheduler = BackgroundScheduler()
scheduler.add_job(func=delete_expired_urls, trigger="interval", seconds=60)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    app.run(debug=True, port = 8001)
import random
import string
from flask import Flask, render_template, redirect, url_for, request

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


@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        #получение url, указанного на форме
        long_url = request.form['long_url']
        #получение url, указанного на форме
        # delete_short_url = request.form['delete_short_url']
        # #удаление ключа из словаря
        # if delete_short_url != '':
        #     return shortened_urls.pop(short_url, None)
        # #генерация короткого url
        short_url = genereate_short_url()
        #проверка на то есть ли сгенерированный короткий url в слова
        #выйдем из цикла, кто получим уникальное значение
        while short_url in shortened_urls:
            short_url = genereate_short_url()
        shortened_urls[short_url] = long_url
        #возвращаем корневой url + сгенерированный короткий
        return f"Shortened URL: {request.url_root}{short_url}"
    return render_template('index.html')
    

@app.route('/<short_url>')
def redirect_url(short_url):
    long_url = shortened_urls.get(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return "URL not found", 404

if __name__ == '__main__':
    app.run(debug=True, port = 8001)
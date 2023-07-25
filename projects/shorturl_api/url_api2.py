from flask import Flask, redirect, url_for, request
from urllib.parse import urlparse
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from class_interface import Url_shorter_dict, Url_shorter_sql

#Инициализация приложения
app = Flask(__name__, template_folder='templates')

test = False

if test:
        
    @app.route('/shorts/<url>', methods=['GET'])
    def redirect_short_url(url):
        pass

    @app.route('/shorts/<url>', methods=['DELETE'])
    def delete_url(url):
        pass

    scheduler = BackgroundScheduler()
    scheduler.add_job(func=delete_expired_urls, trigger="interval", seconds=60)
    scheduler.start()
else:
    pass


# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

if __name__ == '__main__':
    app.run(debug=True, port = 8001)
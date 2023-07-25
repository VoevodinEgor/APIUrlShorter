from abc import ABC, abstractmethod
import time
import random
import string
from requests import request
from flask import redirect, Flask

app = Flask(__name__, template_folder='templates')

class Formal_url_shorter_interface(ABC):
    @abstractmethod
    def get_url(self):
        pass
    def set_url(self):
        pass
    def delete_url(self):
        pass

class Url_shorter_sql(Formal_url_shorter_interface):
    
    @app.route('/shorts/<url>', methods=['GET'])
    def get_url(self, short_url: str) -> str:
        pass
    
    @app.route('/shorts', methods=['POST'])
    def set_url(self, url: str) -> None:
        pass

    @app.route('/shorts/<url>', methods=['DELETE'])
    def delete_url(self, short_url: str) -> None:
        pass

class Url_shorter_dict(Formal_url_shorter_interface):
    shortened_urls = {}

    @app.route('/shorts/<url>', methods=['GET'])
    def get_url(self, short_url: str) -> str:
        pass
    
    @app.route('/shorts', methods=['POST'])
    def set_url(self, url: str, lenght = 6) -> str:
        chars = string.ascii_letters + string.digits
        short_url = ''.join(random.choice(chars) for _ in range(lenght))
        while short_url in self.shortened_urls:
            short_url = ''.join(random.choice(chars) for _ in range(lenght))
        data = request.get_json()
        long_url = data['url']
        lifetime_seconds = data.get('lifetime')
        if lifetime_seconds != None:
            current_time = time.time()
            self.shortened_urls[short_url] = {"long_url":long_url, 'current_time': current_time, 'lifetime_seconds':lifetime_seconds}
        else:
            self.shortened_urls[short_url] = {"long_url":long_url}
        return {"url": short_url}

    @app.route('/shorts/<url>', methods=['DELETE'])
    def delete_url(self, short_url: str) -> None:
        if self.shortened_urls.pop(url) != -1:
            return 'deleted'
        else:
            return {"error":"Unknown url"}
    
    def delete_expired_urls(self) -> None:
        keys_to_delete = []
        for key,value in self.shortened_urls.items():
            lifetime = value.get('lifetime_seconds')
            if lifetime != None:
                creation_time = value.get('current_time')
                if time.time() > lifetime + creation_time:
                    keys_to_delete.append(key)
        for key in keys_to_delete:
            self.shortened_urls.pop(key)

    def redirect_short_url(self, url: str) -> str:
        try:
            long_url = self.shortened_urls.get(url).get('long_url')
            return redirect(long_url)
        except:
            return {"error":"URL not found, 404"}


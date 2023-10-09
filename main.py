import os
import signal
import subprocess
from flask import Flask, request
import requests
import time
import validators

app = Flask(__name__)
@app.route('/proxy')
def fn_proxy():
    path = request.url.split('url=', 1)[1]
    print(path)
    if not validators.url(path):
        return "Not a valid url!"
    arti_process = subprocess.Popen("./arti proxy", stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
    requests.utils.default_user_agent = lambda: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    time.sleep(2)
    proxies= {
       'http': 'socks5h://127.0.0.1:9150',
       'https': 'socks5h://127.0.0.1:9150'
    }
    r = requests.get(url=path, proxies=proxies)
    os.killpg(os.getpgid(arti_process.pid), signal.SIGTERM)
    print(r.text)
    return r.text

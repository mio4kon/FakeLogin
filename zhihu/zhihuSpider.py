import sys
sys.path.append("..")
import log
import requests
import re
import json
import time
from PIL import Image

try:
    import cookielib
except:
    import http.cookiejar as cookielib

session = requests.session()

headers = {
    "Host": "www.zhihu.com",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0 Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
    "Accept":
    "text/html,application/xhtml+xml,application/xmlq=0.9,image/webp,*/*q=0.8",
    "DNT": "1",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "zh-CN,zhq=0.8,zh-TWq=0.6,enq=0.4",
}


def get_xsrf():
    index_url = 'http://www.zhihu.com'
    response = session.get(index_url, headers=headers, verify=False)
    html = response.text
    pattern = r'name="_xsrf"\s*value="(.*?)"'
    _xsrf = re.findall(pattern, html)
    if len(_xsrf) == 0:
        log.d('get _xsrf error!')
        return
    log.d('get _xsrf :' + _xsrf[0])
    return _xsrf[0]


def getCaptcha():
    savaName = 'captcha.jpg'
    t = str(int(time.time() * 1000))
    captchaUrl = 'http://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    captchaResponse = session.get(captchaUrl, headers=headers, verify=False)
    with open(savaName, 'wb') as f:
        f.write(captchaResponse.content)
    im = Image.open(savaName)
    im.show()
    im.close()
    captcha = input("请输入验证码:\n")
    return captcha


def login(username, password):
    log.d("being login.. \nusername:" + username)
    postUrl = 'http://www.zhihu.com/login/email'
    _xsrf = get_xsrf()
    # request headers
    headers['X-Requested-With'] = 'XMLHttpRequest'
    headers['X-Xsrftoken'] = _xsrf
    # form data
    captcha = getCaptcha()
    log.d("get Captcha is :" + captcha)
    formData = {
        '_xsrf': _xsrf,
        'email': username,
        'password': password,
        'remember_me': 'true',
    }
    formData['captcha'] = captcha
    loginResponse = session.post(
        postUrl, data=formData, headers=headers, verify=False)
    loginJson = json.loads(loginResponse.text)
    log.d('json:' + str(loginJson))


try:
    login('mio4kon.dev@gmail.com', '1234567')
except Exception as e:
    log.e(e)
finally:
    log.save()

import requests

class Xpost1:
    def __init__(self):
        
        self.token = '7063678462:AAFwJOQrSx7xGIij5g3-E6GxxjMXjZgcxWA'
        self.chat_id = '5846480832'

    def telegram(self, message):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        params = {
            'chat_id': self.chat_id,
            'text': message
        }
        response = requests.post(url, params=params)
        

class Xpost2:
    def __init__(self):
        
        self.token = '7185238502:AAGt-D793CTyyQMqVfsiN2FVOryRO2RggyI'
        self.chat_id = '5846480832'

    def telegram(self, message):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        params = {
            'chat_id': self.chat_id,
            'text': message
        }
        response = requests.post(url, params=params)
        

class Xpost3:
    def __init__(self):
        
        self.token = '6995663800:AAEpDJKY-MxfySvb_n2fl0rH5GnQT4jgNkc'
        self.chat_id = '5846480832'

    def telegram(self, message):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        params = {
            'chat_id': self.chat_id,
            'text': message
        }
        response = requests.post(url, params=params)
        

class Xpost4:
    def __init__(self):
        
        self.token = '7005002027:AAF1LTjc56uwgacCDuLlAmj5v3VZ4SysIIY'
        self.chat_id = '5846480832'

    def telegram(self, message):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        params = {
            'chat_id': self.chat_id,
            'text': message
        }
        response = requests.post(url, params=params)
        

class Xpost5:
    def __init__(self):
        
        self.token = '6880564530:AAHyMXRe_uxSVsD__xPNChqbiwQsv20H2lE'
        self.chat_id = '5846480832'

    def telegram(self, message):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        params = {
            'chat_id': self.chat_id,
            'text': message
        }
        response = requests.post(url, params=params)
        

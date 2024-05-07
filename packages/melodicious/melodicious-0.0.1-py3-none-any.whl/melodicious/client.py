import requests
import traceback
import datetime


class APIClient:
    def __init__(self, base_url, username, usertoken, callEndpoint, configs, tokenEndpoint='tokenAPI', tokenPort=80,
                 callPort=80):
        self.session = requests.Session()
        self.username = username
        self.usertoken = usertoken
        self.login_url = f'{base_url}:{tokenPort}/{tokenEndpoint}'
        self.call_url = f'{base_url}:{callPort}/{callEndpoint}'
        self.configs = configs
        self.token = None

    def print_traceback(self):
        """TRACE ERROR"""
        head = '\n[📒]'
        upline = '=' * 52
        downline = '=' * 58
        print(f'{head}{upline}{traceback.format_exc()}{downline}')

    def login(self):
        """LOG IN"""
        nowtime = datetime.datetime.now()
        print(f'🔑 [login] {nowtime}')

        try:
            userinfo = {'username': self.username, 'usertoken': self.usertoken}
            response = self.session.post(url=self.login_url, json=userinfo).json()
            if response.get('status') == 'success':
                self.token = response.get('token')
                return {'status': 'success', 'message': 'token success'}
            else:
                return response
        except:
            self.print_traceback()
            return {'status': 'error', 'message': 'login issue'}

    def call(self):
        """CALL API"""
        print('🏃🏻‍ [running]')
        if not self.token:
            if not self.login():
                print("⚠️ Login failed")
                return None

        headers = {'Authorization': f'Bearer {self.token}'}
        self.configs.update({'username': self.username})
        try:
            response = self.session.get(url=self.call_url, headers=headers, json=self.configs, stream=True).json()
            if response.get('status') == 'success':
                return response
            else:
                return response
        except:
            self.print_traceback()
            return {'status': 'error', 'message': 'call issue'}

    def playing(self):
        """Main Run"""
        try:
            login_response = self.login()
            if login_response.get('status') == 'success':
                api_response = self.call()
                print('🌈 [success]\n')
                return api_response
            else:
                return login_response
        except:
            self.print_traceback()
            return {'status': 'error', 'message': 'Main issue'}

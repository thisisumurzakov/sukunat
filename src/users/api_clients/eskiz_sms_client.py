import os

import redis
import requests
from .sms_client_interface import SMSClientInterface


class EskizSmsClient(SMSClientInterface):
    def __init__(self):
        self.base_url = 'https://notify.eskiz.uz/api'
        self.email = os.getenv('ESKIZ_EMAIL')
        self.password = os.getenv('ESKIZ_PASSWORD')
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

    def authenticate(self):
        token = self.redis_client.get('eskiz_token')
        if token:
            return token
        auth_url = f"{self.base_url}/auth/login"
        data = {'email': self.email, 'password': self.password}
        response = requests.post(auth_url, data=data)
        if response.status_code == 200:
            token = response.json()['data']['token']
            # Cache the token. Assuming token expiry is 24 hours.
            self.redis_client.set('eskiz_token', token, ex=86390)
            return token
        else:
            raise Exception('Authentication Failed')

    def send_sms(self, phone_number, message):
        token = self.authenticate()
        send_url = f"{self.base_url}/message/sms/send"
        headers = {'Authorization': f'Bearer {token}'}
        payload = {
            'mobile_phone': phone_number,
            'message': message,
            'from': '5000',  # This should be your registered sender name
        }
        response = requests.post(send_url, headers=headers, data=payload)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                return True, "SMS sent successfully"
            else:
                return False, data['message']
        else:
            return False, f"Failed to send SMS with status code {response.status_code}"

import json

from requests import session
from urllib3.filepost import choose_boundary


class HTTPClient:

    def __init__(self, base_url: str = '', *, timeout=120, debug=False):
        self._base_url = base_url.rstrip('/')
        self._s = session()
        self._timeout = timeout
        self.debug = debug

    @staticmethod
    def _encode_data_to_form_data(data):
        """将dict转换为multipart/form-data"""
        body = b''
        boundary = f'----{choose_boundary()}'
        content_type = f'multipart/form-data; boundary={boundary}'  # noqa
        for key, value in data.items():
            value = "" if value is None else str(value)
            body += f'--{boundary}\r\n'.encode('utf-8')
            body += f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode('utf-8')  # noqa
            body += f'{value}\r\n'.encode('utf-8')
        body += f'--{boundary}--'.encode('utf-8')
        return body, content_type

    def request(self, method, url: str, *, params=None, data=None, headers=None, cookies=None, files=None):
        if not url.startswith('http://') and not url.startswith('https://'):
            url = self._base_url + url
        debug = [f'{method} - {url}']

        if not headers:
            headers = {}
        if 'Content-Type' not in headers:
            headers['Content-Type'] = 'application/json;charset=UTF-8'
        if 'application/json' in headers['Content-Type'] and data:
            try:
                debug.append(f'Payload - {json.dumps(data, ensure_ascii=False)}')
                data = json.dumps(data, ensure_ascii=True)
                # debug.insert(-1, f'Headers - {headers}')
            except TypeError as e:
                pass
        elif 'multipart/form-data' in headers['Content-Type'] and data:
            debug.append(f'Form Data - {data}')
            data, content_type = self._encode_data_to_form_data(data)
            headers['Content-Type'] = content_type
            # debug.insert(-1, f'Headers - {headers}')
        return self._s.request(
            method, url, params=params, data=data, headers=headers, cookies=cookies, files=files, verify=False,
            timeout=self._timeout
        )

    def get(self, url, *, params=None, headers=None, cookies=None):
        return self.request('GET', url, params=params, headers=headers, cookies=cookies)

    def post(self, url, *, data=None, headers=None, cookies=None):
        return self.request('POST', url, data=data, headers=headers, cookies=cookies)

    def put(self, url, *, data=None, headers=None, cookies=None):
        return self.request('PUT', url, data=data, headers=headers, cookies=cookies)

    def delete(self, url, *, data=None, headers=None, cookies=None):
        return self.request('DELETE', url, data=data, headers=headers, cookies=cookies)

    def close(self):
        self._s.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


if __name__ == '__main__':
    client = HTTPClient('http://192.168.1.53:30011')
    rep = client.post('/user/oauth/token', data={
        "username": "hosontest88",
        "password": "c5da3ad4b028d8746dde18804ef765c1",
        "captchaToken": "",
        "client_id": "factory",
        "client_secret": "secret",
        "grant_type": "password",
    }, headers={'Content-Type': 'multipart/form-data'})
    # rep = client.post('/product/shell-price/page', data={"size": 50, "current": 1, "tenantId": None})
    print(rep.status_code)
    print(rep.json())
